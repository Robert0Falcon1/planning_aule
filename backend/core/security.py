"""
Gestione della sicurezza: hashing password e generazione/verifica token JWT.
Usa bcrypt direttamente (senza passlib) per compatibilità con bcrypt >= 4.0.
"""

from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from backend.config import settings


def hash_password(password: str) -> str:
    """
    Genera l'hash bcrypt di una password in chiaro.
    Codifica la stringa in bytes prima di passarla a bcrypt.
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verifica_password(password_chiaro: str, password_hash: str) -> bool:
    """
    Confronta una password in chiaro con il suo hash bcrypt.
    Entrambi i valori vengono codificati in bytes per la verifica.
    """
    try:
        return bcrypt.checkpw(
            password_chiaro.encode("utf-8"),
            password_hash.encode("utf-8")
        )
    except Exception:
        return False


def crea_access_token(dati: dict, scadenza: Optional[timedelta] = None) -> str:
    """
    Genera un token JWT firmato con i dati forniti.

    Args:
        dati:     Payload da includere nel token (es: {"sub": "email@example.com"})
        scadenza: Durata del token (usa il default da settings se None)

    Returns:
        Token JWT come stringa
    """
    payload = dati.copy()

    # Calcola la data di scadenza
    if scadenza:
        expire = datetime.utcnow() + scadenza
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    payload.update({"exp": expire, "iat": datetime.utcnow()})

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decodifica_token(token: str) -> Optional[dict]:
    """
    Decodifica e verifica un token JWT.

    Returns:
        Il payload del token se valido, None altrimenti
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None