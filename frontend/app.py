"""
Entry point del frontend Streamlit.
Gestisce login, routing per ruolo e layout principale.
"""

# ── Fix percorso: aggiunge la root del progetto a sys.path ───────────────────
# Necessario perché Streamlit esegue il file direttamente senza aggiungere
# automaticamente la directory padre al path di Python.
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
from frontend.config import PAGE_CONFIG
from frontend.api.auth import is_autenticato
from frontend.components.login import mostra_pagina_login
from frontend.components.sidebar import mostra_sidebar

# ── Configurazione pagina (deve essere il primo comando Streamlit) ─────────────
st.set_page_config(**PAGE_CONFIG)

# ── CSS personalizzato ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .stButton button {
        text-align: left !important;
        border-radius: 8px;
        border: none;
        transition: background 0.2s;
    }
    .stButton button:hover { background: #E3F2FD !important; }
    [data-testid="metric-container"] {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 10px;
    }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def main():
    """Funzione principale: gestisce autenticazione e routing."""

    if not is_autenticato():
        mostra_pagina_login()
        return

    pagina = mostra_sidebar()
    ruolo  = st.session_state.get("ruolo", "")

    if ruolo == "responsabile_corso":
        from frontend.pages.responsabile_corso import mostra
        mostra(pagina)
    elif ruolo == "segreteria_sede":
        from frontend.pages.segreteria_sede import mostra
        mostra(pagina)
    elif ruolo == "responsabile_sede":
        from frontend.pages.responsabile_sede import mostra
        mostra(pagina)
    elif ruolo == "segreteria_didattica":
        from frontend.pages.segreteria_didattica import mostra
        mostra(pagina)
    elif ruolo == "coordinamento":
        from frontend.pages.coordinamento import mostra
        mostra(pagina)
    else:
        st.error(f"Ruolo '{ruolo}' non riconosciuto.")


if __name__ == "__main__":
    main()