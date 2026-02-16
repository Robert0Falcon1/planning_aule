"""Schema Pydantic per la gestione degli utenti."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from backend.models.enums import RuoloUtente


class UtenteBase(BaseModel):
    nome:     str
    cognome:  str
    email:    EmailStr
    ruolo:    RuoloUtente
    sede_id:  Optional[int] = None


class UtenteCrea(UtenteBase):
    """Schema per la creazione di un nuovo utente."""
    password: str


class UtenteRisposta(UtenteBase):
    """Schema per la restituzione dei dati utente (senza password)."""
    id:             int
    attivo:         bool
    data_creazione: datetime

    class Config:
        from_attributes = True