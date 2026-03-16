"""
Modello ORM per le prenotazioni aule.
Utilizza Single Table Inheritance per gestire prenotazioni singole e massive.
Include anche il modello RichiestaPrenotazione e Conflitto.
"""

from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Text,
                         Enum as SAEnum, Boolean, Date)
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import (StatoPrenotazione, StatoRichiesta,
                                   TipoPrenotazione, TipoRicorrenza)


class Prenotazione(Base):
    __tablename__ = "prenotazioni"

    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo            = Column(SAEnum(TipoPrenotazione), nullable=False)
    richiedente_id  = Column(Integer, ForeignKey("utenti.id"), nullable=False)
    stato           = Column(SAEnum(StatoPrenotazione),
                             default=StatoPrenotazione.IN_ATTESA, nullable=False)
    google_event_id = Column(String(255), nullable=True)
    data_creazione  = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_aggiornamento = Column(DateTime, default=datetime.utcnow,
                                onupdate=datetime.utcnow, nullable=False)

    # Colonne per prenotazioni massive
    tipo_ricorrenza   = Column(SAEnum(TipoRicorrenza), nullable=True)
    giorni_settimana  = Column(String(20), nullable=True)
    data_inizio_range = Column(Date, nullable=True)
    data_fine_range   = Column(Date, nullable=True)
    intervallo        = Column(Integer, nullable=True, default=1)

    __mapper_args__ = {
        "polymorphic_on":       tipo,
        "polymorphic_identity": None,
    }

    # Relazioni — aula/corso rimossi, ora sono sullo slot
    richiedente = relationship("Utente", back_populates="prenotazioni_richieste",
                               foreign_keys=[richiedente_id])
    slots       = relationship("SlotOrario", back_populates="prenotazione",
                               cascade="all, delete-orphan")
    richiesta   = relationship("RichiestaPrenotazione", back_populates="prenotazione",
                               uselist=False)
    attrezzature_richieste = relationship("RichiestaAttrezzatura",
                                          back_populates="prenotazione",
                                          cascade="all, delete-orphan")

    ha_conflitti_attivi  = Column(Boolean, default=False, nullable=False)
    conflitti_come_pren1 = relationship("ConflittoPrenotazione",
                                        foreign_keys="ConflittoPrenotazione.prenotazione_id_1",
                                        back_populates="prenotazione_1",
                                        cascade="all, delete-orphan")
    conflitti_come_pren2 = relationship("ConflittoPrenotazione",
                                        foreign_keys="ConflittoPrenotazione.prenotazione_id_2",
                                        back_populates="prenotazione_2",
                                        cascade="all")

    @property
    def conflitti(self):
        return self.conflitti_come_pren1 + self.conflitti_come_pren2

    @property
    def ha_conflitti_non_risolti(self) -> bool:
        return any(c.stato_risoluzione is None for c in self.conflitti)

    def __repr__(self):
        return f"<Prenotazione #{self.id} [{self.tipo}]>"
    

class PrenotazioneSingola(Prenotazione):
    """Prenotazione per un singolo slot temporale."""
    __mapper_args__ = {"polymorphic_identity": TipoPrenotazione.SINGOLA}


class PrenotazioneMassiva(Prenotazione):
    """Prenotazione ricorrente che genera automaticamente più slot."""
    __mapper_args__ = {"polymorphic_identity": TipoPrenotazione.MASSIVA}

    def conta_occorrenze(self) -> int:
        """Restituisce il numero di slot generati per questa prenotazione."""
        return len([s for s in self.slots if not s.annullato])


class RichiestaPrenotazione(Base):
    """
    Workflow di approvazione di una prenotazione.
    Mantenuta per tracking ha_conflitti anche dopo rimozione workflow approvazione.
    """
    __tablename__ = "richieste_prenotazione"

    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prenotazione_id = Column(Integer, ForeignKey("prenotazioni.id"), nullable=False, unique=True)
    segreteria_id   = Column(Integer, ForeignKey("utenti.id"), nullable=True,
                              comment="Segreteria che ha gestito la richiesta")
    stato           = Column(SAEnum(StatoRichiesta),
                             default=StatoRichiesta.INVIATA, nullable=False)
    data_richiesta  = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_gestione   = Column(DateTime, nullable=True)
    note_rifiuto    = Column(Text, nullable=True)
    ha_conflitti    = Column(Boolean, default=False,
                              comment="True se esistono conflitti rilevati al momento della richiesta")

    # ── Relazioni ─────────────────────────────────────────────────────────────
    prenotazione = relationship("Prenotazione",  back_populates="richiesta")
    segreteria   = relationship("Utente",        back_populates="richieste_gestite",
                                foreign_keys=[segreteria_id])

    def __repr__(self) -> str:
        return f"<Richiesta #{self.id} [{self.stato}]>"