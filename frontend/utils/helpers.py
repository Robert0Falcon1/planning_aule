"""
Funzioni di utilità condivise nel frontend.
"""

from datetime import date, time, datetime, timedelta
import streamlit as st
from frontend.config import STATO_CONFIG, GIORNI_SETTIMANA


def formato_data(d) -> str:
    """Formatta una data in formato italiano DD/MM/YYYY."""
    if isinstance(d, str):
        try:
            d = date.fromisoformat(d)
        except ValueError:
            return d
    if isinstance(d, (date, datetime)):
        return d.strftime("%d/%m/%Y")
    return str(d)


def formato_ora(t) -> str:
    """Formatta un orario come HH:MM."""
    if isinstance(t, str):
        return t[:5]  # Prende solo HH:MM
    if isinstance(t, time):
        return t.strftime("%H:%M")
    return str(t)


def stato_badge(stato: str) -> str:
    """Restituisce l'etichetta formattata per uno stato prenotazione."""
    config = STATO_CONFIG.get(stato, {"label": stato})
    return config["label"]


def giorni_da_numeri(numeri: list[int]) -> str:
    """Converte lista di numeri in nomi dei giorni (es: [1,3] → 'Lun, Mer')."""
    nomi = {
        1: "Lun", 2: "Mar", 3: "Mer",
        4: "Gio", 5: "Ven", 6: "Sab", 7: "Dom"
    }
    return ", ".join(nomi.get(n, str(n)) for n in sorted(numeri))


def settimana_corrente() -> tuple[date, date]:
    """Restituisce (lunedì, domenica) della settimana corrente."""
    oggi = date.today()
    lunedi = oggi - timedelta(days=oggi.weekday())
    domenica = lunedi + timedelta(days=6)
    return lunedi, domenica


def mese_corrente() -> tuple[date, date]:
    """Restituisce (primo giorno, ultimo giorno) del mese corrente."""
    oggi = date.today()
    primo = oggi.replace(day=1)
    if oggi.month == 12:
        ultimo = oggi.replace(year=oggi.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        ultimo = oggi.replace(month=oggi.month + 1, day=1) - timedelta(days=1)
    return primo, ultimo


def require_auth():
    """
    Verifica che l'utente sia autenticato.
    Se non lo è, reindirizza alla pagina di login.
    """
    if "token" not in st.session_state:
        st.warning("⚠️ Sessione non attiva. Effettua il login.")
        st.stop()


def nome_utente() -> str:
    """Restituisce il nome completo dell'utente dalla sessione."""
    nome    = st.session_state.get("nome", "")
    cognome = st.session_state.get("cognome", "")
    return f"{nome} {cognome}".strip()