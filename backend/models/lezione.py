"""
Modello ORM per le lezioni di un corso.
Una lezione con si_ripete=True genera una PrenotazioneMassiva.
Gestisce il registro presenze tramite tabella di associazione.
"""

from datetime import date, time
from sqlalchemy import (Column, Integer, String, Date, Time, Boolean,
                         ForeignKey, Enum as SAEnum, Text, Table)
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import TipoLezione


# ── Tabella di associazione Lezione ↔ Allievo (presenze) ─────────────────────
lezione_presenze = Table(
    "lezione_presenze",
    Base.metadata,
    Column("lezione_id", Integer, ForeignKey("lezioni.id"),  primary_key=True),
    Column("allievo_id", Integer, ForeignKey("allievi.id"), primary_key=True),
)


class Lezione(Base):
    """
    Singola lezione registrata per un corso.
    Corrisponde a una riga del registro su Sistema Piemonte (inserita due volte).
    """
    __tablename__ = "lezioni"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    corso_id   = Column(Integer, ForeignKey("corsi.id"), nullable=False)

    # ── Orario ────────────────────────────────────────────────────────────────
    data       = Column(Date, nullable=False, index=True,
                         comment="Inserita due volte su Sistema Piemonte")
    ora_inizio = Column(Time, nullable=False)
    ora_fine   = Column(Time, nullable=False)

    # ── Tipologia e metadata ───────────────────────────────────────────────────
    tipo_lezione     = Column(SAEnum(TipoLezione), nullable=False,
                               default=TipoLezione.NORMALE)
    note             = Column(Text, nullable=True)
    si_ripete        = Column(Boolean, nullable=False, default=False,
                               comment="Se True → al salvataggio viene generata una PrenotazioneMassiva")
    numero_variazione = Column(Integer, nullable=False, default=0,
                                comment="Contatore incrementale delle modifiche apportate alla lezione")

    # ── Relazioni ─────────────────────────────────────────────────────────────
    corso           = relationship("Corso",   back_populates="lezioni")
    allievi_presenti = relationship("Allievo", secondary=lezione_presenze,
                                    back_populates="lezioni")

    # ── Metodi ────────────────────────────────────────────────────────────────
    def get_durata_minuti(self) -> int:
        inizio = self.ora_inizio.hour * 60 + self.ora_inizio.minute
        fine   = self.ora_fine.hour   * 60 + self.ora_fine.minute
        return fine - inizio

    def is_fad(self) -> bool:
        """FAD: Formazione a Distanza — non richiede aula fisica."""
        return self.tipo_lezione == TipoLezione.FAD

    def __repr__(self) -> str:
        return f"<Lezione {self.data} {self.ora_inizio}-{self.ora_fine} [{self.tipo_lezione}]>"