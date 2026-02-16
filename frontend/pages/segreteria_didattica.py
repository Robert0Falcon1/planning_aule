"""Dashboard per la Segreteria Didattica."""

import streamlit as st
from datetime import date, timedelta
from frontend.api import prenotazioni as api_pren, corsi as api_corsi
from frontend.components.alerts import mostra_stato_badge, card_metrica
from frontend.utils.helpers import formato_data, formato_ora, stato_badge


def mostra(pagina: str):
    if pagina == "dashboard":
        _dashboard()
    elif pagina == "prenotazioni_corsi":
        _prenotazioni_per_corso()


def _dashboard():
    st.title("📚 Dashboard Segreteria Didattica")
    st.markdown("---")

    tutte  = api_pren.get_prenotazioni()
    lista_corsi = api_corsi.get_corsi()

    col1, col2, col3 = st.columns(3)
    with col1:
        card_metrica("Corsi gestiti", len(lista_corsi), colore="#7B1FA2")
    with col2:
        card_metrica("Prenotazioni totali", len(tutte))
    with col3:
        conf = [p for p in tutte if p.get("stato") == "confermata"]
        card_metrica("Confermate", len(conf), colore="#28A745")

    st.markdown("---")
    st.subheader("📚 Riepilogo corsi")

    if not lista_corsi:
        st.info("Nessun corso disponibile.")
        return

    for c in lista_corsi:
        pren_corso = [p for p in tutte if p.get("corso_id") == c.get("id")]
        with st.expander(f"[{c.get('codice')}] {c.get('titolo')} ({len(pren_corso)} prenotazioni)"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Inizio:** {formato_data(c.get('data_inizio', ''))}")
                st.markdown(f"**Fine:** {formato_data(c.get('data_fine', ''))}")
            with col2:
                st.markdown(f"**Partecipanti:** {c.get('num_partecipanti', 0)}")
                st.markdown(f"**Finanziamento:** {c.get('tipo_finanziamento', '').replace('_', ' ').title()}")
            with col3:
                conf_corso = [p for p in pren_corso if p.get("stato") == "confermata"]
                st.markdown(f"**Prenotazioni confermate:** {len(conf_corso)}")


def _prenotazioni_per_corso():
    st.title("📚 Prenotazioni per Corso")
    st.markdown("---")

    lista_corsi = api_corsi.get_corsi()
    if not lista_corsi:
        st.info("Nessun corso disponibile.")
        return

    corso_options = {
        f"[{c['codice']}] {c['titolo']}": c["id"]
        for c in lista_corsi
    }

    col1, col2 = st.columns([2, 1])
    with col1:
        corso_sel = st.selectbox("Seleziona corso", options=list(corso_options.keys()))
        corso_id  = corso_options.get(corso_sel)
    with col2:
        filtro_stato = st.selectbox(
            "Stato",
            ["Tutti", "in_attesa", "confermata", "rifiutata", "conflitto"],
            format_func=lambda x: "Tutti" if x == "Tutti" else x.replace("_", " ").title()
        )

    if corso_id:
        lista = api_pren.get_prenotazioni(
            corso_id=corso_id,
            stato=filtro_stato if filtro_stato != "Tutti" else None,
        )

        st.caption(f"**{len(lista)}** prenotazioni per questo corso")
        st.markdown("---")

        if not lista:
            st.info("Nessuna prenotazione trovata.")
            return

        import pandas as pd
        righe = []
        for p in lista:
            slots = p.get("slots", [])
            righe.append({
                "ID":       p["id"],
                "Aula":     p["aula_id"],
                "Stato":    stato_badge(p.get("stato", "")),
                "Tipo":     p.get("tipo", "").replace("_", " ").title(),
                "N. Slot":  len(slots),
                "Dal":      formato_data(slots[0]["data"]) if slots else "-",
                "Al":       formato_data(slots[-1]["data"]) if len(slots) > 1 else "-",
            })
        st.dataframe(pd.DataFrame(righe), use_container_width=True, hide_index=True)