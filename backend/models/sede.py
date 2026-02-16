"""
Modello ORM per le sedi dell'Agenzia Formativa.
Una sede contiene più aule e ha una capienza massima complessiva.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database import Base


class Sede(Base):
    """Sede fisica dell'Agenzia Formativa (es: Via Livorno 49, Torino)."""

    __tablename__ = "sedi"

    # ── Colonne ──────────────────────────────────────────────────────────────
    id                = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome              = Column(String(150), nullable=False)
    indirizzo         = Column(String(255), nullable=False)
    citta             = Column(String(100), nullable=False)
    capienza_massima  = Column(Integer, nullable=False, default=0,
                               comment="Numero massimo di persone contemporaneamente presenti in sede")
    attiva            = Column(Integer, default=1)  # 1=attiva, 0=disattivata

    # ── Relazioni ─────────────────────────────────────────────────────────────
    aule         = relationship("Aula",         back_populates="sede", cascade="all, delete-orphan")
    utenti       = relationship("Utente",       back_populates="sede")
    attrezzature = relationship("Attrezzatura", back_populates="sede", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Sede {self.nome} - {self.citta}>"