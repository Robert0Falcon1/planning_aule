"""
Componente pagina di login.
"""

import streamlit as st
from frontend.api.auth import login


def mostra_pagina_login():
    """Renderizza la pagina di login con logo e form."""

    # Layout centrato
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("---")
        st.markdown(
            "<h1 style='text-align:center'>🏫</h1>"
            "<h2 style='text-align:center'>Sistema Prenotazione Aule</h2>"
            "<p style='text-align:center; color:grey'>Agenzia Formativa</p>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        with st.form("form_login", clear_on_submit=False):
            st.subheader("Accedi")
            email    = st.text_input("📧 Email", placeholder="utente@example.it")
            password = st.text_input("🔒 Password", type="password")
            submitted = st.form_submit_button("Entra →", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Inserisci email e password.")
                else:
                    with st.spinner("Autenticazione in corso..."):
                        successo = login(email, password)
                    if successo:
                        st.success("✅ Login effettuato!")
                        st.rerun()
                    else:
                        st.error("❌ Credenziali non valide.")

        st.markdown("---")
        st.markdown(
            "<p style='text-align:center; font-size:0.8em; color:grey'>"
            "Per assistenza contatta la segreteria</p>",
            unsafe_allow_html=True,
        )