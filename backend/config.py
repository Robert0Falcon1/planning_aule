"""
Configurazione centralizzata dell'applicazione.
Legge le variabili d'ambiente dal file .env
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Impostazioni dell'applicazione caricate da variabili d'ambiente."""

    # Configurazione JWT
    secret_key: str = "chiave_di_fallback_solo_per_sviluppo"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    # Configurazione Database
    database_url: str = "sqlite:///./prenotazione_aule.db"

    # Informazioni applicazione
    app_name: str = "Sistema Prenotazione Aule"
    app_version: str = "1.0.0"
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Restituisce l'istanza singleton delle impostazioni (cached)."""
    return Settings()


# Istanza globale delle impostazioni
settings = get_settings()