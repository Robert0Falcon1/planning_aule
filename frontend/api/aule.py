"""Funzioni API per le aule."""

from frontend.api.client import get, post


def get_aule(sede_id: int = None) -> list:
    """Restituisce le aule, filtrate per sede se specificato."""
    params = {"sede_id": sede_id} if sede_id else None
    return get("/aule/", params=params) or []


def get_slot_occupati(aula_id: int, data_dal: str, data_al: str) -> list:
    """
    Restituisce gli slot occupati per un'aula in un intervallo di date.
    Le date devono essere in formato ISO: YYYY-MM-DD.
    """
    return get(f"/prenotazioni/slot-liberi/{aula_id}", params={
        "data_dal": data_dal,
        "data_al":  data_al,
    }) or []


def crea_aula(nome: str, capienza: int, sede_id: int, note: str = None) -> dict | None:
    """Crea una nuova aula."""
    return post("/aule/", data={
        "nome":     nome,
        "capienza": capienza,
        "sede_id":  sede_id,
        "note":     note,
    })