"""
Router per la gestione dei conflitti tra prenotazioni.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from backend.database import get_db
from backend.core.dependencies import get_utente_corrente, require_coordinamento
from backend.models.utente import Utente
from backend.models.conflitto import ConflittoPrenotazione
from backend.services.conflitti_service import ConflittoService
from backend.models.enums import RuoloUtente, StatoRisoluzioneConflitto

router = APIRouter(prefix="/conflitti", tags=["Conflitti"])


@router.get("/", summary="Lista conflitti")
def lista_conflitti(
    sede_id: Optional[int] = None,
    solo_attivi: bool = True,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    """
    Lista conflitti tra prenotazioni.
    - COORDINAMENTO: vede tutti i conflitti (filtrabile per sede)
    - OPERATIVO: vede solo i conflitti che coinvolgono le proprie prenotazioni
    """
    from backend.models.prenotazione import Prenotazione
    from backend.models.aula import Aula

    if solo_attivi:
        query = db.query(ConflittoPrenotazione).filter(
            ConflittoPrenotazione.stato_risoluzione == None
        )
    else:
        query = db.query(ConflittoPrenotazione)

    # Filtro sede (solo COORDINAMENTO)
    if sede_id and utente.ruolo == RuoloUtente.COORDINAMENTO:
        from backend.models.slot_orario import SlotOrario
        query = (
            query
            .join(SlotOrario, ConflittoPrenotazione.slot_id_1 == SlotOrario.id)
            .join(Aula, SlotOrario.aula_id == Aula.id)
            .filter(Aula.sede_id == sede_id)
        )

    # OPERATIVO: filtra solo i conflitti delle proprie prenotazioni
    if utente.ruolo == RuoloUtente.OPERATIVO:
        mie_pren_ids = db.query(Prenotazione.id).filter(
            Prenotazione.richiedente_id == utente.id
        ).scalar_subquery()
        query = query.filter(
            or_(
                ConflittoPrenotazione.prenotazione_id_1.in_(mie_pren_ids),
                ConflittoPrenotazione.prenotazione_id_2.in_(mie_pren_ids),
            )
        )

    conflitti = query.all()

    return [
        {
            "id": c.id,
            "prenotazione_id_1": c.prenotazione_id_1,
            "prenotazione_id_2": c.prenotazione_id_2,
            "slot_id_1": c.slot_id_1,
            "slot_id_2": c.slot_id_2,
            "tipo_conflitto": c.tipo_conflitto.value,
            "stato_risoluzione": c.stato_risoluzione.value if c.stato_risoluzione else None,
            "rilevato_il": c.rilevato_il,
            "risolto_il": c.risolto_il,
        }
        for c in conflitti
    ]


@router.get("/stats/summary", summary="Statistiche conflitti")
def statistiche_conflitti(
    sede_id: Optional[int] = None,
    db: Session = Depends(get_db),
    utente: Utente = Depends(require_coordinamento)
):
    """Statistiche riepilogative sui conflitti"""
    query = db.query(ConflittoPrenotazione)

    if sede_id:
        from backend.models.slot_orario import SlotOrario
        from backend.models.aula import Aula
        query = (
            query
            .join(SlotOrario, ConflittoPrenotazione.slot_id_1 == SlotOrario.id)
            .join(Aula, SlotOrario.aula_id == Aula.id)
            .filter(Aula.sede_id == sede_id)
        )

    totali = query.count()
    attivi = query.filter(
        ConflittoPrenotazione.stato_risoluzione == None
    ).count()
    risolti = totali - attivi

    return {
        "totali": totali,
        "attivi": attivi,
        "risolti": risolti,
        "percentuale_risolti": (risolti / totali * 100) if totali > 0 else 0
    }


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
            "stato_risoluzione": conflitto.stato_risoluzione.value if conflitto.stato_risoluzione else None,
            "rilevato_il": conflitto.rilevato_il,
            "risolto_il": conflitto.risolto_il,
            "note_risoluzione": conflitto.note_risoluzione,
        },
        "prenotazione_1": {
            "id": conflitto.prenotazione_1.id,
        },
        "prenotazione_2": {
            "id": conflitto.prenotazione_2.id,
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
    - mantieni_1: mantiene slot_1, annulla slot_2
    - mantieni_2: mantiene slot_2, annulla slot_1
    - elimina_entrambe: annulla entrambi gli slot in conflitto
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
        db.rollback()
        raise HTTPException(400, str(e))