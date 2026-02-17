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


@router.delete("/{utente_id}", status_code=200, summary="Disattiva utente")
def disattiva_utente(
    utente_id: int,
    db:        Session = Depends(get_db),
    corrente:  Utente  = Depends(verifica_permesso("utente:creare"))
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
    db:        Session = Depends(get_db),
    _:         Utente  = Depends(verifica_permesso("utente:creare"))
):
    """Riattiva un utente precedentemente disattivato."""
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