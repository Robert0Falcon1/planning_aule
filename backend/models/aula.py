"""
Modello ORM per le aule all'interno di una sede.
Ogni aula ha una capienza e può ospitare prenotazioni.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base


class Aula(Base):
    """Aula fisica all'interno di una sede."""

    __tablename__ = "aule"

    # ── Colonne ──────────────────────────────────────────────────────────────
    id        = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome      = Column(String(100), nullable=False)
    capienza  = Column(Integer, nullable=False, default=20,
                       comment="Numero massimo di partecipanti nell'aula")
    sede_id   = Column(Integer, ForeignKey("sedi.id"), nullable=False)
    note      = Column(String(500), nullable=True)
    attiva    = Column(Integer, default=1)

    # ── Relazioni ─────────────────────────────────────────────────────────────
    sede         = relationship("Sede",        back_populates="aule")
    prenotazioni = relationship("Prenotazione", back_populates="aula")

    def __repr__(self) -> str:
        return f"<Aula {self.nome} (cap. {self.capienza}) - sede {self.sede_id}>"