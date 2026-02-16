"""
Modello ORM per gli utenti del sistema.
Utilizza Single Table Inheritance (STI) per i 5 ruoli su un'unica tabella.
CORREZIONE: tutte le relationship con back_populates devono stare
sulla classe base Utente, non sulle sottoclassi.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import RuoloUtente


class Utente(Base):
    """
    Classe base per tutti gli utenti del sistema.
    Single Table Inheritance: tutti i ruoli condividono questa tabella.
    La colonna 'ruolo' funge da discriminatore polimorfico.
    """
    __tablename__ = "utenti"

    # ── Colonne ──────────────────────────────────────────────────────────────
    id             = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome           = Column(String(100), nullable=False)
    cognome        = Column(String(100), nullable=False)
    email          = Column(String(255), unique=True, nullable=False, index=True)
    password_hash  = Column(String(255), nullable=False)
    attivo         = Column(Boolean, default=True, nullable=False)
    ruolo          = Column(SAEnum(RuoloUtente), nullable=False)
    sede_id        = Column(Integer, ForeignKey("sedi.id"), nullable=True)
    data_creazione = Column(DateTime, default=datetime.utcnow, nullable=False)
    ultimo_accesso = Column(DateTime, nullable=True)

    # ── Mapping polimorfico ───────────────────────────────────────────────────
    __mapper_args__ = {
        "polymorphic_on":       ruolo,
        "polymorphic_identity": None,
    }

    # ── Relazioni sulla classe BASE (obbligatorio per back_populates) ─────────
    # IMPORTANTE: back_populates deve corrispondere alla proprietà del modello
    # target che punta a Utente. Poiché Corso/Prenotazione/RichiestaPrenotazione
    # dichiarano relationship verso "Utente" (non verso le sottoclassi),
    # i back_populates DEVONO stare qui su Utente.

    sede = relationship(
        "Sede",
        back_populates="utenti"
    )

    corsi = relationship(
        "Corso",
        back_populates="responsabile",
        foreign_keys="Corso.responsabile_id"
    )

    prenotazioni_richieste = relationship(
        "Prenotazione",
        back_populates="richiedente",
        foreign_keys="Prenotazione.richiedente_id"
    )

    richieste_gestite = relationship(
        "RichiestaPrenotazione",
        back_populates="segreteria",
        foreign_keys="RichiestaPrenotazione.segreteria_id"
    )

    def __repr__(self) -> str:
        return f"<Utente {self.email} [{self.ruolo}]>"


# ── Sottoclassi per ogni ruolo (solo mapper_args, nessuna relationship) ───────

class ResponsabileCorso(Utente):
    """Utente che può richiedere prenotazioni per i propri corsi."""
    __mapper_args__ = {"polymorphic_identity": RuoloUtente.RESPONSABILE_CORSO}


class ResponsabileSede(Utente):
    """Utente con visibilità sullo stato delle aule della propria sede."""
    __mapper_args__ = {"polymorphic_identity": RuoloUtente.RESPONSABILE_SEDE}


class SegreteriaSede(Utente):
    """Utente che valida e inserisce le prenotazioni nella propria sede."""
    __mapper_args__ = {"polymorphic_identity": RuoloUtente.SEGRETERIA_SEDE}


class SegreteriaDidattica(Utente):
    """Utente con visibilità sulle prenotazioni legate ai corsi."""
    __mapper_args__ = {"polymorphic_identity": RuoloUtente.SEGRETERIA_DIDATTICA}


class Coordinamento(Utente):
    """Utente con visibilità globale su tutte le sedi."""
    __mapper_args__ = {"polymorphic_identity": RuoloUtente.COORDINAMENTO}