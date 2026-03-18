"""
Modello ConflittoPrenotazione - Sistema rilevamento automatico conflitti
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.database import Base
from backend.models.enums import TipoConflitto, StatoRisoluzioneConflitto


class ConflittoPrenotazione(Base):
    """
    Conflitto tra due prenotazioni rilevato automaticamente
    """
    
    __tablename__ = "conflitti_prenotazione"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Prenotazioni in conflitto
    prenotazione_id_1 = Column(
        Integer, 
        ForeignKey("prenotazioni.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    prenotazione_id_2 = Column(
        Integer, 
        ForeignKey("prenotazioni.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    slot_id_1 = Column(Integer, ForeignKey("slot_orari.id"), nullable=True,
                    comment="Slot specifico di prenotazione_1 che causa il conflitto")
    slot_id_2 = Column(Integer, ForeignKey("slot_orari.id"), nullable=True,
                    comment="Slot specifico di prenotazione_2 che causa il conflitto")

    slot_1 = relationship("SlotOrario", foreign_keys=[slot_id_1])
    slot_2 = relationship("SlotOrario", foreign_keys=[slot_id_2])

    # Tipo di conflitto
    tipo_conflitto = Column(
        SQLEnum(TipoConflitto),
        nullable=False,
        default=TipoConflitto.OVERLAP_ORARIO
    )
    
    # Rilevamento
    rilevato_il = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    
    # Risoluzione (COORDINAMENTO)
    stato_risoluzione = Column(
        SQLEnum(StatoRisoluzioneConflitto),
        nullable=True,
        default=None,
        index=True
    )
    
    risolto_il = Column(DateTime, nullable=True)
    
    risolto_da = Column(
        Integer,
        ForeignKey("utenti.id", ondelete="SET NULL"),
        nullable=True
    )
    
    note_risoluzione = Column(Text, nullable=True)
    
    # Relazioni
    prenotazione_1 = relationship(
        "Prenotazione",
        foreign_keys=[prenotazione_id_1],
        back_populates="conflitti_come_pren1"
    )
    
    prenotazione_2 = relationship(
        "Prenotazione",
        foreign_keys=[prenotazione_id_2],
        back_populates="conflitti_come_pren2"
    )
    
    risolutore = relationship(
        "Utente",
        foreign_keys=[risolto_da],
        back_populates="conflitti_risolti"
    )
    
    @property
    def is_risolto(self) -> bool:
        """Controlla se il conflitto è risolto"""
        return self.stato_risoluzione is not None and self.stato_risoluzione != ''

    
    def risolvi(
        self, 
        risolto_da_id: int, 
        stato: StatoRisoluzioneConflitto,
        note: str = None
    ):
        """Risolve il conflitto"""
        self.stato_risoluzione = stato
        self.risolto_da = risolto_da_id
        self.risolto_il = datetime.now(timezone.utc)
        self.note_risoluzione = note