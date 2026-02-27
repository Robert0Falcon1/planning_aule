"""
Modello ORM per i corsi gestiti dall'Agenzia Formativa.
Aggiornato con tutti i campi del class diagram v3:
stati Sistema Piemonte, ore dettagliate, relazioni docenti/allievi.
"""

from datetime import date, datetime
from sqlalchemy import (Column, Integer, String, Float, Date, DateTime,
                         ForeignKey, Enum as SAEnum, Boolean, Text, Table)
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import TipoFinanziamento, StatoCorso, OreAccertamento


# ── Tabelle di associazione ────────────────────────────────────────────────────

corso_docenti = Table(
    "corso_docenti",
    Base.metadata,
    Column("corso_id",   Integer, ForeignKey("corsi.id"),    primary_key=True),
    Column("docente_id", Integer, ForeignKey("docenti.id"),  primary_key=True),
)

corso_allievi = Table(
    "corso_allievi",
    Base.metadata,
    Column("corso_id",   Integer, ForeignKey("corsi.id"),   primary_key=True),
    Column("allievo_id", Integer, ForeignKey("allievi.id"), primary_key=True),
)


class Corso(Base):
    """Corso formativo organizzato dall'Agenzia."""

    __tablename__ = "corsi"

    # ── Identificazione ───────────────────────────────────────────────────────
    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codice      = Column(String(50), unique=True, nullable=False, index=True,
                          comment="Formato: B164-{progressivo}-{anno}-{accorpamento}")
    titolo      = Column(String(255), nullable=False)
    descrizione = Column(Text, nullable=True,
                          comment="Derivato dal repertorio regionale")

    # ── Finanziamento / Sistema Piemonte ──────────────────────────────────────
    tipo_finanziamento             = Column(SAEnum(TipoFinanziamento), nullable=False)
    stato_del_corso                = Column(SAEnum(StatoCorso), nullable=True,
                                             comment="Codice stato Sistema Piemonte")
    numero_proposta                = Column(Integer, nullable=True)
    id_corso_finanziato            = Column(Integer, nullable=True,
                                             comment="15xxxx=GOL · 10xxxx=FSE")
    id_attivita                    = Column(Integer, nullable=True)
    criterio_selezione_destinatari = Column(String(500), nullable=True)

    # ── FK ────────────────────────────────────────────────────────────────────
    responsabile_id = Column(Integer, ForeignKey("utenti.id"), nullable=False)
    sede_id         = Column(Integer, ForeignKey("sedi.id"),   nullable=True)

    # ── Date ──────────────────────────────────────────────────────────────────
    data_creazione    = Column(DateTime, default=datetime.utcnow)
    data_avvio_corso  = Column(Date, nullable=True,
                                comment="Data avvio formale su Sistema Piemonte")
    data_inizio_corso = Column(Date, nullable=False)
    data_fine_presunta = Column(Date, nullable=False)
    attivo            = Column(Boolean, default=True)

    # ── Partecipanti e ore ────────────────────────────────────────────────────
    num_partecipanti          = Column(Integer, nullable=False, default=1)
    ore_totali                = Column(Float, nullable=True,
                                        comment="Ore totali previste dal progetto formativo")
    ore_erogate               = Column(Float, nullable=False, default=0.0)
    ore_stage                 = Column(Float, nullable=True)
    ente_stage                = Column(String(255), nullable=True,
                                        comment="Derivato da mapping allievi")
    ore_aggiuntive            = Column(Float, nullable=True,
                                        comment="Ore discrezionali del docente (test ITA/Informatica)")
    ore_accertamento_stranieri = Column(SAEnum(OreAccertamento), nullable=True,
                                         comment="Tipo prova accertamento: 40 min × prova fissa")
    ore_selezione_allievi     = Column(Float, nullable=True,
                                        comment="Inserite dal RC dal frontend, modificabili")

    # ── Relazioni ─────────────────────────────────────────────────────────────
    responsabile = relationship(
        "Utente",
        back_populates="corsi",
        foreign_keys=[responsabile_id],
    )
    sede = relationship(
        "Sede",
        back_populates="corsi",
        foreign_keys=[sede_id],
    )
    prenotazioni = relationship("Prenotazione", back_populates="corso")
    lezioni      = relationship("Lezione",      back_populates="corso",
                                cascade="all, delete-orphan")
    docenti  = relationship("Docente", secondary=corso_docenti, back_populates="corsi")
    allievi  = relationship("Allievo", secondary=corso_allievi, back_populates="corsi")

    # ── Metodi ────────────────────────────────────────────────────────────────
    def is_attivo(self) -> bool:
        return self.data_inizio_corso <= date.today() <= self.data_fine_presunta

    def get_ore_residue(self) -> float:
        if self.ore_totali is None:
            return 0.0
        return self.ore_totali - self.ore_erogate

    def inferisci_finanziamento(self) -> TipoFinanziamento:
        """
        Determina il tipo di finanziamento dal prefisso di id_corso_finanziato.
        15xxxx → GOL (FINANZIATO_PUBBLICO) · 10xxxx → FSE (FINANZIATO_PUBBLICO)
        """
        if self.id_corso_finanziato:
            s = str(self.id_corso_finanziato)
            if s.startswith("15") or s.startswith("10"):
                return TipoFinanziamento.FINANZIATO_PUBBLICO
        return self.tipo_finanziamento

    def __repr__(self) -> str:
        return f"<Corso {self.codice} - {self.titolo}>"