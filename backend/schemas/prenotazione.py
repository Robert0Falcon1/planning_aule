"""Schema Pydantic per la gestione delle prenotazioni."""
from pydantic import BaseModel, field_validator
from datetime import date, time, datetime
from typing import Optional, List
from backend.models.enums import (StatoPrenotazione, TipoPrenotazione,
                                   TipoRicorrenza, StatoRichiesta)

class SlotOrarioSchema(BaseModel):
    """Schema di risposta per un docente."""
    id: Optional[int] = None
    aula_id: int
    corso_id: int
    docente_id: Optional[int] = None  # ← CAMBIATO DA int A Optional[int]
    note: Optional[str] = None
    
    data: date
    ora_inizio: time
    ora_fine: time
    annullato: bool = False
    
    @field_validator("ora_fine")
    @classmethod
    def ora_fine_dopo_inizio(cls, v, info):
        if "ora_inizio" in info.data and v <= info.data["ora_inizio"]:
            raise ValueError("L'ora di fine deve essere successiva all'ora di inizio")
        return v
    
    class Config:
        from_attributes = True
        

class PrenotazioneSingolaInput(BaseModel):
    aula_id:    int
    corso_id:   int
    docente_id: int  # ← AGGIUNTO E OBBLIGATORIO
    slot:       'SlotInputSchema'
    note:       Optional[str] = None


class PrenotazioneMassivaInput(BaseModel):
    aula_id:         int
    corso_id:        int
    docente_id:      int  # ← AGGIUNTO E OBBLIGATORIO
    data_inizio:     date
    data_fine:       date
    ora_inizio:      time
    ora_fine:        time
    tipo_ricorrenza: TipoRicorrenza
    giorni_settimana: List[int]
    note:            Optional[str] = None
    
    @field_validator("giorni_settimana")
    @classmethod
    def valida_giorni(cls, v):
        if not all(1 <= g <= 7 for g in v):
            raise ValueError("I giorni della settimana devono essere tra 1 (lunedì) e 7 (domenica)")
        return sorted(set(v))


class RichiestaEmbedded(BaseModel):
    id:            int
    stato:         StatoRichiesta
    ha_conflitti:  bool
    note_rifiuto:  Optional[str] = None
    data_gestione: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PrenotazioneRisposta(BaseModel):
    """Schema di risposta per una prenotazione."""
    id:             int
    tipo:           TipoPrenotazione
    richiedente_id: int
    stato:          StatoPrenotazione
    data_creazione: datetime
    slots:          List[SlotOrarioSchema] = []
    richiesta:      Optional[RichiestaEmbedded] = None
    
    class Config:
        from_attributes = True


class RichiestaPrenotazioneRisposta(BaseModel):
    id:              int
    prenotazione_id: int
    stato:           StatoRichiesta
    ha_conflitti:    bool
    data_richiesta:  datetime
    note_rifiuto:    Optional[str] = None
    
    class Config:
        from_attributes = True


class SlotInputSchema(BaseModel):
    """Schema per il slot in input (senza aula_id/corso_id/docente_id che stanno nel payload top-level)."""
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