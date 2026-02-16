"""
Router per l'autenticazione: login e informazioni sull'utente corrente.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.core.security import verifica_password, crea_access_token
from backend.core.dependencies import get_utente_corrente
from backend.models.utente import Utente
from backend.schemas.auth import TokenResponse
from backend.schemas.utente import UtenteRisposta

router = APIRouter(prefix="/auth", tags=["Autenticazione"])


@router.post("/login", response_model=TokenResponse, summary="Login utente")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autentica un utente e restituisce un token JWT.
    - **username**: email dell'utente
    - **password**: password in chiaro
    """
    # Cerca l'utente per email
    utente = db.query(Utente).filter(Utente.email == form_data.username).first()

    # Verifica credenziali (messaggio generico per sicurezza)
    if not utente or not verifica_password(form_data.password, utente.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password non corretti",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not utente.attivo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account disattivato"
        )

    # Aggiorna l'ultimo accesso
    utente.ultimo_accesso = datetime.utcnow()
    db.commit()

    # Genera il token JWT con email e ruolo nel payload
    token = crea_access_token(dati={
        "sub":   utente.email,
        "ruolo": utente.ruolo.value,
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        ruolo=utente.ruolo,
        nome=utente.nome,
        cognome=utente.cognome,
        email=utente.email,
        sede_id=utente.sede_id,
    )


@router.get("/me", response_model=UtenteRisposta, summary="Profilo utente corrente")
def get_me(utente: Utente = Depends(get_utente_corrente)):
    """Restituisce i dati dell'utente autenticato tramite il token JWT."""
    return utente