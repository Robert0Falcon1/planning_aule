"""
Servizio principale per la gestione delle prenotazioni.
Coordina creazione, validazione, conflitti e stati del workflow.
"""

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from backend.models.prenotazione import (Prenotazione, PrenotazioneSingola,
                                          PrenotazioneMassiva, RichiestaPrenotazione,
                                          Conflitto)
from backend.models.slot_orario import SlotOrario
from backend.models.utente import Utente
from backend.models.enums import (StatoPrenotazione, StatoRichiesta,
                                   TipoRicorrenza, TipoConflitto)
from backend.schemas.prenotazione import (PrenotazioneSingolaInput,
                                           PrenotazioneMassivaInput)
from backend.services.conflict_service import (rileva_conflitti_slot,
                                                verifica_capienza_sede)
from backend.models.aula import Aula


def crea_prenotazione_singola(
    db: Session,
    dati: PrenotazioneSingolaInput,
    utente: Utente
) -> tuple[PrenotazioneSingola, RichiestaPrenotazione]:
    """
    Crea una prenotazione singola con il relativo workflow di richiesta.

    Returns:
        Tupla (prenotazione, richiesta)
    """
    # ── Creazione prenotazione ────────────────────────────────────────────────
    prenotazione = PrenotazioneSingola(
        aula_id=dati.aula_id,
        corso_id=dati.corso_id,
        richiedente_id=utente.id,
        note=dati.note,
        stato=StatoPrenotazione.IN_ATTESA,
    )
    db.add(prenotazione)
    db.flush()  # Ottieni l'ID senza fare commit

    # ── Creazione slot ────────────────────────────────────────────────────────
    slot = SlotOrario(
        prenotazione_id=prenotazione.id,
        data=dati.slot.data,
        ora_inizio=dati.slot.ora_inizio,
        ora_fine=dati.slot.ora_fine,
    )
    db.add(slot)
    db.flush()

    # ── Rilevamento conflitti (warning, non blocco) ────────────────────────────
    slots_da_verificare = [{
        "data": dati.slot.data,
        "ora_inizio": dati.slot.ora_inizio,
        "ora_fine": dati.slot.ora_fine,
    }]
    conflitti_trovati = rileva_conflitti_slot(db, dati.aula_id, slots_da_verificare)

    # ── Creazione richiesta di approvazione ───────────────────────────────────
    richiesta = RichiestaPrenotazione(
        prenotazione_id=prenotazione.id,
        stato=StatoRichiesta.INVIATA,
        ha_conflitti=len(conflitti_trovati) > 0,
    )
    db.add(richiesta)
    db.flush()

    # ── Registrazione conflitti come warning ──────────────────────────────────
    if conflitti_trovati:
        prenotazione.stato = StatoPrenotazione.CONFLITTO
        for c in conflitti_trovati:
            conflitto = Conflitto(
                richiesta_id=richiesta.id,
                prenotazione_conflitta_id=c.get("prenotazione_conflitta_id"),
                tipo=c["tipo"],
                descrizione=c["descrizione"],
            )
            db.add(conflitto)

    db.commit()
    db.refresh(prenotazione)
    db.refresh(richiesta)
    return prenotazione, richiesta


def genera_date_ricorrenza(
    data_inizio: date,
    data_fine: date,
    tipo: TipoRicorrenza,
    giorni_settimana: list[int],
) -> list[date]:
    """
    Genera tutte le date di una prenotazione ricorrente.

    Args:
        data_inizio:     Prima data del range
        data_fine:       Ultima data del range
        tipo:            Tipo di ricorrenza
        giorni_settimana: Lista di giorni (1=lunedì, 7=domenica)

    Returns:
        Lista di date generate
    """
    date_generate = []
    corrente = data_inizio

    while corrente <= data_fine:
        # isoweekday(): 1=lunedì, 7=domenica
        if corrente.isoweekday() in giorni_settimana:
            date_generate.append(corrente)

        # Avanzamento in base al tipo di ricorrenza
        if tipo == TipoRicorrenza.GIORNALIERA:
            corrente += timedelta(days=1)
        elif tipo == TipoRicorrenza.SETTIMANALE:
            corrente += timedelta(days=1)
        elif tipo == TipoRicorrenza.BISETTIMANALE:
            corrente += timedelta(days=1)
        elif tipo == TipoRicorrenza.MENSILE:
            corrente += relativedelta(months=1)
            # Per mensile: salta alle settimane pari
            break  # Semplificazione: mensile gestito separatamente

    return date_generate


def crea_prenotazione_massiva(
    db: Session,
    dati: PrenotazioneMassivaInput,
    utente: Utente
) -> tuple[PrenotazioneMassiva, RichiestaPrenotazione]:
    """
    Crea una prenotazione massiva generando tutti gli slot ricorrenti.

    Returns:
        Tupla (prenotazione, richiesta)
    """
    # ── Creazione prenotazione base ───────────────────────────────────────────
    prenotazione = PrenotazioneMassiva(
        aula_id=dati.aula_id,
        corso_id=dati.corso_id,
        richiedente_id=utente.id,
        note=dati.note,
        stato=StatoPrenotazione.IN_ATTESA,
        tipo_ricorrenza=dati.tipo_ricorrenza,
        giorni_settimana=",".join(map(str, dati.giorni_settimana)),
        data_inizio_range=dati.data_inizio,
        data_fine_range=dati.data_fine,
    )
    db.add(prenotazione)
    db.flush()

    # ── Generazione degli slot ────────────────────────────────────────────────
    date_ricorrenti = genera_date_ricorrenza(
        dati.data_inizio,
        dati.data_fine,
        dati.tipo_ricorrenza,
        dati.giorni_settimana,
    )

    slots_da_verificare = []
    for d in date_ricorrenti:
        slot = SlotOrario(
            prenotazione_id=prenotazione.id,
            data=d,
            ora_inizio=dati.ora_inizio,
            ora_fine=dati.ora_fine,
        )
        db.add(slot)
        slots_da_verificare.append({
            "data": d,
            "ora_inizio": dati.ora_inizio,
            "ora_fine": dati.ora_fine,
        })

    db.flush()

    # ── Rilevamento conflitti ─────────────────────────────────────────────────
    conflitti_trovati = rileva_conflitti_slot(db, dati.aula_id, slots_da_verificare)

    # ── Richiesta di approvazione ─────────────────────────────────────────────
    richiesta = RichiestaPrenotazione(
        prenotazione_id=prenotazione.id,
        stato=StatoRichiesta.INVIATA,
        ha_conflitti=len(conflitti_trovati) > 0,
    )
    db.add(richiesta)
    db.flush()

    if conflitti_trovati:
        prenotazione.stato = StatoPrenotazione.CONFLITTO
        for c in conflitti_trovati:
            conflitto = Conflitto(
                richiesta_id=richiesta.id,
                prenotazione_conflitta_id=c.get("prenotazione_conflitta_id"),
                tipo=c["tipo"],
                descrizione=c["descrizione"],
            )
            db.add(conflitto)

    db.commit()
    db.refresh(prenotazione)
    db.refresh(richiesta)
    return prenotazione, richiesta


def approva_richiesta(
    db: Session,
    richiesta_id: int,
    segreteria: Utente
) -> RichiestaPrenotazione:
    """Approva una richiesta di prenotazione e la conferma."""
    from datetime import datetime
    richiesta = db.query(RichiestaPrenotazione).filter(
        RichiestaPrenotazione.id == richiesta_id
    ).first()
    if not richiesta:
        raise ValueError(f"Richiesta #{richiesta_id} non trovata")

    richiesta.stato = StatoRichiesta.APPROVATA
    richiesta.segreteria_id = segreteria.id
    richiesta.data_gestione = datetime.utcnow()
    richiesta.prenotazione.stato = StatoPrenotazione.CONFERMATA

    db.commit()
    db.refresh(richiesta)
    return richiesta


def rifiuta_richiesta(
    db: Session,
    richiesta_id: int,
    motivo: str,
    segreteria: Utente
) -> RichiestaPrenotazione:
    """Rifiuta una richiesta di prenotazione con un motivo."""
    from datetime import datetime
    richiesta = db.query(RichiestaPrenotazione).filter(
        RichiestaPrenotazione.id == richiesta_id
    ).first()
    if not richiesta:
        raise ValueError(f"Richiesta #{richiesta_id} non trovata")

    richiesta.stato = StatoRichiesta.RIFIUTATA
    richiesta.segreteria_id = segreteria.id
    richiesta.data_gestione = datetime.utcnow()
    richiesta.note_rifiuto = motivo
    richiesta.prenotazione.stato = StatoPrenotazione.RIFIUTATA

    db.commit()
    db.refresh(richiesta)
    return richiesta