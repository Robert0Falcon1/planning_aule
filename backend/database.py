"""
Configurazione della connessione al database tramite SQLAlchemy.
Gestisce il motore, la sessione e la base dichiarativa dei modelli.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config import settings


# ── Creazione del motore SQLAlchemy ──────────────────────────────────────────
# connect_args è necessario solo per SQLite per abilitare i foreign key
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # Solo per SQLite
    echo=settings.debug,  # Logga le query SQL in modalità debug
)


# ── Abilitazione Foreign Keys in SQLite ──────────────────────────────────────
@event.listens_for(engine, "connect")
def abilita_foreign_keys(dbapi_connection, connection_record):
    """SQLite disabilita i FK per default: questa funzione li abilita ad ogni connessione."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# ── Factory della sessione ────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ── Base dichiarativa per i modelli ORM ──────────────────────────────────────
class Base(DeclarativeBase):
    """Classe base da cui ereditano tutti i modelli SQLAlchemy."""
    pass


def get_db():
    """
    Dependency injector per FastAPI.
    Fornisce una sessione DB per ogni richiesta e la chiude al termine.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def crea_tabelle():
    """Crea tutte le tabelle nel database se non esistono già."""
    Base.metadata.create_all(bind=engine)