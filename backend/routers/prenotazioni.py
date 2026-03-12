"""
Router per la gestione delle prenotazioni aule - Sistema 2 RUOLI
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
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


@router.post("/massiva", response_model=PrenotazioneRisposta, status_code=201,
             summary="Crea Prenotazione massiva")
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

    if sede_id:
        query = query.join(Aula).filter(Aula.sede_id == sede_id)

    if corso_id:
        query = query.filter(Prenotazione.corso_id == corso_id)

    if stato:
        query = query.filter(Prenotazione.stato == stato)

    # FIX: filtro date tramite subquery invece di join diretto.
    # Il join diretto su SlotOrario interferisce con joinedload(Prenotazione.slots)
    # producendo duplicati o risultati incompleti (prenotazioni con slot nel range
    # non restituite correttamente). La subquery filtra per id senza toccare il join.
    if data_dal or data_al:
        slot_subq = db.query(SlotOrario.prenotazione_id)
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
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")

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
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")

    if utente.ruolo != RuoloUtente.COORDINAMENTO:
        if prenotazione.richiedente_id != utente.id:
            raise HTTPException(
                status_code=403,
                detail="Non hai i permessi per eliminare questa prenotazione"
            )

    richiesta = db.query(RichiestaPrenotazione).filter(
        RichiestaPrenotazione.prenotazione_id == prenotazione_id
    ).first()
    if richiesta:
        db.delete(richiesta)

    db.delete(prenotazione)
    db.commit()

    return {"message": f"Prenotazione {prenotazione_id} eliminata con successo"}


@router.delete("/{prenotazione_id}/slots/{slot_id}", status_code=200,
               summary="Annulla singolo slot di una prenotazione massiva")
def annulla_slot(
    prenotazione_id: int,
    slot_id: int,
    db: Session = Depends(get_db),
    utente: Utente = Depends(get_utente_corrente)
):
    """
    Annulla un singolo slot di una prenotazione massiva.

    - Imposta slot.annullato = True (non cancella la riga)
    - Se era l'ultimo slot attivo, elimina l'intera prenotazione
    - Ricalcola ha_conflitti sulla prenotazione dopo l'annullamento
    - OPERATIVO: solo proprie prenotazioni
    - COORDINAMENTO: qualsiasi
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
        raise HTTPException(status_code=400, detail="Slot già annullato")

    slot.annullato = True
    db.flush()

    # Risolvi automaticamente i conflitti NON_RISOLTO che coinvolgevano questo slot.
    # detect_and_record_conflicts non chiude i conflitti esistenti — va fatto esplicitamente.
    from backend.models.conflitto import ConflittoPrenotazione
    from backend.models.enums import StatoRisoluzioneConflitto

    conflitti_slot = db.query(ConflittoPrenotazione).filter(
        or_(
            ConflittoPrenotazione.slot_id_1 == slot_id,
            ConflittoPrenotazione.slot_id_2 == slot_id,
        ),
        ConflittoPrenotazione.stato_risoluzione == None  # attivi = NULL
    ).all()

    for cf in conflitti_slot:
        # RISOLTO_MANTENUTA_1 = teniamo prenotazione 1 → slot_2 è quello annullato
        # RISOLTO_MANTENUTA_2 = teniamo prenotazione 2 → slot_1 è quello annullato
        cf.stato_risoluzione = (
            StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_2
            if cf.slot_id_1 == slot_id
            else StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_1
        )
        cf.risolto_il = datetime.now(timezone.utc)

    db.flush()

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
            "message": f"Slot {slot_id} annullato. Prenotazione {prenotazione_id} eliminata (nessun slot rimasto).",
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
    """
    prenotazione = db.query(Prenotazione).filter(
        Prenotazione.id == prenotazione_id
    ).first()

    if not prenotazione:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")

    if utente.ruolo != RuoloUtente.COORDINAMENTO:
        if prenotazione.richiedente_id != utente.id:
            raise HTTPException(
                status_code=403,
                detail="Non hai i permessi per modificare questa prenotazione"
            )

    if prenotazione.tipo.value != "singola":
        raise HTTPException(
            status_code=400,
            detail="Puoi modificare solo prenotazioni singole"
        )

    prenotazione.aula_id = dati.aula_id
    prenotazione.corso_id = dati.corso_id
    prenotazione.note = dati.note

    db.query(SlotOrario).filter(
        SlotOrario.prenotazione_id == prenotazione_id
    ).delete()

    nuovo_slot = SlotOrario(
        prenotazione_id=prenotazione.id,
        data=dati.slot.data,
        ora_inizio=dati.slot.ora_inizio,
        ora_fine=dati.slot.ora_fine
    )
    db.add(nuovo_slot)
    db.flush()

    conflitti = ConflittoService.detect_and_record_conflicts(db, prenotazione)

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