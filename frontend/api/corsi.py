"""Funzioni API per i corsi."""

from frontend.api.client import get, post


def get_corsi() -> list:
    """Restituisce i corsi visibili per l'utente corrente."""
    return get("/corsi/") or []


def crea_corso(
    codice: str, titolo: str, tipo_finanziamento: str,
    responsabile_id: int, num_partecipanti: int,
    data_inizio: str, data_fine: str, descrizione: str = None
) -> dict | None:
    """Crea un nuovo corso."""
    return post("/corsi/", data={
        "codice":              codice,
        "titolo":              titolo,
        "tipo_finanziamento":  tipo_finanziamento,
        "responsabile_id":     responsabile_id,
        "num_partecipanti":    num_partecipanti,
        "data_inizio":         data_inizio,
        "data_fine":           data_fine,
        "descrizione":         descrizione,
    })