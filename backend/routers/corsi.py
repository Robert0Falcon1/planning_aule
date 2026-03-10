"""
Router per i corsi formativi.
Tutti gli utenti autenticati possono consultare i corsi.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from backend.database import get_db
from backend.core.dependencies import get_utente_corrente
from backend.models.utente import Utente
from backend.models.corso import Corso

router = APIRouter(prefix="/corsi", tags=["Corsi"])


@router.get("/", summary="Lista corsi")
def lista_corsi(
    sede_id:  Optional[int]  = None,
    attivo:   Optional[bool] = None,
    db:       Session        = Depends(get_db),
    utente:   Utente         = Depends(get_utente_corrente),
):
    """
    Restituisce la lista dei corsi.
    Filtri opzionali: sede_id, attivo.
    """
    query = db.query(Corso)

    if sede_id is not None:
        query = query.filter(Corso.sede_id == sede_id)
    if attivo is not None:
        query = query.filter(Corso.attivo == attivo)

    corsi = query.order_by(Corso.data_inizio_corso.desc()).all()

    return [
        {
            "id":                corso.id,
            "codice":            corso.codice,
            "titolo":            corso.titolo,
            "sede_id":           corso.sede_id,
            "stato_del_corso":   corso.stato_del_corso.value if corso.stato_del_corso else None,
            "tipo_finanziamento": corso.tipo_finanziamento.value,
            "data_inizio_corso": corso.data_inizio_corso,
            "data_fine_presunta": corso.data_fine_presunta,
            "attivo":            corso.attivo,
        }
        for corso in corsi
    ]


@router.get("/{corso_id}", summary="Dettaglio corso")
def dettaglio_corso(
    corso_id: int,
    db:       Session = Depends(get_db),
    utente:   Utente  = Depends(get_utente_corrente),
):
    """Dettaglio completo di un corso."""
    corso = db.query(Corso).filter(Corso.id == corso_id).first()

    if not corso:
        raise HTTPException(404, f"Corso {corso_id} non trovato")

    return {
        "id":                            corso.id,
        "codice":                        corso.codice,
        "titolo":                        corso.titolo,
        "descrizione":                   corso.descrizione,
        "sede_id":                       corso.sede_id,
        "responsabile_id":               corso.responsabile_id,
        "tipo_finanziamento":            corso.tipo_finanziamento.value,
        "stato_del_corso":               corso.stato_del_corso.value if corso.stato_del_corso else None,
        "numero_proposta":               corso.numero_proposta,
        "id_corso_finanziato":           corso.id_corso_finanziato,
        "data_inizio_corso":             corso.data_inizio_corso,
        "data_fine_presunta":            corso.data_fine_presunta,
        "data_avvio_corso":              corso.data_avvio_corso,
        "attivo":                        corso.attivo,
        "num_partecipanti":              corso.num_partecipanti,
        "ore_totali":                    corso.ore_totali,
        "ore_erogate":                   corso.ore_erogate,
        "ore_stage":                     corso.ore_stage,
        "ore_residue":                   corso.get_ore_residue(),
    }