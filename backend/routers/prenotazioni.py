"""
Router per la gestione delle prenotazioni aule - Sistema 2 RUOLI
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError  # ← AGGIUNTO
from pydantic import BaseModel
from backend.database import get_db
from backend.core.dependencies import get_utente_corrente, verifica_permesso
from backend.models.utente import Utente
from backend.models.prenotazione import Prenotazione, RichiestaPrenotazione
from backend.models.slot_orario import SlotOrario
from backend.models.aula import Aula
from backend.models.conflitto import ConflittoPrenotazione
from backend.models.enums import StatoPrenotazione, StatoRichiesta, RuoloUtente, StatoRisoluzioneConflitto
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
from datetime import date, time, datetime, timezone
from typing import Optional

router = APIRouter(prefix="/prenotazioni", tags=["Prenotazioni"])


class SlotModificaInput(BaseModel):
    aula_id:    Optional[int]  = None
    corso_id:   Optional[int]  = None
    data:       Optional[date] = None
    ora_inizio: Optional[time] = None
    ora_fine:   Optional[time] = None
    note:       Optional[str]  = None


@router.post("/singola", response_model=PrenotazioneRisposta, status_code=201,
             summary="Crea prenotazione singola")
def nuova_prenotazione_singola(
    dati: PrenotazioneSingolaInput,
    db: Session = Depends(get_db),
    utente: Utente = Depends(verifica_permesso("prenotazione:richiedere"))
):
    try:
        prenotazione, _ = crea_prenotazione_singola(db, dati, utente)
        conflitti = ConflittoService.detect_and_record_conflicts(db, prenotazione)
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
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        
        # Foreign key per corso_id
        if 'fk_slot_corso' in error_msg or 'corso_id' in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Il corso con ID {dati.corso_id} non esiste. Verifica l'ID inserito."
            )
        
        # Foreign key per aula_id
        if 'fk_slot_aula' in error_msg or 'aula_id' in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail=f"L'aula con ID {dati.aula_id} non esiste."
            )
        
        # Errore generico di integrità
        raise HTTPException(
            status_code=400,
            detail="Errore nei dati inseriti. Verifica che tutti i riferimenti (corso, aula) esistano."
        )
    except Exception as e:
        db.rollback()
        raise


@router.post("/massiva", response_model=PrenotazioneRisposta, status_code=201,
             summary="Crea Prenotazione massiva")
def nuova_prenotazione_massiva(
    dati: PrenotazioneMassivaInput,
    db: Session = Depends(get_db),
    utente: Utente = Depends(verifica_permesso("prenotazione:richiedere"))
):
    try:
        prenotazione, _ = crea_prenotazione_massiva(db, dati, utente)
        conflitti = ConflittoService.detect_and_record_conflicts(db, prenotazione)
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
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        
        # Foreign key per corso_id
        if 'fk_slot_corso' in error_msg or 'corso_id' in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Il corso con ID {dati.corso_id} non esiste. Verifica l'ID inserito."
            )
        
        # Foreign key per aula_id
        if 'fk_slot_aula' in error_msg or 'aula_id' in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail=f"L'aula con ID {dati.aula_id} non esiste."
            )
        
        # Errore generico di integrità
        raise HTTPException(
            status_code=400,
            detail="Errore nei dati inseriti. Verifica che tutti i riferimenti (corso, aula) esistano."
        )
    except Exception as e:
        db.rollback()
        raise


@router.get("/slot-liberi/{aula_id}", summary="Slot liberi per aula")
def slot_liberi(
    aula_id: int,
    data_dal: date,
    data_al: date,
    db: Session = Depends(get_db),
    _: Utente = Depends(verifica_permesso("aula:vedere_slot_liberi"))
):
    slot_occupati = (
        db.query(SlotOrario)
        .join(Prenotazione)
        .filter(
            SlotOrario.aula_id == aula_id,
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


@router.get("/", response_model=list[PrenotazioneRisposta],
            summary="Lista prenotazioni")
def lista_prenotazioni(
    sede_id:  Optional[int]              = None,
    corso_id: Optional[int]              = None,
    stato:    Optional[StatoPrenotazione] = None,
    data_dal: Optional[date]             = None,
    data_al:  Optional[date]             = None,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    query = db.query(Prenotazione).options(
        joinedload(Prenotazione.richiesta),
        joinedload(Prenotazione.slots),
    )

    if stato:
        query = query.filter(Prenotazione.stato == stato)

    if sede_id or corso_id or data_dal or data_al:
        slot_subq = db.query(SlotOrario.prenotazione_id)
        if sede_id:
            slot_subq = slot_subq.join(Aula, SlotOrario.aula_id == Aula.id)\
                                  .filter(Aula.sede_id == sede_id)
        if corso_id:
            slot_subq = slot_subq.filter(SlotOrario.corso_id == corso_id)
        if data_dal:
            slot_subq = slot_subq.filter(SlotOrario.data >= data_dal)
        if data_al:
            slot_subq = slot_subq.filter(SlotOrario.data <= data_al)
        query = query.filter(Prenotazione.id.in_(slot_subq))

    return query.order_by(Prenotazione.data_creazione.desc()).all()


@router.get("/{prenotazione_id}", response_model=PrenotazioneRisposta,
            summary="Dettaglio prenotazione")
def dettaglio_prenotazione(
    prenotazione_id: int,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
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
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return p


@router.delete("/{prenotazione_id}", status_code=200,
               summary="Elimina prenotazione")
def elimina_prenotazione(
    prenotazione_id: int,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    prenotazione = db.query(Prenotazione).filter(
        Prenotazione.id == prenotazione_id
    ).first()
    if not prenotazione:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    if utente.ruolo != RuoloUtente.COORDINAMENTO:
        if prenotazione.richiedente_id != utente.id:
            raise HTTPException(status_code=403,
                detail="Non hai i permessi per eliminare questa prenotazione")
    richiesta = db.query(RichiestaPrenotazione).filter(
        RichiestaPrenotazione.prenotazione_id == prenotazione_id
    ).first()
    if richiesta:
        db.delete(richiesta)
    db.delete(prenotazione)
    db.commit()
    return {"message": f"Prenotazione {prenotazione_id} eliminata con successo"}


@router.patch("/{prenotazione_id}/slots/{slot_id}", response_model=PrenotazioneRisposta,
              summary="Modifica singolo slot")
def modifica_slot(
    prenotazione_id: int,
    slot_id: int,
    dati: SlotModificaInput,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    """
    Modifica un singolo slot. Tutti i campi (aula, corso, note, data, orario)
    sono ora slot-level — ogni slot è indipendente.
    """
    prenotazione = (
        db.query(Prenotazione)
        .options(joinedload(Prenotazione.slots), joinedload(Prenotazione.richiesta))
        .filter(Prenotazione.id == prenotazione_id)
        .first()
    )
    if not prenotazione:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    if utente.ruolo != RuoloUtente.COORDINAMENTO:
        if prenotazione.richiedente_id != utente.id:
            raise HTTPException(status_code=403,
                detail="Non hai i permessi per modificare questa prenotazione")

    slot = db.query(SlotOrario).filter(
        SlotOrario.id == slot_id,
        SlotOrario.prenotazione_id == prenotazione_id,
    ).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot non trovato")
    if slot.annullato:
        raise HTTPException(status_code=400, detail="Impossibile modificare uno slot annullato")

    if dati.aula_id    is not None: slot.aula_id    = dati.aula_id
    if dati.corso_id   is not None: slot.corso_id   = dati.corso_id
    if dati.note       is not None: slot.note       = dati.note
    if dati.data       is not None: slot.data       = dati.data
    if dati.ora_inizio is not None: slot.ora_inizio = dati.ora_inizio
    if dati.ora_fine   is not None: slot.ora_fine   = dati.ora_fine

    db.flush()

    # Chiudi i conflitti esistenti su questo slot prima di ricalcolare
    conflitti_esistenti = db.query(ConflittoPrenotazione).filter(
        or_(
            ConflittoPrenotazione.slot_id_1 == slot_id,
            ConflittoPrenotazione.slot_id_2 == slot_id,
        ),
        ConflittoPrenotazione.stato_risoluzione == None
    ).all()

    altre_pren_ids = set()
    for cf in conflitti_esistenti:
        altra_id = (
            cf.prenotazione_id_2
            if cf.prenotazione_id_1 == prenotazione_id
            else cf.prenotazione_id_1
        )
        altre_pren_ids.add(altra_id)
        cf.stato_risoluzione = StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_1
        cf.risolto_il = datetime.now(timezone.utc)
        cf.note_risoluzione = "Chiuso automaticamente per modifica slot"

    db.flush()

    # ── CHIAVE: expire_all + re-fetch ─────────────────────────────────────────
    # joinedload cacha i relationship in memoria — dopo flush() i valori
    # degli slot sono aggiornati nel DB ma NON nella collection Python.
    # expire_all() invalida tutta la cache della sessione, il re-fetch
    # rilegge tutto dal DB con i valori aggiornati.
    db.expire_all()
    prenotazione = (
        db.query(Prenotazione)
        .options(joinedload(Prenotazione.slots), joinedload(Prenotazione.richiesta))
        .filter(Prenotazione.id == prenotazione_id)
        .first()
    )

    # Ricalcola conflitti con i nuovi dati dello slot
    conflitti = ConflittoService.detect_and_record_conflicts(db, prenotazione)
    if prenotazione.richiesta:
        prenotazione.richiesta.ha_conflitti = len(conflitti) > 0

    for altra_pren_id in altre_pren_ids:
        ConflittoService._aggiorna_flag_conflitti(db, altra_pren_id)

    db.commit()
    db.refresh(prenotazione)
    return prenotazione


@router.delete("/{prenotazione_id}/slots/{slot_id}", status_code=200,
               summary="Annulla singolo slot di una prenotazione massiva")
def annulla_slot(
    prenotazione_id: int,
    slot_id: int,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    prenotazione = (
        db.query(Prenotazione)
        .options(joinedload(Prenotazione.slots), joinedload(Prenotazione.richiesta))
        .filter(Prenotazione.id == prenotazione_id)
        .first()
    )
    if not prenotazione:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    if utente.ruolo != RuoloUtente.COORDINAMENTO:
        if prenotazione.richiedente_id != utente.id:
            raise HTTPException(status_code=403,
                detail="Non hai i permessi per modificare questa prenotazione")

    slot = db.query(SlotOrario).filter(
        SlotOrario.id == slot_id,
        SlotOrario.prenotazione_id == prenotazione_id,
    ).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot non trovato")
    if slot.annullato:
        raise HTTPException(status_code=400, detail="Slot già annullato")

    slot.annullato = True
    db.flush()

    # ← RACCOGLI CONFLITTI UNICI e altre prenotazioni coinvolte
    conflitti_slot = db.query(ConflittoPrenotazione).filter(
        or_(
            ConflittoPrenotazione.slot_id_1 == slot_id,
            ConflittoPrenotazione.slot_id_2 == slot_id,
        ),
        ConflittoPrenotazione.stato_risoluzione == None
    ).all()

    # ← TRACCIA QUALI CONFLITTI HAI GIÀ PROCESSATO (per evitare duplicati)
    conflitti_processati = set()
    altre_pren_ids = set()

    for cf in conflitti_slot:
        # ← SALTA SE GIÀ PROCESSATO (prevenzione StaleDataError)
        if cf.id in conflitti_processati:
            continue
        
        conflitti_processati.add(cf.id)
        
        # Determina l'altra prenotazione coinvolta
        altra_id = (
            cf.prenotazione_id_2
            if cf.prenotazione_id_1 == prenotazione_id
            else cf.prenotazione_id_1
        )
        altre_pren_ids.add(altra_id)
        
        # Risolvi il conflitto
        cf.stato_risoluzione = (
            StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_2
            if cf.slot_id_1 == slot_id
            else StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_1
        )
        cf.risolto_il = datetime.now(timezone.utc)

    # ← FLUSH UNA SOLA VOLTA dopo aver processato tutti i conflitti
    db.flush()

    # ← AGGIORNA FLAG CONFLITTI PER LE ALTRE PRENOTAZIONI
    for altra_pren_id in altre_pren_ids:
        ConflittoService._aggiorna_flag_conflitti(db, altra_pren_id)

    slot_attivi = [s for s in prenotazione.slots if not s.annullato]

    if not slot_attivi:
        richiesta = db.query(RichiestaPrenotazione).filter(
            RichiestaPrenotazione.prenotazione_id == prenotazione_id
        ).first()
        if richiesta:
            db.delete(richiesta)
        db.delete(prenotazione)
        db.commit()
        return {
            "message": f"Slot {slot_id} annullato. Prenotazione {prenotazione_id} eliminata.",
            "prenotazione_eliminata": True,
        }

    conflitti = ConflittoService.detect_and_record_conflicts(db, prenotazione)
    if prenotazione.richiesta:
        prenotazione.richiesta.ha_conflitti = len(conflitti) > 0

    db.commit()
    return {
        "message": f"Slot {slot_id} annullato.",
        "prenotazione_eliminata": False,
        "slot_attivi_rimasti": len(slot_attivi),
        "prenotazione_id": prenotazione_id,
    }