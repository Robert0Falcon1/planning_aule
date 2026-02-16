"""
Componente sidebar con navigazione e info utente.
"""

import streamlit as st
from frontend.api.auth import logout
from frontend.config import RUOLO_LABELS


def mostra_sidebar() -> str:
    """
    Renderizza la sidebar con:
    - Info utente loggato
    - Menu di navigazione per ruolo
    - Pulsante logout

    Returns:
        La pagina selezionata dall'utente
    """
    ruolo   = st.session_state.get("ruolo", "")
    nome    = st.session_state.get("nome", "")
    cognome = st.session_state.get("cognome", "")

    with st.sidebar:
        # ── Intestazione ──────────────────────────────────────────────────────
        st.markdown("### 🏫 Prenotazione Aule")
        st.markdown("---")

        # ── Info utente ───────────────────────────────────────────────────────
        st.markdown(f"**{nome} {cognome}**")
        st.markdown(
            f"<span style='background:#E8F4FD; padding:3px 8px; color: black; font-weight: 600;"
            f"border-radius:4px; font-size:0.85em'>"
            f"{RUOLO_LABELS.get(ruolo, ruolo)}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # ── Menu navigazione per ruolo ────────────────────────────────────────
        pagina = _menu_per_ruolo(ruolo)

        st.markdown("---")

        # ── Logout ────────────────────────────────────────────────────────────
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

    return pagina


def _menu_per_ruolo(ruolo: str) -> str:
    """Costruisce il menu di navigazione in base al ruolo."""

    if ruolo == "responsabile_corso":
        voci = {
            "🏠 Dashboard":             "dashboard",
            "📅 Nuova Prenotazione":    "nuova_prenotazione",
            "🔄 Prenotazione Massiva":  "prenotazione_massiva",
            "📋 Le Mie Prenotazioni":   "mie_prenotazioni",
            "🔍 Slot Disponibili":      "slot_disponibili",
        }
    elif ruolo == "segreteria_sede":
        voci = {
            "🏠 Dashboard":             "dashboard",
            "📥 Richieste Pendenti":    "richieste_pendenti",
            "⚠️ Conflitti":             "conflitti",
            "📅 Calendario Sede":       "calendario_sede",
            "🏢 Gestione Aule":         "gestione_aule",
        }
    elif ruolo == "responsabile_sede":
        voci = {
            "🏠 Dashboard":             "dashboard",
            "📅 Prenotazioni Sede":     "prenotazioni_sede",
            "📊 Saturazione Spazi":     "saturazione",
        }
    elif ruolo == "segreteria_didattica":
        voci = {
            "🏠 Dashboard":             "dashboard",
            "📚 Prenotazioni per Corso":"prenotazioni_corsi",
        }
    elif ruolo == "coordinamento":
        voci = {
            "🏠 Dashboard":             "dashboard",
            "🌐 Vista Globale":         "vista_globale",
            "📊 Report Saturazione":    "report_saturazione",
            "👥 Gestione Utenti":       "gestione_utenti",
            "🏢 Gestione Sedi":         "gestione_sedi",
        }
    else:
        voci = {"🏠 Dashboard": "dashboard"}

    # Inizializza la pagina corrente nella sessione
    if "pagina_corrente" not in st.session_state:
        st.session_state["pagina_corrente"] = "dashboard"

    for label, key in voci.items():
        attivo = st.session_state["pagina_corrente"] == key
        stile  = "background:#1E88E5; color:white" if attivo else ""
        if st.button(
            label,
            key=f"nav_{key}",
            use_container_width=True,
            help=label,
        ):
            st.session_state["pagina_corrente"] = key
            st.rerun()

    return st.session_state.get("pagina_corrente", "dashboard")