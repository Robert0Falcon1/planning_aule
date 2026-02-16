"""
Servizio per il rilevamento dei conflitti tra prenotazioni.
Implementa la logica di overlap degli slot orari e verifica capienza.
"""

from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from backend.models.prenotazione import Prenotazione, Conflitto
from backend.models.slot_orario import SlotOrario
from backend.models.aula import Aula
from backend.models.sede import Sede
from backend.models.enums import StatoPrenotazione, TipoConflitto


def rileva_conflitti_slot(
    db: Session,
    aula_id: int,
    slots_nuovi: list[dict],
    escludi_prenotazione_id: int | None = None
) -> list[dict]:
    """
    Verifica se i nuovi slot si sovrappongono con prenotazioni esistenti.

    Args:
        db:                     Sessione database
        aula_id:                ID dell'aula da verificare
        slots_nuovi:            Lista di dict con chiavi: data, ora_inizio, ora_fine
        escludi_prenotazione_id: ID prenotazione da escludere (per aggiornamenti)

    Returns:
        Lista di conflitti trovati come dict con dettagli
    """
    conflitti_trovati = []

    for slot in slots_nuovi:
        # Query per trovare slot sovrapposti nella stessa aula nella stessa data
        query = (
            db.query(SlotOrario)
            .join(Prenotazione)
            .filter(
                Prenotazione.aula_id == aula_id,
                Prenotazione.stato.in_([
                    StatoPrenotazione.CONFERMATA,
                    StatoPrenotazione.IN_ATTESA,
                    StatoPrenotazione.CONFLITTO,
                ]),
                SlotOrario.data == slot["data"],
                SlotOrario.annullato == False,
                # Condizione di sovrapposizione: A.inizio < B.fine AND B.inizio < A.fine
                SlotOrario.ora_inizio < slot["ora_fine"],
                slot["ora_inizio"] < SlotOrario.ora_fine,
            )
        )

        # Esclude la prenotazione corrente (per aggiornamenti)
        if escludi_prenotazione_id:
            query = query.filter(
                Prenotazione.id != escludi_prenotazione_id
            )

        slot_sovrapposti = query.all()

        for s in slot_sovrapposti:
            conflitti_trovati.append({
                "tipo": TipoConflitto.SOVRAPPOSIZIONE_SLOT,
                "prenotazione_conflitta_id": s.prenotazione_id,
                "descrizione": (
                    f"Sovrapposizione il {slot['data']} tra "
                    f"{slot['ora_inizio']} - {slot['ora_fine']} e "
                    f"{s.ora_inizio} - {s.ora_fine} "
                    f"(prenotazione #{s.prenotazione_id})"
                )
            })

    return conflitti_trovati


def verifica_capienza_sede(
    db: Session,
    sede_id: int,
    data: date,
    ora_inizio,
    ora_fine,
    num_partecipanti: int
) -> dict | None:
    """
    Verifica che la capienza massima della sede non venga superata.

    Returns:
        Dict con dettagli del conflitto se la capienza è superata, None altrimenti
    """
    sede = db.query(Sede).filter(Sede.id == sede_id).first()
    if not sede or sede.capienza_massima == 0:
        return None  # Nessun limite configurato

    # Somma i partecipanti delle prenotazioni confermate nello stesso orario
    partecipanti_presenti = (
        db.query(Prenotazione)
        .join(SlotOrario)
        .join(Aula)
        .filter(
            Aula.sede_id == sede_id,
            Prenotazione.stato == StatoPrenotazione.CONFERMATA,
            SlotOrario.data == data,
            SlotOrario.annullato == False,
            SlotOrario.ora_inizio < ora_fine,
            ora_inizio < SlotOrario.ora_fine,
        )
        .with_entities(Prenotazione.corso_id)
        .all()
    )

    # Calcola totale partecipanti (semplificato: usa i corsi associati)
    totale = sum([1 for _ in partecipanti_presenti]) * 20  # Stima conservativa

    if totale + num_partecipanti > sede.capienza_massima:
        return {
            "tipo": TipoConflitto.CAPIENZA_SUPERATA,
            "descrizione": (
                f"La capienza massima della sede ({sede.capienza_massima} persone) "
                f"potrebbe essere superata il {data} "
                f"dalle {ora_inizio} alle {ora_fine}."
            )
        }
    return None