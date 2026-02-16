"""
Modello ORM per gli slot orari delle prenotazioni.
Uno slot rappresenta un blocco di tempo in una specifica data.
"""

from datetime import date, time
from sqlalchemy import Column, Integer, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base


class SlotOrario(Base):
    """Blocco orario associato a una prenotazione (data + ora inizio + ora fine)."""

    __tablename__ = "slot_orari"

    # ── Colonne ──────────────────────────────────────────────────────────────
    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prenotazione_id = Column(Integer, ForeignKey("prenotazioni.id"), nullable=False)
    data            = Column(Date, nullable=False, index=True)
    ora_inizio      = Column(Time, nullable=False)
    ora_fine        = Column(Time, nullable=False)
    annullato       = Column(Boolean, default=False)  # Permette annullamento singolo slot

    # ── Relazioni ─────────────────────────────────────────────────────────────
    prenotazione = relationship("Prenotazione", back_populates="slots")

    def get_durata_minuti(self) -> int:
        """Calcola la durata dello slot in minuti."""
        inizio = self.ora_inizio.hour * 60 + self.ora_inizio.minute
        fine   = self.ora_fine.hour * 60 + self.ora_fine.minute
        return fine - inizio

    def sovrappone_con(self, altro: "SlotOrario") -> bool:
        """
        Verifica se questo slot si sovrappone con un altro nella stessa data.
        Due slot si sovrappongono se uno inizia prima che l'altro finisca.
        """
        if self.data != altro.data:
            return False
        return self.ora_inizio < altro.ora_fine and altro.ora_inizio < self.ora_fine

    def __repr__(self) -> str:
        return f"<Slot {self.data} {self.ora_inizio}-{self.ora_fine}>"