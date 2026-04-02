"""
Router API per la gestione dei docenti.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.docente import Docente
from backend.models.sede import Sede
from backend.schemas.docente import DocenteSchema
from backend.routers.auth import get_utente_corrente

router = APIRouter(prefix="/docenti", tags=["Docenti"])


@router.get("/", response_model=List[DocenteSchema])
def get_docenti(
    sede_id: Optional[int] = Query(None, description="Filtra docenti per sede"),
    attivi: bool = Query(True, description="Mostra solo docenti attivi"),
    db: Session = Depends(get_db),
    current_user = Depends(get_utente_corrente)
):
    """
    Recupera la lista dei docenti.
    
    - **sede_id**: Filtra docenti che operano nella sede specificata
    - **attivi**: Se True mostra solo docenti con ore_di_incarico > ore_svolte
    """
    query = db.query(Docente)
    
    # Filtro per sede (tramite relazione many-to-many docente_sedi)
    if sede_id:
        query = query.join(Docente.sedi).filter(Sede.id == sede_id)
    
    # Filtro per docenti attivi (hanno ancora ore disponibili)
    if attivi:
        query = query.filter(
            (Docente.ore_di_incarico == None) | 
            (Docente.ore_di_incarico > Docente.ore_svolte)
        )
    
    # Ordina per cognome, nome
    docenti = query.order_by(Docente.cognome, Docente.nome).all()
    
    return docenti


@router.get("/{docente_id}", response_model=DocenteSchema)
def get_docente(
    docente_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_utente_corrente)
):
    """
    Recupera un singolo docente per ID.
    """
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    
    if not docente:
        raise HTTPException(status_code=404, detail="Docente non trovato")
    
    return docente