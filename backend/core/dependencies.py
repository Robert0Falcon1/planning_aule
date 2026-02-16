"""
Dipendenze FastAPI condivise tra i router.
Gestisce l'autenticazione JWT e il controllo dei permessi RBAC.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.core.security import decodifica_token
from backend.core.permissions import ha_permesso
from backend.models.utente import Utente
from backend.models.enums import RuoloUtente

# Schema OAuth2: il token viene estratto dall'header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_utente_corrente(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Utente:
    """
    Dipendenza che estrae e valida l'utente dal token JWT.
    Da usare come Depends() negli endpoint protetti.

    Raises:
        HTTPException 401: Se il token è assente, malformato o scaduto
        HTTPException 403: Se l'utente è disattivato
    """
    credenziali_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenziali non valide o token scaduto",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decodifica il token JWT
    payload = decodifica_token(token)
    if payload is None:
        raise credenziali_exception

    # Estrae l'email dal campo "sub" del payload
    email: str = payload.get("sub")
    if email is None:
        raise credenziali_exception

    # Cerca l'utente nel database
    utente = db.query(Utente).filter(Utente.email == email).first()
    if utente is None:
        raise credenziali_exception

    # Verifica che l'account sia attivo
    if not utente.attivo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account disattivato. Contattare l'amministratore."
        )

    return utente


def verifica_permesso(azione: str):
    """
    Factory di dipendenze FastAPI per il controllo RBAC.

    Uso negli endpoint:
        @router.post("/prenotazioni")
        def crea(utente = Depends(verifica_permesso("prenotazione:richiedere"))):
            ...
    """
    def _dipendenza(utente: Utente = Depends(get_utente_corrente)) -> Utente:
        if not ha_permesso(utente.ruolo, azione):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permesso negato. Ruolo '{utente.ruolo}' "
                       f"non autorizzato per '{azione}'."
            )
        return utente
    return _dipendenza