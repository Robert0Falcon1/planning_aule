"""Componenti per messaggi e notifiche."""

import streamlit as st
from frontend.config import STATO_CONFIG


def mostra_conflitto_warning(conflitti: list):
    """Mostra un avviso con i conflitti rilevati (non bloccante)."""
    if not conflitti:
        return
    st.warning(
        f"⚠️ **Attenzione: {len(conflitti)} conflitto/i rilevato/i**\n\n"
        "La richiesta è stata comunque inviata. La Segreteria di Sede la gestirà."
    )
    with st.expander("Dettagli conflitti"):
        for c in conflitti:
            st.markdown(f"- 🔸 `{c.get('tipo', '')}`: {c.get('descrizione', '')}")


def mostra_stato_badge(stato: str):
    """Renderizza un badge colorato per lo stato."""
    config = STATO_CONFIG.get(stato, {"label": stato, "color": "#888"})
    st.markdown(
        f"<span style='background:{config['color']}; color:white; "
        f"padding:3px 10px; border-radius:10px; font-size:0.85em'>"
        f"{config['label']}</span>",
        unsafe_allow_html=True,
    )


def card_metrica(titolo: str, valore, delta=None, colore: str = "#1E88E5"):
    """Renderizza una card metrica personalizzata."""
    st.markdown(
        f"""
        <div style='background:{colore}15; border-left:4px solid {colore};
                    padding:15px 20px; border-radius:8px; margin:5px 0'>
            <p style='margin:0; font-size:0.85em; color:grey'>{titolo}</p>
            <p style='margin:0; font-size:1.8em; font-weight:bold; color:{colore}'>{valore}</p>
            {f"<p style='margin:0; font-size:0.8em; color:grey'>{delta}</p>" if delta else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )