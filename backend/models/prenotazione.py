"""
Modello ORM per le prenotazioni aule.
Utilizza Single Table Inheritance per gestire prenotazioni singole e massive.
Include anche il modello RichiestaPrenotazione e Conflitto.
"""

from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Text,
                         Enum as SAEnum, Boolean, Date, Time)
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import (StatoPrenotazione, StatoRichiesta,
                                   TipoPrenotazione, TipoRicorrenza, TipoConflitto)


class Prenotazione(Base):
    """
    Prenotazione di un'aula per un corso.
    Classe base per prenotazioni singole e massive (STI).
    """
    __tablename__ = "prenotazioni"

    # ── Colonne comuni ────────────────────────────────────────────────────────
    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo            = Column(SAEnum(TipoPrenotazione), nullable=False)  # Discriminatore STI
    aula_id         = Column(Integer, ForeignKey("aule.id"), nullable=False)
    corso_id        = Column(Integer, ForeignKey("corsi.id"), nullable=False)
    richiedente_id  = Column(Integer, ForeignKey("utenti.id"), nullable=False)
    stato           = Column(SAEnum(StatoPrenotazione),
                             default=StatoPrenotazione.IN_ATTESA, nullable=False)
    note            = Column(Text, nullable=True)
    google_event_id = Column(String(255), nullable=True)  # ID evento Google Calendar
    data_creazione  = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_aggiornamento = Column(DateTime, default=datetime.utcnow,
                                 onupdate=datetime.utcnow, nullable=False)

    # ── Colonne per prenotazioni massive ──────────────────────────────────────
    tipo_ricorrenza   = Column(SAEnum(TipoRicorrenza), nullable=True)
    giorni_settimana  = Column(String(20), nullable=True,
                                comment="Es: '1,3,5' per Lun/Mer/Ven")
    data_inizio_range = Column(Date, nullable=True)
    data_fine_range   = Column(Date, nullable=True)
    intervallo        = Column(Integer, nullable=True, default=1)

    # ── Mapping polimorfico ───────────────────────────────────────────────────
    __mapper_args__ = {
        "polymorphic_on":       tipo,
        "polymorphic_identity": None,
    }

    # ── Relazioni ─────────────────────────────────────────────────────────────
    aula        = relationship("Aula",   back_populates="prenotazioni")
    corso       = relationship("Corso",  back_populates="prenotazioni")
    richiedente = relationship("Utente", back_populates="prenotazioni_richieste",
                               foreign_keys=[richiedente_id])
    slots       = relationship("SlotOrario", back_populates="prenotazione",
                               cascade="all, delete-orphan")
    richiesta   = relationship("RichiestaPrenotazione", back_populates="prenotazione",
                               uselist=False)
    attrezzature_richieste = relationship("RichiestaAttrezzatura",
                                           back_populates="prenotazione",
                                           cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Prenotazione #{self.id} [{self.tipo}] - aula {self.aula_id}>"


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
    Creata automaticamente quando un ResponsabileCorso fa una richiesta.
    La SegreteriaSede poi approva o rifiuta.
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
    conflitti    = relationship("Conflitto",     back_populates="richiesta",
                                cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Richiesta #{self.id} [{self.stato}]>"


class Conflitto(Base):
    """
    Conflitto rilevato tra una richiesta e una prenotazione esistente.
    Viene segnalato come WARNING ma non blocca la richiesta.
    """
    __tablename__ = "conflitti"

    id                      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    richiesta_id            = Column(Integer, ForeignKey("richieste_prenotazione.id"), nullable=False)
    prenotazione_conflitta_id = Column(Integer, ForeignKey("prenotazioni.id"), nullable=True,
                                        comment="Prenotazione già esistente che crea il conflitto")
    tipo                    = Column(SAEnum(TipoConflitto), nullable=False)
    descrizione             = Column(Text, nullable=False)
    data_rilevamento        = Column(DateTime, default=datetime.utcnow)

    # ── Relazioni ─────────────────────────────────────────────────────────────
    richiesta            = relationship("RichiestaPrenotazione", back_populates="conflitti")
    prenotazione_conflitta = relationship("Prenotazione",
                                           foreign_keys=[prenotazione_conflitta_id])

    def __repr__(self) -> str:
        return f"<Conflitto [{self.tipo}] su richiesta #{self.richiesta_id}>"