"""
Modello ORM per gli allievi iscritti ai corsi.
Allievo eredita da Persona ma NON ha credenziali di accesso al gestionale.
"""

from datetime import date
from sqlalchemy import (Column, Integer, String, Float, Boolean, Date,
                         ForeignKey, Enum as SAEnum, Text)
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.enums import (
    Sesso, Cittadinanza, ResidenzaIn, LivelloIstruzione,
    CondizioneOccupazionale, DisabilitaVulnerabilita, SvantaggioAbitativo,
)


class Allievo(Base):
    """
    Allievo iscritto a uno o più corsi.
    Non ha accesso al gestionale (nessuna email/password).
    """
    __tablename__ = "allievi"

    # ── Anagrafica base (equivalente Persona) ─────────────────────────────────
    id      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome    = Column(String(100), nullable=False)
    cognome = Column(String(100), nullable=False)

    # ── Anagrafica estesa ─────────────────────────────────────────────────────
    codice_fiscale    = Column(String(16), nullable=True, index=True)
    data_nascita      = Column(Date, nullable=True)
    nazione_nascita   = Column(String(100), nullable=True)
    provincia_nascita = Column(String(5),   nullable=True)
    comune_nascita    = Column(String(100), nullable=True)
    sesso             = Column(SAEnum(Sesso), nullable=True)

    # ── Cittadinanza e residenza ───────────────────────────────────────────────
    cittadinanza          = Column(SAEnum(Cittadinanza), nullable=True)
    paese                 = Column(String(100), nullable=True,
                                    comment="Derivato da cittadinanza, gestito lato backend")
    residente_in          = Column(SAEnum(ResidenzaIn), nullable=True)
    provincia_residenza   = Column(String(5),   nullable=True)
    comune_residenza      = Column(String(100), nullable=True)
    indirizzo             = Column(String(255), nullable=True)
    cap                   = Column(String(10),  nullable=True)

    # ── Contatti ──────────────────────────────────────────────────────────────
    telefono_prefisso = Column(String(10),  nullable=True)
    telefono_numero   = Column(String(20),  nullable=True)
    email             = Column(String(255), nullable=True)

    # ── Date corso ────────────────────────────────────────────────────────────
    data_firma_patto_attivazione = Column(Date, nullable=True)
    data_iscrizione              = Column(Date, nullable=True)
    data_inizio_frequenza        = Column(Date, nullable=True)
    data_ritiro                  = Column(Date, nullable=True)
    motivo_ritiro                = Column(String(500), nullable=True)

    # ── Registro ──────────────────────────────────────────────────────────────
    posizione_registro_cartaceo = Column(Integer, nullable=True,
                                          comment="Corrispondenza registro cartaceo / Sistema Piemonte")
    ore_assenza  = Column(Float, nullable=False, default=0.0)
    ore_erogate  = Column(Float, nullable=False, default=0.0)
    uditore      = Column(Boolean, nullable=False, default=False,
                           comment="Se True l'allievo è uditore non formale")

    # ── Profilo ───────────────────────────────────────────────────────────────
    livello_istruzione         = Column(SAEnum(LivelloIstruzione),         nullable=True)
    condizione_occupazionale   = Column(SAEnum(CondizioneOccupazionale),   nullable=True)
    disabilita_vulnerabilita   = Column(SAEnum(DisabilitaVulnerabilita),   nullable=True,
                                         default=DisabilitaVulnerabilita.NESSUNA)
    svantaggio_abitativo       = Column(SAEnum(SvantaggioAbitativo),       nullable=True,
                                         default=SvantaggioAbitativo.NESSUNA)
    documenti_allegati         = Column(Text, nullable=True,
                                         comment="Nomi file separati da virgola")

    # ── Relazioni ─────────────────────────────────────────────────────────────
    corsi    = relationship("Corso",   secondary="corso_allievi",   back_populates="allievi")
    lezioni  = relationship("Lezione", secondary="lezione_presenze", back_populates="allievi_presenti")

    # ── Metodi ────────────────────────────────────────────────────────────────
    def is_ritirato(self) -> bool:
        return self.data_ritiro is not None

    def get_percentuale_presenza(self) -> float:
        """Ritorna la % di presenza rispetto alle ore erogate al corso."""
        if not self.ore_erogate:
            return 0.0
        ore_presenza = self.ore_erogate - self.ore_assenza
        return round((ore_presenza / self.ore_erogate) * 100, 2)

    def __repr__(self) -> str:
        return f"<Allievo {self.cognome} {self.nome}>"