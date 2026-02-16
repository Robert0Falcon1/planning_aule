"""Dashboard per il Responsabile di Sede."""

import streamlit as st
from datetime import date, timedelta
from frontend.api import prenotazioni as api_pren, aule
from frontend.components.alerts import mostra_stato_badge, card_metrica
from frontend.utils.helpers import formato_data, formato_ora, mese_corrente


def mostra(pagina: str):
    if pagina == "dashboard":
        _dashboard()
    elif pagina == "prenotazioni_sede":
        _prenotazioni_sede()
    elif pagina == "saturazione":
        _saturazione()


def _dashboard():
    st.title("🏢 Dashboard Responsabile di Sede")
    sede_id = st.session_state.get("sede_id")
    st.markdown("---")

    tutte = api_pren.get_prenotazioni(sede_id=sede_id)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metrica("Totale Prenotazioni", len(tutte))
    with col2:
        conf = [p for p in tutte if p.get("stato") == "confermata"]
        card_metrica("Confermate", len(conf), colore="#28A745")
    with col3:
        att  = [p for p in tutte if p.get("stato") == "in_attesa"]
        card_metrica("In Attesa", len(att), colore="#FFA500")
    with col4:
        confl = [p for p in tutte if p.get("stato") == "conflitto"]
        card_metrica("Conflitti", len(confl), colore="#FFC107")

    st.markdown("---")

    # Prenotazioni oggi
    oggi = date.today().isoformat()
    oggi_list = [
        p for p in tutte
        if any(s.get("data", "") == oggi for s in p.get("slots", []))
        and p.get("stato") == "confermata"
    ]
    st.subheader(f"📅 Prenotazioni di oggi ({len(oggi_list)})")
    if oggi_list:
        for p in oggi_list:
            slot_oggi = [s for s in p.get("slots", []) if s.get("data", "") == oggi]
            for s in slot_oggi:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.markdown(f"⏰ **{formato_ora(s['ora_inizio'])}-{formato_ora(s['ora_fine'])}**")
                with col2:
                    st.markdown(f"Aula {p['aula_id']} | Corso {p['corso_id']}")
                with col3:
                    mostra_stato_badge(p.get("stato", ""))
                st.divider()
    else:
        st.info("Nessuna prenotazione confermata per oggi.")


def _prenotazioni_sede():
    st.title("📅 Prenotazioni della Sede")
    sede_id = st.session_state.get("sede_id")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_stato = st.selectbox(
            "Stato",
            ["Tutti", "in_attesa", "confermata", "rifiutata", "conflitto"],
            format_func=lambda x: "Tutti" if x == "Tutti" else x.replace("_", " ").title()
        )
    with col2:
        data_dal = st.date_input("Dal", value=date.today())
    with col3:
        data_al  = st.date_input("Al",  value=date.today() + timedelta(days=30))

    lista = api_pren.get_prenotazioni(
        sede_id=sede_id,
        stato=filtro_stato if filtro_stato != "Tutti" else None,
        data_dal=data_dal.isoformat(),
        data_al=data_al.isoformat(),
    )

    st.caption(f"**{len(lista)}** prenotazioni trovate")
    st.markdown("---")

    if not lista:
        st.info("Nessuna prenotazione nel periodo selezionato.")
        return

    # Tabella riepilogativa
    import pandas as pd
    righe = []
    for p in lista:
        slots = p.get("slots", [])
        righe.append({
            "ID":      p["id"],
            "Tipo":    p.get("tipo", "").replace("_", " ").title(),
            "Aula":    p["aula_id"],
            "Corso":   p["corso_id"],
            "Stato":   p.get("stato", "").replace("_", " ").title(),
            "N. Slot": len(slots),
            "Primo slot": formato_data(slots[0]["data"]) if slots else "-",
        })

    df = pd.DataFrame(righe)
    st.dataframe(df, use_container_width=True, hide_index=True)


def _saturazione():
    st.title("📊 Saturazione Spazi")
    sede_id = st.session_state.get("sede_id")
    st.markdown("---")

    primo_mese, ultimo_mese = mese_corrente()
    lista_aule = aule.get_aule(sede_id=sede_id)

    if not lista_aule:
        st.warning("Nessuna aula disponibile.")
        return

    st.subheader(f"📅 Mese corrente: {primo_mese.strftime('%B %Y')}")

    # Per ogni aula calcola gli slot occupati nel mese
    import pandas as pd
    dati_saturazione = []
    for a in lista_aule:
        occupati = aule.get_slot_occupati(
            aula_id=a["id"],
            data_dal=primo_mese.isoformat(),
            data_al=ultimo_mese.isoformat(),
        )
        # Ore occupate totali
        ore_occ = sum(
            (
                int(s.get("ora_fine", "00:00")[:2]) * 60 +
                int(s.get("ora_fine", "00:00")[3:5]) -
                int(s.get("ora_inizio", "00:00")[:2]) * 60 -
                int(s.get("ora_inizio", "00:00")[3:5])
            ) / 60
            for s in occupati
        )
        dati_saturazione.append({
            "Aula":          a["nome"],
            "Capienza":      a["capienza"],
            "Slot occupati": len(occupati),
            "Ore occupate":  round(ore_occ, 1),
        })

    df = pd.DataFrame(dati_saturazione)

    # Metriche aggregate
    col1, col2 = st.columns(2)
    with col1:
        card_metrica("Aule totali", len(lista_aule))
    with col2:
        tot_slot = df["Slot occupati"].sum()
        card_metrica("Slot totali occupati nel mese", int(tot_slot), colore="#1E88E5")

    st.markdown("---")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Grafico a barre
    if not df.empty:
        import altair as alt
        chart = alt.Chart(df).mark_bar(color="#1E88E5").encode(
            x=alt.X("Aula:N", sort="-y"),
            y=alt.Y("Slot occupati:Q"),
            tooltip=["Aula", "Slot occupati", "Ore occupate"],
        ).properties(height=300, title="Slot occupati per aula nel mese corrente")
        st.altair_chart(chart, use_container_width=True)