"""
Dipendenze FastAPI condivise tra i router.
Gestisce l'autenticazione JWT e il controllo dei permessi RBAC.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.core.security import decodifica_token
from backend.core.permissions import PermissionChecker
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
    Versione semplificata per sistema 2 ruoli.
    
    La maggior parte dei controlli è ora gestita direttamente nei router
    tramite PermissionChecker e require_coordinamento.
    """
    def _dipendenza(utente: Utente = Depends(get_utente_corrente)) -> Utente:
        # Mapping azioni → permessi nel nuovo sistema
        if "validare" in azione or "rifiutare" in azione:
            # Solo COORDINAMENTO (vecchie azioni di approvazione/rifiuto)
            if not PermissionChecker.is_coordinamento(utente):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permesso negato: richiesto ruolo COORDINAMENTO"
                )
        elif "richiedere" in azione or "creare" in azione:
            # Tutti possono richiedere/creare prenotazioni
            pass
        elif "vedere" in azione or "visualizzare" in azione:
            # Tutti possono vedere (filtro nei query)
            pass
        else:
            # Default: permetti (controlli specifici nei router)
            pass
        
        return utente
    return _dipendenza

def require_coordinamento(utente: Utente = Depends(get_utente_corrente)):
    """Dependency: richiede ruolo COORDINAMENTO"""
    from backend.core.permissions import PermissionChecker
    
    if not PermissionChecker.is_coordinamento(utente):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accesso negato: richiesto ruolo COORDINAMENTO"
        )
    return utente


# Helper aggiuntivi per compatibilità
GRUPPO_OPERATIVO = [RuoloUtente.OPERATIVO]
GRUPPO_SUPERVISIONE = [RuoloUtente.COORDINAMENTO]