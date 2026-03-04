"""
Router per la gestione delle prenotazioni aule - Sistema 2 RUOLI
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from backend.database import get_db
from backend.core.dependencies import get_utente_corrente, verifica_permesso
from backend.models.utente import Utente
from backend.models.prenotazione import Prenotazione, RichiestaPrenotazione
from backend.models.slot_orario import SlotOrario
from backend.models.aula import Aula
from backend.models.enums import StatoPrenotazione, StatoRichiesta, RuoloUtente
from backend.schemas.prenotazione import (
    PrenotazioneSingolaInput,
    PrenotazioneMassivaInput,
    PrenotazioneRisposta
)
from backend.services.booking_service import (
    crea_prenotazione_singola,
    crea_prenotazione_massiva
)
from backend.services.conflitti_service import ConflittoService
from datetime import date, datetime, timezone
from typing import Optional

router = APIRouter(prefix="/prenotazioni", tags=["Prenotazioni"])


@router.post("/singola", response_model=PrenotazioneRisposta, status_code=201,
             summary="Crea prenotazione singola")
def nuova_prenotazione_singola(
    dati: PrenotazioneSingolaInput,
    db: Session = Depends(get_db),
    utente: Utente = Depends(verifica_permesso("prenotazione:richiedere"))
):
    """
    Crea una prenotazione singola per un'aula.
    Sistema 2 ruoli: auto-approva immediatamente e rileva conflitti.
    """
    prenotazione, _ = crea_prenotazione_singola(db, dati, utente)
    
    # Rileva conflitti automaticamente
    conflitti = ConflittoService.detect_and_record_conflicts(db, prenotazione)
    
    # Auto-approva richiesta (sistema 2 ruoli)
    richiesta = RichiestaPrenotazione(
        prenotazione_id=prenotazione.id,
        stato=StatoRichiesta.APPROVATA,
        ha_conflitti=(len(conflitti) > 0),
        data_richiesta=datetime.now(timezone.utc),
        data_gestione=datetime.now(timezone.utc)
    )
    db.add(richiesta)
    db.commit()
    db.refresh(prenotazione)
    
    return prenotazione


@router.post("/massiva", response_model=PrenotazioneRisposta, status_code=201,
             summary="Crea prenotazione massiva (ricorrente)")
def nuova_prenotazione_massiva(
    dati: PrenotazioneMassivaInput,
    db: Session = Depends(get_db),
    utente: Utente = Depends(verifica_permesso("prenotazione:richiedere"))
):
    """
    Crea una prenotazione ricorrente generando automaticamente tutti gli slot.
    Sistema 2 ruoli: auto-approva immediatamente e rileva conflitti.
    """
    prenotazione, _ = crea_prenotazione_massiva(db, dati, utente)
    
    # Rileva conflitti automaticamente
    conflitti = ConflittoService.detect_and_record_conflicts(db, prenotazione)
    
    # Auto-approva richiesta (sistema 2 ruoli)
    richiesta = RichiestaPrenotazione(
        prenotazione_id=prenotazione.id,
        stato=StatoRichiesta.APPROVATA,
        ha_conflitti=(len(conflitti) > 0),
        data_richiesta=datetime.now(timezone.utc),
        data_gestione=datetime.now(timezone.utc)
    )
    db.add(richiesta)
    db.commit()
    db.refresh(prenotazione)
    
    return prenotazione


@router.get("/", response_model=list[PrenotazioneRisposta],
            summary="Lista prenotazioni")
def lista_prenotazioni(
    sede_id: Optional[int] = None,
    corso_id: Optional[int] = None,
    stato: Optional[StatoPrenotazione] = None,
    data_dal: Optional[date] = None,
    data_al: Optional[date] = None,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    """
    Restituisce le prenotazioni.
    
    Sistema 2 ruoli:
    - OPERATIVO: visualizza tutte le prenotazioni
    - COORDINAMENTO: visualizza tutte le prenotazioni
    
    Tutti gli utenti hanno visibilità completa sul sistema.
    """
    query = db.query(Prenotazione).options(
        joinedload(Prenotazione.richiesta),
        joinedload(Prenotazione.slots),
    )

    # Sistema 2 ruoli: tutti vedono tutto (nessun filtro per ruolo)
    # Filtri opzionali dalla querystring
    if sede_id:
        query = query.join(Aula).filter(Aula.sede_id == sede_id)
    
    if corso_id:
        query = query.filter(Prenotazione.corso_id == corso_id)
    
    if stato:
        query = query.filter(Prenotazione.stato == stato)
    
    if data_dal or data_al:
        query = query.join(SlotOrario)
        if data_dal:
            query = query.filter(SlotOrario.data >= data_dal)
        if data_al:
            query = query.filter(SlotOrario.data <= data_al)

    return query.order_by(Prenotazione.data_creazione.desc()).all()


@router.get("/{prenotazione_id}", response_model=PrenotazioneRisposta,
            summary="Dettaglio prenotazione")
def dettaglio_prenotazione(
    prenotazione_id: int,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    """Restituisce il dettaglio di una singola prenotazione."""
    p = (
        db.query(Prenotazione)
        .options(
            joinedload(Prenotazione.richiesta),
            joinedload(Prenotazione.slots)
        )
        .filter(Prenotazione.id == prenotazione_id)
        .first()
    )
    
    if not p:
        raise HTTPException(
            status_code=404,
            detail="Prenotazione non trovata"
        )
    
    return p


@router.delete("/{prenotazione_id}", status_code=200,
               summary="Elimina prenotazione")
def elimina_prenotazione(
    prenotazione_id: int,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    """
    Elimina una prenotazione.
    
    Permessi Sistema 2 ruoli:
    - OPERATIVO: può eliminare solo le proprie prenotazioni
    - COORDINAMENTO: può eliminare qualsiasi prenotazione
    """
    prenotazione = db.query(Prenotazione).filter(
        Prenotazione.id == prenotazione_id
    ).first()
    
    if not prenotazione:
        raise HTTPException(
            status_code=404,
            detail="Prenotazione non trovata"
        )
    
    # Verifica permessi
    if utente.ruolo != RuoloUtente.COORDINAMENTO:
        if prenotazione.richiedente_id != utente.id:
            raise HTTPException(
                status_code=403,
                detail="Non hai i permessi per eliminare questa prenotazione"
            )
    
    # Elimina richiesta associata
    richiesta = db.query(RichiestaPrenotazione).filter(
        RichiestaPrenotazione.prenotazione_id == prenotazione_id
    ).first()
    if richiesta:
        db.delete(richiesta)
    
    # Elimina prenotazione
    db.delete(prenotazione)
    db.commit()
    
    return {"message": f"Prenotazione {prenotazione_id} eliminata con successo"}


@router.patch("/{prenotazione_id}", response_model=PrenotazioneRisposta,
              summary="Modifica prenotazione")
def modifica_prenotazione(
    prenotazione_id: int,
    dati: PrenotazioneSingolaInput,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    """
    Modifica una prenotazione esistente (solo singole, non massive).
    
    Permessi Sistema 2 ruoli:
    - OPERATIVO: può modificare solo le proprie prenotazioni
    - COORDINAMENTO: può modificare qualsiasi prenotazione
    
    Nota: Ricrea slot e ricalcola conflitti.
    """
    prenotazione = db.query(Prenotazione).filter(
        Prenotazione.id == prenotazione_id
    ).first()
    
    if not prenotazione:
        raise HTTPException(
            status_code=404,
            detail="Prenotazione non trovata"
        )
    
    # Verifica permessi
    if utente.ruolo != RuoloUtente.COORDINAMENTO:
        if prenotazione.richiedente_id != utente.id:
            raise HTTPException(
                status_code=403,
                detail="Non hai i permessi per modificare questa prenotazione"
            )
    
    # Verifica che sia una prenotazione singola
    if prenotazione.tipo.value != "singola":
        raise HTTPException(
            status_code=400,
            detail="Puoi modificare solo prenotazioni singole"
        )
    
    # Aggiorna dati prenotazione
    prenotazione.aula_id = dati.aula_id
    prenotazione.corso_id = dati.corso_id
    prenotazione.note = dati.note
    
    # Elimina slot vecchi
    db.query(SlotOrario).filter(
        SlotOrario.prenotazione_id == prenotazione_id
    ).delete()
    
    # Crea nuovo slot
    nuovo_slot = SlotOrario(
        prenotazione_id=prenotazione.id,
        data=dati.slot.data,
        ora_inizio=dati.slot.ora_inizio,
        ora_fine=dati.slot.ora_fine
    )
    db.add(nuovo_slot)
    db.flush()
    
    # Ricalcola conflitti
    conflitti = ConflittoService.detect_and_record_conflicts(db, prenotazione)
    
    # Aggiorna richiesta
    richiesta = db.query(RichiestaPrenotazione).filter(
        RichiestaPrenotazione.prenotazione_id == prenotazione_id
    ).first()
    if richiesta:
        richiesta.ha_conflitti = (len(conflitti) > 0)
    
    db.commit()
    db.refresh(prenotazione)
    
    return prenotazione


@router.get("/slot-liberi/{aula_id}", summary="Slot liberi per aula")
def slot_liberi(
    aula_id: int,
    data_dal: date,
    data_al: date,
    db: Session = Depends(get_db),
    _: Utente = Depends(verifica_permesso("aula:vedere_slot_liberi"))
):
    """
    Restituisce gli slot occupati per un'aula in un range di date.
    Il frontend può calcolare gli slot liberi sottraendo quelli occupati.
    """
    slot_occupati = (
        db.query(SlotOrario)
        .join(Prenotazione)
        .filter(
            Prenotazione.aula_id == aula_id,
            Prenotazione.stato.in_([
                StatoPrenotazione.CONFERMATA,
                StatoPrenotazione.IN_ATTESA,
                StatoPrenotazione.CONFLITTO,
            ]),
            SlotOrario.data >= data_dal,
            SlotOrario.data <= data_al,
            SlotOrario.annullato == False,
        )
        .all()
    )
    
    return [{
        "data": s.data,
        "ora_inizio": s.ora_inizio,
        "ora_fine": s.ora_fine,
        "prenotazione_id": s.prenotazione_id,
    } for s in slot_occupati]