"""Router per la gestione degli utenti (solo Coordinamento)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, EmailStr
from backend.database import get_db
from backend.core.security import hash_password
from backend.core.dependencies import require_coordinamento
from backend.models.utente import Utente
from backend.models.enums import RuoloUtente
from backend.schemas.utente import UtenteCrea, UtenteRisposta

router = APIRouter(prefix="/utenti", tags=["Utenti"])


class UtenteModifica(BaseModel):
    """Campi modificabili di un utente esistente. Tutti opzionali."""
    nome:     Optional[str]      = None
    cognome:  Optional[str]      = None
    email:    Optional[EmailStr] = None
    ruolo:    Optional[RuoloUtente] = None
    sede_id:  Optional[int]      = None
    password: Optional[str]      = None   # se presente, viene ri-hashata


@router.get("/", response_model=list[UtenteRisposta], summary="Lista utenti")
def lista_utenti(
    db: Session = Depends(get_db),
    _: Utente = Depends(require_coordinamento)
):
    """Restituisce tutti gli utenti (solo COORDINAMENTO)."""
    return db.query(Utente).all()


@router.post("/", response_model=UtenteRisposta, status_code=201,
             summary="Crea utente")
def crea_utente(
    dati: UtenteCrea,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_coordinamento)
):
    """Crea un nuovo utente nel sistema (solo COORDINAMENTO)."""
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


@router.patch("/{utente_id}", response_model=UtenteRisposta, summary="Modifica utente")
def modifica_utente(
    utente_id: int,
    dati: UtenteModifica,
    db: Session = Depends(get_db),
    corrente: Utente = Depends(require_coordinamento)
):
    """
    Aggiorna i dati di un utente esistente. Solo COORDINAMENTO.
    Tutti i campi sono opzionali — vengono aggiornati solo quelli presenti.
    """
    utente = db.query(Utente).filter(Utente.id == utente_id).first()
    if not utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    # Verifica unicità email se viene cambiata
    if dati.email and dati.email != utente.email:
        if db.query(Utente).filter(Utente.email == dati.email).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{dati.email}' già registrata"
            )

    if dati.nome     is not None: utente.nome    = dati.nome
    if dati.cognome  is not None: utente.cognome = dati.cognome
    if dati.email    is not None: utente.email   = dati.email
    if dati.ruolo    is not None: utente.ruolo   = dati.ruolo
    if dati.sede_id  is not None: utente.sede_id = dati.sede_id
    if dati.password is not None: utente.password_hash = hash_password(dati.password)

    db.commit()
    db.refresh(utente)
    return utente


@router.delete("/{utente_id}", status_code=200, summary="Disattiva utente")
def disattiva_utente(
    utente_id: int,
    db: Session = Depends(get_db),
    corrente: Utente = Depends(require_coordinamento)
):
    """
    Soft-delete: imposta attivo=False senza eliminare il record.
    Mantiene l'integrità referenziale con prenotazioni e corsi esistenti.
    """
    utente = db.query(Utente).filter(Utente.id == utente_id).first()
    if not utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    if utente.id == corrente.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Non puoi disattivare il tuo stesso account"
        )
    if not utente.attivo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'utente è già disattivato"
        )

    utente.attivo = False
    db.commit()
    return {"detail": f"Utente '{utente.email}' disattivato con successo"}


@router.patch("/{utente_id}/riattiva", status_code=200, summary="Riattiva utente")
def riattiva_utente(
    utente_id: int,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_coordinamento)
):
    """Riattiva un utente precedentemente disattivato. Solo COORDINAMENTO."""
    utente = db.query(Utente).filter(Utente.id == utente_id).first()
    if not utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    if utente.attivo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'utente è già attivo"
        )

    utente.attivo = True
    db.commit()
    return {"detail": f"Utente '{utente.email}' riattivato con successo"}