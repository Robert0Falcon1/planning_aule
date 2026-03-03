"""
Router per la gestione dei conflitti tra prenotazioni.
Solo COORDINAMENTO può accedere a questi endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from backend.database import get_db
from backend.core.dependencies import get_utente_corrente
from backend.models.utente import Utente
from backend.models.conflitto import ConflittoPrenotazione
from backend.services.conflitti_service import ConflittoService
from backend.models.enums import RuoloUtente

router = APIRouter(prefix="/conflitti", tags=["Conflitti"])


def require_coordinamento(utente: Utente = Depends(get_utente_corrente)):
    """Verifica che l'utente sia COORDINAMENTO"""
    if utente.ruolo != RuoloUtente.COORDINAMENTO:
        raise HTTPException(
            status_code=403,
            detail="Accesso negato: richiesto ruolo COORDINAMENTO"
        )
    return utente


@router.get("/", summary="Lista conflitti")
def lista_conflitti(
    sede_id: Optional[int] = None,
    solo_attivi: bool = True,
    db: Session = Depends(get_db),
    utente: Utente = Depends(require_coordinamento)
):
    """
    Lista conflitti tra prenotazioni.
    Solo COORDINAMENTO può visualizzare i conflitti.
    """
    if solo_attivi:
        conflitti = ConflittoService.get_active_conflicts(db, sede_id)
    else:
        query = db.query(ConflittoPrenotazione)
        if sede_id:
            from backend.models.prenotazione import Prenotazione
            from backend.models.aula import Aula
            query = (
                query
                .join(Prenotazione, ConflittoPrenotazione.prenotazione_id_1 == Prenotazione.id)
                .join(Aula, Prenotazione.aula_id == Aula.id)
                .filter(Aula.sede_id == sede_id)
            )
        conflitti = query.all()
    
    return [
        {
            "id": c.id,
            "prenotazione_id_1": c.prenotazione_id_1,
            "prenotazione_id_2": c.prenotazione_id_2,
            "tipo_conflitto": c.tipo_conflitto.value,
            "stato_risoluzione": c.stato_risoluzione.value,
            "rilevato_il": c.rilevato_il,
            "risolto_il": c.risolto_il,
        }
        for c in conflitti
    ]


@router.get("/{conflitto_id}", summary="Dettaglio conflitto")
def dettaglio_conflitto(
    conflitto_id: int,
    db: Session = Depends(get_db),
    utente: Utente = Depends(require_coordinamento)
):
    """Dettaglio completo di un conflitto con le due prenotazioni coinvolte"""
    conflitto = db.query(ConflittoPrenotazione).filter(
        ConflittoPrenotazione.id == conflitto_id
    ).first()
    
    if not conflitto:
        raise HTTPException(404, "Conflitto non trovato")
    
    return {
        "conflitto": {
            "id": conflitto.id,
            "tipo_conflitto": conflitto.tipo_conflitto.value,
            "stato_risoluzione": conflitto.stato_risoluzione.value,
            "rilevato_il": conflitto.rilevato_il,
            "risolto_il": conflitto.risolto_il,
            "note_risoluzione": conflitto.note_risoluzione,
        },
        "prenotazione_1": {
            "id": conflitto.prenotazione_1.id,
            "corso_id": conflitto.prenotazione_1.corso_id,
            "aula_id": conflitto.prenotazione_1.aula_id,
        },
        "prenotazione_2": {
            "id": conflitto.prenotazione_2.id,
            "corso_id": conflitto.prenotazione_2.corso_id,
            "aula_id": conflitto.prenotazione_2.aula_id,
        }
    }


@router.post("/{conflitto_id}/risolvi", summary="Risolvi conflitto")
def risolvi_conflitto(
    conflitto_id: int,
    azione: str,
    note: str = "",
    db: Session = Depends(get_db),
    utente: Utente = Depends(require_coordinamento)
):
    """
    Risolve un conflitto.
    
    Azioni possibili:
    - mantieni_1: mantiene prenotazione 1, elimina 2
    - mantieni_2: mantiene prenotazione 2, elimina 1
    - elimina_entrambe: elimina entrambe
    - manuale: segna come risolto senza eliminazioni
    """
    try:
        conflitto = ConflittoService.resolve_conflict(
            db, conflitto_id, utente.id, azione, note
        )
        db.commit()
        
        return {
            "ok": True,
            "message": f"Conflitto risolto: {azione}",
            "conflitto": {
                "id": conflitto.id,
                "stato_risoluzione": conflitto.stato_risoluzione.value,
                "risolto_il": conflitto.risolto_il,
            }
        }
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/stats/summary", summary="Statistiche conflitti")
def statistiche_conflitti(
    sede_id: Optional[int] = None,
    db: Session = Depends(get_db),
    utente: Utente = Depends(require_coordinamento)
):
    """Statistiche riepilogative sui conflitti"""
    from backend.models.enums import StatoRisoluzioneConflitto
    
    query = db.query(ConflittoPrenotazione)
    
    if sede_id:
        from backend.models.prenotazione import Prenotazione
        from backend.models.aula import Aula
        query = (
            query
            .join(Prenotazione, ConflittoPrenotazione.prenotazione_id_1 == Prenotazione.id)
            .join(Aula, Prenotazione.aula_id == Aula.id)
            .filter(Aula.sede_id == sede_id)
        )
    
    totali = query.count()
    attivi = query.filter(
        ConflittoPrenotazione.stato_risoluzione == StatoRisoluzioneConflitto.NON_RISOLTO
    ).count()
    risolti = totali - attivi
    
    return {
        "totali": totali,
        "attivi": attivi,
        "risolti": risolti,
        "percentuale_risolti": (risolti / totali * 100) if totali > 0 else 0
    }