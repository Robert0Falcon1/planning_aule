from datetime import date, time
from sqlalchemy import Column, Integer, Date, Time, ForeignKey, Boolean, Text, Index
from sqlalchemy.orm import relationship
from backend.database import Base


class SlotOrario(Base):
    __tablename__ = "slot_orari"

    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prenotazione_id = Column(Integer, ForeignKey("prenotazioni.id"), nullable=False)
    aula_id         = Column(Integer, ForeignKey("aule.id"),   nullable=False)
    corso_id        = Column(Integer, ForeignKey("corsi.id"),  nullable=False)
    note            = Column(Text, nullable=True)
    data            = Column(Date,    nullable=False, index=True)
    ora_inizio      = Column(Time,    nullable=False)
    ora_fine        = Column(Time,    nullable=False)
    annullato       = Column(Boolean, default=False)

    __table_args__ = (
        Index("ix_slot_orari_prenotazione_data", "prenotazione_id", "data"),
    )

    prenotazione = relationship("Prenotazione", back_populates="slots")
    aula         = relationship("Aula",  back_populates="slots")
    corso        = relationship("Corso", back_populates="slots")

    def get_durata_minuti(self) -> int:
        inizio = self.ora_inizio.hour * 60 + self.ora_inizio.minute
        fine   = self.ora_fine.hour   * 60 + self.ora_fine.minute
        return fine - inizio

    def sovrappone_con(self, altro: "SlotOrario") -> bool:
        if self.data != altro.data:
            return False
        return self.ora_inizio < altro.ora_fine and altro.ora_inizio < self.ora_fine

    def __repr__(self):
        return f"<Slot {self.data} {self.ora_inizio}-{self.ora_fine} aula={self.aula_id}>"