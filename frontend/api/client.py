"""
Client HTTP centralizzato per le chiamate al backend FastAPI.
Gestisce autenticazione, errori e timeout in modo uniforme.
"""

import requests
import streamlit as st
from frontend.config import API_BASE_URL, REQUEST_TIMEOUT


def _get_headers() -> dict:
    """
    Costruisce gli header HTTP con il token JWT dalla sessione Streamlit.
    """
    token = st.session_state.get("token")
    if token:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
    return {"Content-Type": "application/json"}


def get(endpoint: str, params: dict = None) -> dict | list | None:
    """
    Esegue una GET verso il backend.

    Returns:
        Il corpo della risposta JSON oppure None in caso di errore
    """
    try:
        resp = requests.get(
            f"{API_BASE_URL}{endpoint}",
            headers=_get_headers(),
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json()
        _gestisci_errore(resp)
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossibile connettersi al backend. Verifica che il server sia avviato.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout della richiesta. Riprova tra poco.")
        return None


def post(endpoint: str, data: dict = None, form_data: dict = None) -> dict | None:
    """
    Esegue una POST verso il backend.
    Usa form_data per il login OAuth2, data (JSON) per tutto il resto.
    """
    try:
        if form_data:
            # Login OAuth2: Content-Type application/x-www-form-urlencoded
            resp = requests.post(
                f"{API_BASE_URL}{endpoint}",
                data=form_data,
                timeout=REQUEST_TIMEOUT,
            )
        else:
            resp = requests.post(
                f"{API_BASE_URL}{endpoint}",
                headers=_get_headers(),
                json=data,
                timeout=REQUEST_TIMEOUT,
            )
        if resp.status_code in (200, 201):
            return resp.json()
        _gestisci_errore(resp)
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossibile connettersi al backend.")
        return None


def put(endpoint: str, data: dict = None) -> dict | None:
    """Esegue una PUT verso il backend."""
    try:
        resp = requests.put(
            f"{API_BASE_URL}{endpoint}",
            headers=_get_headers(),
            json=data,
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json()
        _gestisci_errore(resp)
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossibile connettersi al backend.")
        return None


def _gestisci_errore(response: requests.Response):
    """
    Gestisce le risposte HTTP con errore mostrando messaggi appropriati.
    """
    try:
        dettaglio = response.json().get("detail", "Errore sconosciuto")
    except Exception:
        dettaglio = response.text or "Errore sconosciuto"

    if response.status_code == 401:
        st.error("🔒 Sessione scaduta. Effettua nuovamente il login.")
        # Pulisce la sessione
        for key in ["token", "utente", "ruolo"]:
            st.session_state.pop(key, None)
        st.rerun()
    elif response.status_code == 403:
        st.error(f"🚫 Accesso negato: {dettaglio}")
    elif response.status_code == 404:
        st.warning(f"🔍 Non trovato: {dettaglio}")
    elif response.status_code == 409:
        st.warning(f"⚠️ Conflitto: {dettaglio}")
    elif response.status_code == 422:
        st.error(f"📝 Dati non validi: {dettaglio}")
    else:
        st.error(f"❌ Errore {response.status_code}: {dettaglio}")