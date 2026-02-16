"""Funzioni API per autenticazione."""

import streamlit as st
from frontend.api.client import post, get


def login(email: str, password: str) -> bool:
    """
    Autentica l'utente e salva il token JWT nella sessione Streamlit.

    Returns:
        True se il login ha avuto successo, False altrimenti
    """
    risposta = post("/auth/login", form_data={
        "username": email,
        "password": password,
    })

    if risposta and "access_token" in risposta:
        # Salva i dati nella sessione Streamlit
        st.session_state["token"]   = risposta["access_token"]
        st.session_state["ruolo"]   = risposta["ruolo"]
        st.session_state["nome"]    = risposta["nome"]
        st.session_state["cognome"] = risposta["cognome"]
        st.session_state["email"]   = risposta["email"]
        st.session_state["sede_id"] = risposta.get("sede_id")
        return True
    return False


def logout():
    """Pulisce la sessione Streamlit effettuando il logout."""
    chiavi = ["token", "ruolo", "nome", "cognome", "email", "sede_id"]
    for chiave in chiavi:
        st.session_state.pop(chiave, None)


def is_autenticato() -> bool:
    """Verifica se l'utente è autenticato."""
    return "token" in st.session_state and st.session_state["token"] is not None


def get_utente_corrente() -> dict | None:
    """Recupera i dati aggiornati dell'utente corrente dal backend."""
    return get("/auth/me")