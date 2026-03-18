"""
Configurazione della connessione al database tramite SQLAlchemy.
Gestisce il motore, la sessione e la base dichiarativa dei modelli.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config import settings


# ── Creazione del motore SQLAlchemy ──────────────────────────────────────────
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={
        "charset": "utf8mb4",
        "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
    },
)


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