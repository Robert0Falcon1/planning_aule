"""Funzioni API per le sedi."""

from frontend.api.client import get, post


def get_sedi() -> list:
    """Restituisce tutte le sedi attive."""
    return get("/sedi/") or []


def get_sede(sede_id: int) -> dict | None:
    """Restituisce una sede per ID."""
    return get(f"/sedi/{sede_id}")


def crea_sede(nome: str, indirizzo: str, citta: str, capienza: int) -> dict | None:
    """Crea una nuova sede."""
    return post("/sedi/", data={
        "nome": nome,
        "indirizzo": indirizzo,
        "citta": citta,
        "capienza_massima": capienza,
    })