"""
Modello ORM per i corsi gestiti dall'Agenzia Formativa.
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import TipoFinanziamento


class Corso(Base):
    """Corso formativo organizzato dall'Agenzia."""

    __tablename__ = "corsi"

    # ── Colonne ──────────────────────────────────────────────────────────────
    id                 = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codice             = Column(String(50), unique=True, nullable=False, index=True)
    titolo             = Column(String(255), nullable=False)
    tipo_finanziamento = Column(SAEnum(TipoFinanziamento), nullable=False)
    responsabile_id    = Column(Integer, ForeignKey("utenti.id"), nullable=False)
    num_partecipanti   = Column(Integer, nullable=False, default=1)
    data_inizio        = Column(Date, nullable=False)
    data_fine          = Column(Date, nullable=False)
    descrizione        = Column(String(1000), nullable=True)
    attivo             = Column(Integer, default=1)
    data_creazione     = Column(DateTime, default=datetime.utcnow)

    # ── Relazioni ─────────────────────────────────────────────────────────────
    # back_populates="corsi" corrisponde a Utente.corsi definito nella classe base
    responsabile = relationship(
        "Utente",
        back_populates="corsi",
        foreign_keys=[responsabile_id]
    )

    prenotazioni = relationship(
        "Prenotazione",
        back_populates="corso"
    )

    def is_attivo(self) -> bool:
        """Restituisce True se il corso è nel periodo di svolgimento."""
        return self.data_inizio <= date.today() <= self.data_fine

    def __repr__(self) -> str:
        return f"<Corso {self.codice} - {self.titolo}>"
