"""Schema Pydantic per autenticazione e token JWT."""

from pydantic import BaseModel, EmailStr
from backend.models.enums import RuoloUtente


class LoginRequest(BaseModel):
    """Dati di accesso inviati dal client."""
    username: EmailStr  # Usiamo l'email come username
    password: str


class TokenResponse(BaseModel):
    """Risposta con il token JWT dopo il login."""
    access_token: str
    token_type:   str = "bearer"
    ruolo:        RuoloUtente
    nome:         str
    cognome:      str
    email:        str
    sede_id:      int | None = None


class TokenPayload(BaseModel):
    """Struttura del payload del token JWT."""
    sub:   str          # Email dell'utente
    ruolo: RuoloUtente
    exp:   int | None = None