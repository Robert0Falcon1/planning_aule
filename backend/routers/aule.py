"""Router per la gestione delle aule."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import get_db
from backend.core.dependencies import get_utente_corrente, verifica_permesso
from backend.core.dependencies import get_utente_corrente, require_coordinamento  # ← AGGIUNTO
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

class AulaUpdate(BaseModel):
    nome:     Optional[str]     = None
    capienza: Optional[int]     = None
    note:     Optional[str]     = None
    attiva:   Optional[bool]    = None



@router.get("/", response_model=list[AulaSchema], summary="Lista aule")
def lista_aule(
    sede_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: Utente = Depends(get_utente_corrente)
):
    """Restituisce le aule, opzionalmente filtrate per sede."""
    query = db.query(Aula).filter(Aula.attiva == 1)
    if sede_id:
        query = query.filter(Aula.sede_id == sede_id)
    return query.all()


@router.post("/", response_model=AulaSchema, status_code=201, summary="Crea aula")
def crea_aula(
    dati: AulaInput,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_coordinamento)  # ← SOLO COORDINAMENTO
):
    """Crea una nuova aula in una sede (solo COORDINAMENTO)."""
    aula = Aula(**dati.model_dump())
    db.add(aula)
    db.commit()
    db.refresh(aula)
    return aula



@router.put("/{aula_id}", response_model=AulaSchema)
def aggiorna_aula(
    aula_id: int,
    payload: AulaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_utente_corrente),
):
    if current_user.ruolo != "COORDINAMENTO":
        raise HTTPException(status_code=403, detail="Non autorizzato")

    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula non trovata")

    if payload.nome     is not None: aula.nome     = payload.nome
    if payload.capienza is not None: aula.capienza = payload.capienza
    if payload.note     is not None: aula.note     = payload.note
    if payload.attiva   is not None: aula.attiva   = payload.attiva

    db.commit()
    db.refresh(aula)
    return aula