"""
Modello SQLAlchemy per la tabella Catalogo.
Aggiungere a backend/models/catalogo.py
"""

from sqlalchemy import (Column, Integer, String, Text, Date, DateTime,
                        DECIMAL, SmallInteger, func)
from backend.database import Base


class Catalogo(Base):
    __tablename__ = "Catalogo"

    id                              = Column(Integer, primary_key=True, autoincrement=True)
    stato                           = Column(SmallInteger, nullable=False, default=0)
    profilo_formativo               = Column(String(255), default=None)
    tipologia_utilizzo_parziale     = Column(SmallInteger, nullable=False, default=0)
    formazione_normata              = Column(SmallInteger, nullable=False, default=0)
    tipologia                       = Column(String(100), default=None)
    sep                             = Column(String(100), default=None)
    area_professionale              = Column(String(255), default=None)
    sottoarea_professionale         = Column(String(255), default=None)
    codice_ada                      = Column(String(50), default=None)
    titolo_ada                      = Column(String(255), default=None)
    competenze                      = Column(Text, default=None)
    professioni_nup_istat           = Column(Text, default=None)
    attivita_economiche_ateco_istat = Column(Text, default=None)
    titolo_percorso                 = Column(String(255), default=None)
    titolo_attestato                = Column(String(255), default=None)
    certificazione_uscita           = Column(String(255), default=None)
    tipologia_prova_finale          = Column(String(100), default=None)
    durata_prova_ore                = Column(DECIMAL(5, 2), default=None)
    prova_ingresso_orientamento     = Column(String(255), default=None)
    ore_corso_minime                = Column(DECIMAL(6, 2), default=None)
    ore_stage_minime                = Column(DECIMAL(6, 2), default=None)
    ore_elearning_minime_perc       = Column(DECIMAL(5, 2), default=None)
    ore_corso_massime               = Column(DECIMAL(6, 2), default=None)
    ore_stage_massime               = Column(DECIMAL(6, 2), default=None)
    ore_elearning_massime_perc      = Column(DECIMAL(5, 2), default=None)
    normativa_riferimento           = Column(Text, default=None)
    ore_assenza_massime             = Column(DECIMAL(6, 2), default=None)
    assegnazione_credito_ingresso   = Column(SmallInteger, nullable=False, default=0)
    data_inizio_validita            = Column(Date, default=None)
    data_fine_validita              = Column(Date, default=None)
    eta                             = Column(String(100), default=None)
    livello_minimo_scolarita        = Column(String(100), default=None)
    livello_massimo_scolarita       = Column(String(100), default=None)
    obbligo_scolastico_assolto      = Column(SmallInteger, default=None)
    esperienze_lavorative_pregresse = Column(Text, default=None)
    stato_occupazionale_ammesso     = Column(String(255), default=None)
    created_at                      = Column(DateTime, nullable=False, server_default=func.now())
    updated_at                      = Column(DateTime, nullable=False, server_default=func.now(),
                                             onupdate=func.now())