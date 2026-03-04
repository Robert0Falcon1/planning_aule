"""
Modello ORM per gli utenti del sistema - Sistema 2 RUOLI
Usa ENUM semplice senza Single Table Inheritance.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import RuoloUtente


class Utente(Base):
    """
    Utente del sistema.
    Sistema 2 ruoli: OPERATIVO + COORDINAMENTO (ENUM semplice).
    """
    __tablename__ = "utenti"

    # ── Colonne ──────────────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cognome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    attivo = Column(Boolean, default=True)
    ruolo = Column(SAEnum(RuoloUtente), nullable=False)
    sede_id = Column(Integer, ForeignKey("sedi.id"), nullable=True)
    data_creazione = Column(DateTime, default=datetime.utcnow, nullable=False)
    ultimo_accesso = Column(DateTime, nullable=True)

    # ── Relazioni ─────────────────────────────────────────────────────────────
    sede = relationship("Sede", back_populates="utenti")
    
    corsi = relationship(
        "Corso",
        back_populates="responsabile",
        foreign_keys="Corso.responsabile_id"
    )
    
    prenotazioni_richieste = relationship(
        "Prenotazione",
        back_populates="richiedente",
        foreign_keys="Prenotazione.richiedente_id"
    )
    
    richieste_gestite = relationship(
        "RichiestaPrenotazione",
        back_populates="segreteria",
        foreign_keys="RichiestaPrenotazione.segreteria_id"
    )
    
    conflitti_risolti = relationship(
        "ConflittoPrenotazione",
        foreign_keys="ConflittoPrenotazione.risolto_da",
        back_populates="risolutore"
    )

    def __repr__(self) -> str:
        return f"<Utente {self.email} [{self.ruolo.value}]>"