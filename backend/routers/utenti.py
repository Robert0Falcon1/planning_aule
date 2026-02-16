"""Router per la gestione degli utenti (solo Coordinamento)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.core.security import hash_password
from backend.core.dependencies import get_utente_corrente, verifica_permesso
from backend.models.utente import Utente
from backend.models.enums import RuoloUtente
from backend.schemas.utente import UtenteCrea, UtenteRisposta

router = APIRouter(prefix="/utenti", tags=["Utenti"])

# Mappa ruolo → classe concreta
_MAPPA_RUOLO_CLASSE = {
    RuoloUtente.RESPONSABILE_CORSO:   "ResponsabileCorso",
    RuoloUtente.RESPONSABILE_SEDE:    "ResponsabileSede",
    RuoloUtente.SEGRETERIA_SEDE:      "SegreteriaSede",
    RuoloUtente.SEGRETERIA_DIDATTICA: "SegreteriaDidattica",
    RuoloUtente.COORDINAMENTO:        "Coordinamento",
}


@router.get("/", response_model=list[UtenteRisposta], summary="Lista utenti")
def lista_utenti(
    db: Session = Depends(get_db),
    _:  Utente  = Depends(verifica_permesso("utente:vedere_tutti"))
):
    """Restituisce tutti gli utenti (solo Coordinamento)."""
    return db.query(Utente).all()


@router.post("/", response_model=UtenteRisposta, status_code=201,
             summary="Crea utente")
def crea_utente(
    dati: UtenteCrea,
    db:   Session = Depends(get_db),
    _:    Utente  = Depends(verifica_permesso("utente:creare"))
):
    """Crea un nuovo utente nel sistema (solo Coordinamento)."""
    # Verifica email univoca
    esistente = db.query(Utente).filter(Utente.email == dati.email).first()
    if esistente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{dati.email}' già registrata"
        )

    utente = Utente(
        nome=dati.nome,
        cognome=dati.cognome,
        email=dati.email,
        password_hash=hash_password(dati.password),
        ruolo=dati.ruolo,
        sede_id=dati.sede_id,
        attivo=True,
    )
    db.add(utente)
    db.commit()
    db.refresh(utente)
    return utente