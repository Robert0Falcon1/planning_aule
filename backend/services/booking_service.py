"""
Servizio principale per la gestione delle prenotazioni - Sistema 2 RUOLI
"""

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from backend.models.prenotazione import (Prenotazione, PrenotazioneSingola,
                                          PrenotazioneMassiva, RichiestaPrenotazione)
from backend.models.slot_orario import SlotOrario
from backend.models.utente import Utente
from backend.models.enums import (StatoPrenotazione, StatoRichiesta, TipoRicorrenza)
from backend.schemas.prenotazione import (PrenotazioneSingolaInput, PrenotazioneMassivaInput)


def crea_prenotazione_singola(
    db: Session,
    dati: PrenotazioneSingolaInput,
    utente: Utente
) -> tuple[PrenotazioneSingola, None]:
    prenotazione = PrenotazioneSingola(
        richiedente_id=utente.id,
        stato=StatoPrenotazione.CONFERMATA,
    )
    db.add(prenotazione)
    db.flush()

    slot = SlotOrario(
        prenotazione_id=prenotazione.id,
        aula_id=dati.aula_id,
        corso_id=dati.corso_id,
        note=dati.note,
        data=dati.slot.data,
        ora_inizio=dati.slot.ora_inizio,
        ora_fine=dati.slot.ora_fine,
    )
    db.add(slot)
    db.flush()
    return prenotazione, None


def genera_date_ricorrenza(
    data_inizio: date,
    data_fine: date,
    tipo: TipoRicorrenza,
    giorni_settimana: list[int],
) -> list[date]:
    """
    Genera tutte le date di una prenotazione ricorrente.
    isoweekday(): 1=lunedì … 7=domenica
    """
    date_generate = []
    corrente = data_inizio

    while corrente <= data_fine:
        if corrente.isoweekday() in giorni_settimana:
            date_generate.append(corrente)

        if tipo == TipoRicorrenza.MENSILE:
            corrente += relativedelta(months=1)
        else:
            corrente += timedelta(days=1)

    if tipo == TipoRicorrenza.BISETTIMANALE:
        prima_settimana = data_inizio.isocalendar()[1]
        date_generate = [
            d for d in date_generate
            if (d.isocalendar()[1] - prima_settimana) % 2 == 0
        ]

    return date_generate


def crea_prenotazione_massiva(
    db: Session,
    dati: PrenotazioneMassivaInput,
    utente: Utente
) -> tuple[PrenotazioneMassiva, None]:
    """
    Crea una prenotazione massiva generando tutti gli slot ricorrenti.
    Sistema 2 ruoli: stato CONFERMATA immediato.
    """
    prenotazione = PrenotazioneMassiva(
        richiedente_id=utente.id,
        stato=StatoPrenotazione.CONFERMATA,
        tipo_ricorrenza=dati.tipo_ricorrenza,
        giorni_settimana=",".join(map(str, dati.giorni_settimana)),
        data_inizio_range=dati.data_inizio,
        data_fine_range=dati.data_fine,
    )
    db.add(prenotazione)
    db.flush()

    date_ricorrenti = genera_date_ricorrenza(
        dati.data_inizio,
        dati.data_fine,
        dati.tipo_ricorrenza,
        dati.giorni_settimana,
    )

    for d in date_ricorrenti:
        slot = SlotOrario(
            prenotazione_id=prenotazione.id,
            aula_id=dati.aula_id,
            corso_id=dati.corso_id,
            note=dati.note,
            data=d,
            ora_inizio=dati.ora_inizio,
            ora_fine=dati.ora_fine,
        )
        db.add(slot)

    db.flush()
    return prenotazione, None