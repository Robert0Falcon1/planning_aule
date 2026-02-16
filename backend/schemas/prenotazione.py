"""Schema Pydantic per la gestione delle prenotazioni."""

from pydantic import BaseModel, field_validator
from datetime import date, time, datetime
from typing import Optional, List
from backend.models.enums import (StatoPrenotazione, TipoPrenotazione,
                                   TipoRicorrenza, StatoRichiesta)


class SlotOrarioSchema(BaseModel):
    data:       date
    ora_inizio: time
    ora_fine:   time

    @field_validator("ora_fine")
    @classmethod
    def ora_fine_dopo_inizio(cls, v, info):
        if "ora_inizio" in info.data and v <= info.data["ora_inizio"]:
            raise ValueError("L'ora di fine deve essere successiva all'ora di inizio")
        return v

    class Config:
        from_attributes = True


class PrenotazioneSingolaInput(BaseModel):
    """Input per creare una prenotazione singola."""
    aula_id:    int
    corso_id:   int
    slot:       SlotOrarioSchema
    note:       Optional[str] = None


class PrenotazioneMassivaInput(BaseModel):
    """Input per creare una prenotazione massiva (ricorrente)."""
    aula_id:         int
    corso_id:        int
    data_inizio:     date
    data_fine:       date
    ora_inizio:      time
    ora_fine:        time
    tipo_ricorrenza: TipoRicorrenza
    giorni_settimana: List[int]  # Es: [1, 3, 5] per Lun/Mer/Ven (1=lunedì, 7=domenica)
    note:            Optional[str] = None

    @field_validator("giorni_settimana")
    @classmethod
    def valida_giorni(cls, v):
        if not all(1 <= g <= 7 for g in v):
            raise ValueError("I giorni della settimana devono essere tra 1 (lunedì) e 7 (domenica)")
        return sorted(set(v))


class PrenotazioneRisposta(BaseModel):
    """Schema di risposta per una prenotazione."""
    id:             int
    tipo:           TipoPrenotazione
    aula_id:        int
    corso_id:       int
    richiedente_id: int
    stato:          StatoPrenotazione
    note:           Optional[str]
    data_creazione: datetime
    slots:          List[SlotOrarioSchema] = []

    class Config:
        from_attributes = True


class RichiestaPrenotazioneRisposta(BaseModel):
    """Schema di risposta per una richiesta di prenotazione."""
    id:             int
    prenotazione_id: int
    stato:          StatoRichiesta
    ha_conflitti:   bool
    data_richiesta: datetime
    note_rifiuto:   Optional[str] = None

    class Config:
        from_attributes = True