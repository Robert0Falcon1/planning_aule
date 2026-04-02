"""Schema Pydantic per i docenti."""
from pydantic import BaseModel
from typing import Optional, List
from backend.models.enums import TipologiaDocente, LivelloIstruzione


class SedeMinimal(BaseModel):
    """Schema minimale per sede nel docente."""
    id: int
    nome: str
    
    class Config:
        from_attributes = True


class DocenteSchema(BaseModel):
    """Schema di risposta per un docente."""
    id: int
    nome: str
    cognome: str
    codice_fiscale: Optional[str] = None
    livello_istruzione: Optional[LivelloIstruzione] = None
    tipologia: TipologiaDocente
    webinar: bool = False
    ore_di_incarico: Optional[float] = None
    ore_svolte: float = 0.0
    unita_formative: Optional[str] = None
    sedi: List[SedeMinimal] = []  # ← AGGIUNTO - Lista sedi dove opera
    
    class Config:
        from_attributes = True