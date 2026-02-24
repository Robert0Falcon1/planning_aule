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

    # Configurazione Database (campi individuali da .env)
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "prenotazione_aule"
    db_user: str = "root"
    db_password: str = ""

    # Informazioni applicazione
    app_name: str = "Sistema Prenotazione Aule"
    app_version: str = "1.0.0"
    debug: bool = True

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()