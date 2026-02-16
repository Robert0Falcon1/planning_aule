"""
Router per la gestione delle prenotazioni aule.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.core.dependencies import get_utente_corrente, verifica_permesso
from backend.models.utente import Utente
from backend.models.prenotazione import (Prenotazione, RichiestaPrenotazione)
from backend.models.slot_orario import SlotOrario
from backend.schemas.prenotazione import (PrenotazioneSingolaInput,
                                           PrenotazioneMassivaInput,
                                           PrenotazioneRisposta,
                                           RichiestaPrenotazioneRisposta)
from backend.services.booking_service import (crea_prenotazione_singola,
                                               crea_prenotazione_massiva,
                                               approva_richiesta,
                                               rifiuta_richiesta)
from backend.models.enums import StatoPrenotazione
from datetime import date
from typing import Optional

router = APIRouter(prefix="/prenotazioni", tags=["Prenotazioni"])


@router.post("/singola", response_model=PrenotazioneRisposta, status_code=201,
             summary="Crea prenotazione singola")
def nuova_prenotazione_singola(
    dati: PrenotazioneSingolaInput,
    db:   Session = Depends(get_db),
    utente: Utente = Depends(verifica_permesso("prenotazione:richiedere"))
):
    """
    Crea una prenotazione singola per un'aula.
    Se esistono conflitti vengono segnalati come WARNING ma la richiesta viene comunque creata.
    """
    prenotazione, _ = crea_prenotazione_singola(db, dati, utente)
    return prenotazione


@router.post("/massiva", response_model=PrenotazioneRisposta, status_code=201,
             summary="Crea prenotazione massiva (ricorrente)")
def nuova_prenotazione_massiva(
    dati: PrenotazioneMassivaInput,
    db:   Session = Depends(get_db),
    utente: Utente = Depends(verifica_permesso("prenotazione:richiedere"))
):
    """
    Crea una prenotazione ricorrente generando automaticamente tutti gli slot.
    Es: tutti i lunedì dalle 9 alle 12 da marzo a giugno.
    """
    prenotazione, _ = crea_prenotazione_massiva(db, dati, utente)
    return prenotazione


@router.get("/", response_model=list[PrenotazioneRisposta],
            summary="Lista prenotazioni")
def lista_prenotazioni(
    sede_id:   Optional[int] = None,
    corso_id:  Optional[int] = None,
    stato:     Optional[StatoPrenotazione] = None,
    data_dal:  Optional[date] = None,
    data_al:   Optional[date] = None,
    db:        Session = Depends(get_db),
    utente:    Utente = Depends(get_utente_corrente)
):
    """
    Restituisce le prenotazioni visibili in base al ruolo dell'utente:
    - ResponsabileCorso: solo le proprie
    - SegreteriaSede/ResponsabileSede: della propria sede
    - SegreteriaDidattica: per i propri corsi
    - Coordinamento: tutte
    """
    from backend.models.enums import RuoloUtente
    from backend.models.aula import Aula

    query = db.query(Prenotazione)

    # Filtri per ruolo (RBAC a livello di dati)
    if utente.ruolo == RuoloUtente.RESPONSABILE_CORSO:
        query = query.filter(Prenotazione.richiedente_id == utente.id)
    elif utente.ruolo in [RuoloUtente.SEGRETERIA_SEDE, RuoloUtente.RESPONSABILE_SEDE]:
        query = (query.join(Aula)
                 .filter(Aula.sede_id == utente.sede_id))
    elif utente.ruolo == RuoloUtente.SEGRETERIA_DIDATTICA:
        query = (query.join(Prenotazione.corso)
                 .filter(Prenotazione.corso.has(
                     responsabile_id=utente.id
                 )))
    # COORDINAMENTO: vede tutto, nessun filtro aggiuntivo

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
    db:     Session = Depends(get_db),
    utente: Utente  = Depends(get_utente_corrente)
):
    """Restituisce il dettaglio di una singola prenotazione."""
    p = db.query(Prenotazione).filter(Prenotazione.id == prenotazione_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return p


@router.post("/richieste/{richiesta_id}/approva",
             response_model=RichiestaPrenotazioneRisposta,
             summary="Approva richiesta")
def approva(
    richiesta_id: int,
    db:     Session = Depends(get_db),
    utente: Utente  = Depends(verifica_permesso("prenotazione:validare"))
):
    """Approva una richiesta di prenotazione (solo Segreteria di Sede)."""
    try:
        return approva_richiesta(db, richiesta_id, utente)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/richieste/{richiesta_id}/rifiuta",
             response_model=RichiestaPrenotazioneRisposta,
             summary="Rifiuta richiesta")
def rifiuta(
    richiesta_id: int,
    motivo: str,
    db:     Session = Depends(get_db),
    utente: Utente  = Depends(verifica_permesso("prenotazione:rifiutare"))
):
    """Rifiuta una richiesta di prenotazione con motivazione."""
    try:
        return rifiuta_richiesta(db, richiesta_id, motivo, utente)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/slot-liberi/{aula_id}", summary="Slot liberi per aula")
def slot_liberi(
    aula_id:   int,
    data_dal:  date,
    data_al:   date,
    db:        Session = Depends(get_db),
    _:         Utente  = Depends(verifica_permesso("aula:vedere_slot_liberi"))
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
            ]),
            SlotOrario.data >= data_dal,
            SlotOrario.data <= data_al,
            SlotOrario.annullato == False,
        )
        .all()
    )
    return [{
        "data":       s.data,
        "ora_inizio": s.ora_inizio,
        "ora_fine":   s.ora_fine,
        "prenotazione_id": s.prenotazione_id,
    } for s in slot_occupati]