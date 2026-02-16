"""Funzioni API per le prenotazioni."""

from frontend.api.client import get, post


def get_prenotazioni(
    sede_id: int = None,
    corso_id: int = None,
    stato: str = None,
    data_dal: str = None,
    data_al: str = None,
) -> list:
    """Restituisce le prenotazioni visibili per l'utente corrente."""
    params = {}
    if sede_id:   params["sede_id"]  = sede_id
    if corso_id:  params["corso_id"] = corso_id
    if stato:     params["stato"]    = stato
    if data_dal:  params["data_dal"] = data_dal
    if data_al:   params["data_al"]  = data_al
    return get("/prenotazioni/", params=params) or []


def crea_prenotazione_singola(
    aula_id: int, corso_id: int,
    data: str, ora_inizio: str, ora_fine: str,
    note: str = None
) -> dict | None:
    """Crea una prenotazione singola."""
    return post("/prenotazioni/singola", data={
        "aula_id":  aula_id,
        "corso_id": corso_id,
        "slot": {
            "data":       data,
            "ora_inizio": ora_inizio,
            "ora_fine":   ora_fine,
        },
        "note": note,
    })


def crea_prenotazione_massiva(
    aula_id: int, corso_id: int,
    data_inizio: str, data_fine: str,
    ora_inizio: str, ora_fine: str,
    tipo_ricorrenza: str, giorni_settimana: list[int],
    note: str = None
) -> dict | None:
    """Crea una prenotazione massiva (ricorrente)."""
    return post("/prenotazioni/massiva", data={
        "aula_id":          aula_id,
        "corso_id":         corso_id,
        "data_inizio":      data_inizio,
        "data_fine":        data_fine,
        "ora_inizio":       ora_inizio,
        "ora_fine":         ora_fine,
        "tipo_ricorrenza":  tipo_ricorrenza,
        "giorni_settimana": giorni_settimana,
        "note":             note,
    })


def approva_richiesta(richiesta_id: int) -> dict | None:
    """Approva una richiesta di prenotazione."""
    return post(f"/prenotazioni/richieste/{richiesta_id}/approva")


def rifiuta_richiesta(richiesta_id: int, motivo: str) -> dict | None:
    """Rifiuta una richiesta di prenotazione."""
    return post(
        f"/prenotazioni/richieste/{richiesta_id}/rifiuta",
        data=None,
    )


def get_richieste_pendenti(sede_id: int = None) -> list:
    """Restituisce le prenotazioni in attesa di validazione."""
    return get_prenotazioni(sede_id=sede_id, stato="in_attesa")


def get_prenotazioni_conflitto(sede_id: int = None) -> list:
    """Restituisce le prenotazioni con conflitti."""
    return get_prenotazioni(sede_id=sede_id, stato="conflitto")