"""
Modello ORM per le attrezzature disponibili nelle sedi.
Gestisce le richieste di attrezzatura associate alle prenotazioni.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum, DateTime, Text
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import TipoAttrezzatura, StatoRichiesta


class Attrezzatura(Base):
    """Attrezzatura disponibile in una sede (PC, proiettori, ecc.)."""

    __tablename__ = "attrezzature"

    id                   = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo                 = Column(SAEnum(TipoAttrezzatura), nullable=False)
    descrizione          = Column(String(255), nullable=True)
    quantita_disponibile = Column(Integer, nullable=False, default=1)
    sede_id              = Column(Integer, ForeignKey("sedi.id"), nullable=False)

    # ── Relazioni ─────────────────────────────────────────────────────────────
    sede      = relationship("Sede",                  back_populates="attrezzature")
    richieste = relationship("RichiestaAttrezzatura", back_populates="attrezzatura")

    def __repr__(self) -> str:
        return f"<Attrezzatura {self.tipo} (x{self.quantita_disponibile}) - sede {self.sede_id}>"


class RichiestaAttrezzatura(Base):
    """Richiesta di attrezzatura allegata a una prenotazione."""

    __tablename__ = "richieste_attrezzatura"

    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prenotazione_id = Column(Integer, ForeignKey("prenotazioni.id"), nullable=False)
    attrezzatura_id = Column(Integer, ForeignKey("attrezzature.id"), nullable=False)
    quantita        = Column(Integer, nullable=False, default=1)
    stato           = Column(SAEnum(StatoRichiesta),
                             default=StatoRichiesta.INVIATA, nullable=False)
    note            = Column(Text, nullable=True)
    data_richiesta  = Column(DateTime, default=datetime.utcnow)

    # ── Relazioni ─────────────────────────────────────────────────────────────
    prenotazione = relationship("Prenotazione",  back_populates="attrezzature_richieste")
    attrezzatura = relationship("Attrezzatura",  back_populates="richieste")

    def __repr__(self) -> str:
        return f"<RichiestaAttrezzatura prenotazione={self.prenotazione_id} qty={self.quantita}>"