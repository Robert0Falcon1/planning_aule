"""Router per la gestione delle aule."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import get_db
from backend.core.dependencies import get_utente_corrente, verifica_permesso
from backend.models.aula import Aula
from backend.models.utente import Utente

router = APIRouter(prefix="/aule", tags=["Aule"])


class AulaSchema(BaseModel):
    id: int
    nome: str
    capienza: int
    sede_id: int
    note: Optional[str] = None
    class Config:
        from_attributes = True


class AulaInput(BaseModel):
    nome: str
    capienza: int
    sede_id: int
    note: Optional[str] = None


@router.get("/", response_model=list[AulaSchema], summary="Lista aule")
def lista_aule(
    sede_id: Optional[int] = None,
    db:      Session = Depends(get_db),
    _:       Utente  = Depends(get_utente_corrente)
):
    """Restituisce le aule, opzionalmente filtrate per sede."""
    query = db.query(Aula).filter(Aula.attiva == 1)
    if sede_id:
        query = query.filter(Aula.sede_id == sede_id)
    return query.all()


@router.post("/", response_model=AulaSchema, status_code=201, summary="Crea aula")
def crea_aula(
    dati: AulaInput,
    db:   Session = Depends(get_db),
    _:    Utente  = Depends(verifica_permesso("aula:gestire"))
):
    """Crea una nuova aula in una sede."""
    aula = Aula(**dati.model_dump())
    db.add(aula)
    db.commit()
    db.refresh(aula)
    return aula