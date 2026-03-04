"""Router per la gestione delle sedi."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.core.dependencies import get_utente_corrente, require_coordinamento
from backend.models.sede import Sede
from backend.models.utente import Utente

router = APIRouter(prefix="/sedi", tags=["Sedi"])


class SedeSchema(BaseModel):
    id: int
    nome: str
    indirizzo: str
    citta: str
    capienza_massima: int
    class Config:
        from_attributes = True


class SedeInput(BaseModel):
    nome: str
    indirizzo: str
    citta: str
    capienza_massima: int = 0


@router.get("/", response_model=list[SedeSchema], summary="Lista sedi")
def lista_sedi(
    db: Session = Depends(get_db),
    _: Utente = Depends(get_utente_corrente)
):
    """Restituisce tutte le sedi attive."""
    return db.query(Sede).filter(Sede.attiva == 1).all()


@router.get("/{sede_id}", response_model=SedeSchema, summary="Dettaglio sede")
def dettaglio_sede(
    sede_id: int,
    db: Session = Depends(get_db),
    _: Utente = Depends(get_utente_corrente)
):
    """Restituisce una sede per ID."""
    sede = db.query(Sede).filter(Sede.id == sede_id).first()
    if not sede:
        raise HTTPException(status_code=404, detail="Sede non trovata")
    return sede


@router.post("/", response_model=SedeSchema, status_code=201,
             summary="Crea sede")
def crea_sede(
    dati: SedeInput,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_coordinamento)
):
    """
    Crea una nuova sede (solo COORDINAMENTO).
    
    Sistema 2 ruoli: solo COORDINAMENTO può creare sedi.
    """
    sede = Sede(
        nome=dati.nome,
        indirizzo=dati.indirizzo,
        citta=dati.citta,
        capienza_massima=dati.capienza_massima,
    )
    db.add(sede)
    db.commit()
    db.refresh(sede)
    return sede