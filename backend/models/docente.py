"""
Modello ORM per i docenti dei corsi.
Docente eredita da Persona (nome/cognome/sede) ma NON ha credenziali di accesso.
"""

from sqlalchemy import (Column, Integer, String, Float, Boolean,
                         ForeignKey, Enum as SAEnum, Table)
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import TipologiaDocente, LivelloIstruzione


# ── Tabella di associazione Docente ↔ Sede (opera in) ─────────────────────────
docente_sedi = Table(
    "docente_sedi",
    Base.metadata,
    Column("docente_id", Integer, ForeignKey("docenti.id"), primary_key=True),
    Column("sede_id",    Integer, ForeignKey("sedi.id"),    primary_key=True),
)


class Docente(Base):
    """
    Docente assegnato a uno o più corsi.
    Non ha accesso al gestionale (nessuna email/password).
    """
    __tablename__ = "docenti"

    # ── Anagrafica base (equivalente Persona) ─────────────────────────────────
    id      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome    = Column(String(100), nullable=False)
    cognome = Column(String(100), nullable=False)

    # ── Dati professionali ────────────────────────────────────────────────────
    codice_fiscale     = Column(String(16), nullable=True, index=True)
    livello_istruzione = Column(SAEnum(LivelloIstruzione), nullable=True)
    tipologia          = Column(SAEnum(TipologiaDocente), nullable=False,
                                default=TipologiaDocente.T,
                                comment="T=Teoria · P=Pratica · S=Stage")
    webinar            = Column(Boolean, default=False,
                                comment="Se True il docente opera in remoto e non occupa aula fisica")

    # ── Ore ───────────────────────────────────────────────────────────────────
    ore_di_incarico = Column(Float, nullable=True,
                              comment="Ore totali contrattualizzate per il corso")
    ore_svolte      = Column(Float, nullable=False, default=0.0)

    # ── Unità formative (lista serializzata come JSON/CSV) ───────────────────
    unita_formative = Column(String(1000), nullable=True,
                              comment="Unità formative assegnate, separate da virgola")

    # ── Relazioni ─────────────────────────────────────────────────────────────
    sedi   = relationship("Sede",   secondary=docente_sedi, back_populates="docenti")
    corsi  = relationship("Corso",  secondary="corso_docenti", back_populates="docenti")

    def get_ore_residue(self) -> float:
        if self.ore_di_incarico is None:
            return 0.0
        return self.ore_di_incarico - self.ore_svolte

    def is_remoto(self) -> bool:
        return self.webinar is True

    def __repr__(self) -> str:
        return f"<Docente {self.cognome} {self.nome} [{self.tipologia}]>"