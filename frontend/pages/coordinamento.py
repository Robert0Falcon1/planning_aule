"""Dashboard per il Coordinamento: vista globale e report."""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from frontend.api import prenotazioni as api_pren, sedi as api_sedi, aule as api_aule
from frontend.api.client import post
from frontend.components.alerts import card_metrica
from frontend.utils.helpers import formato_data, stato_badge, mese_corrente


def mostra(pagina: str):
    if pagina == "dashboard":
        _dashboard()
    elif pagina == "vista_globale":
        _vista_globale()
    elif pagina == "report_saturazione":
        _report_saturazione()
    elif pagina == "gestione_utenti":
        _gestione_utenti()
    elif pagina == "gestione_sedi":
        _gestione_sedi()


def _dashboard():
    st.title("🎯 Dashboard Coordinamento")
    st.markdown("---")

    tutte       = api_pren.get_prenotazioni()
    lista_sedi  = api_sedi.get_sedi()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        card_metrica("Sedi attive", len(lista_sedi), colore="#1E88E5")
    with col2:
        card_metrica("Prenotazioni totali", len(tutte))
    with col3:
        conf = [p for p in tutte if p.get("stato") == "confermata"]
        card_metrica("Confermate", len(conf), colore="#28A745")
    with col4:
        att  = [p for p in tutte if p.get("stato") == "in_attesa"]
        card_metrica("In Attesa", len(att), colore="#FFA500")
    with col5:
        confl = [p for p in tutte if p.get("stato") == "conflitto"]
        card_metrica("Conflitti aperti", len(confl), colore="#FFC107")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 Prenotazioni per Sede")
        dati_sedi = []
        for s in lista_sedi:
            pren_sede = api_pren.get_prenotazioni(sede_id=s["id"])
            dati_sedi.append({
                "Sede":    s["nome"],
                "Città":   s["citta"],
                "Totale":  len(pren_sede),
                "Conf.":   len([p for p in pren_sede if p.get("stato") == "confermata"]),
                "Attesa":  len([p for p in pren_sede if p.get("stato") == "in_attesa"]),
            })
        if dati_sedi:
            st.dataframe(pd.DataFrame(dati_sedi), use_container_width=True, hide_index=True)

    with col2:
        st.subheader("📊 Distribuzione stati")
        from collections import Counter
        stati = Counter(p.get("stato", "") for p in tutte)
        if stati:
            df_stati = pd.DataFrame([
                {"Stato": k.replace("_", " ").title(), "Conteggio": v}
                for k, v in stati.items()
            ])
            st.dataframe(df_stati, use_container_width=True, hide_index=True)

            import altair as alt
            chart = alt.Chart(df_stati).mark_arc().encode(
                theta="Conteggio:Q",
                color="Stato:N",
                tooltip=["Stato", "Conteggio"],
            ).properties(height=200)
            st.altair_chart(chart, use_container_width=True)


def _vista_globale():
    st.title("🌐 Vista Globale Prenotazioni")
    st.markdown("---")

    lista_sedi = api_sedi.get_sedi()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sede_options = {"Tutte le sedi": None} | {s["nome"]: s["id"] for s in lista_sedi}
        sede_sel  = st.selectbox("Sede", options=list(sede_options.keys()))
        sede_id   = sede_options[sede_sel]
    with col2:
        filtro_stato = st.selectbox(
            "Stato",
            ["Tutti", "in_attesa", "confermata", "rifiutata", "annullata", "conflitto"],
            format_func=lambda x: "Tutti" if x == "Tutti" else x.replace("_", " ").title()
        )
    with col3:
        data_dal = st.date_input("Dal", value=date.today() - timedelta(days=30))
    with col4:
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
        st.info("Nessuna prenotazione trovata.")
        return

    righe = []
    for p in lista:
        slots = p.get("slots", [])
        righe.append({
            "ID":       p["id"],
            "Tipo":     p.get("tipo", "").replace("_", " ").title(),
            "Aula":     p["aula_id"],
            "Corso":    p["corso_id"],
            "Stato":    stato_badge(p.get("stato", "")),
            "N. Slot":  len(slots),
            "Dal":      formato_data(slots[0]["data"]) if slots else "-",
        })

    st.dataframe(pd.DataFrame(righe), use_container_width=True, hide_index=True)


def _report_saturazione():
    st.title("📊 Report Saturazione Spazi")
    st.markdown("---")

    primo, ultimo = mese_corrente()
    lista_sedi = api_sedi.get_sedi()

    col1, col2 = st.columns(2)
    with col1:
        data_dal = st.date_input("Dal", value=primo)
    with col2:
        data_al  = st.date_input("Al",  value=ultimo)

    if st.button("📊 Genera Report", use_container_width=True):
        dati = []
        with st.spinner("Calcolo saturazione in corso..."):
            for s in lista_sedi:
                lista_aule = api_aule.get_aule(sede_id=s["id"])
                for a in lista_aule:
                    occupati = api_aule.get_slot_occupati(
                        a["id"], data_dal.isoformat(), data_al.isoformat()
                    )
                    ore = sum(
                        (
                            int(sl.get("ora_fine","00:00")[:2])*60 +
                            int(sl.get("ora_fine","00:00")[3:5]) -
                            int(sl.get("ora_inizio","00:00")[:2])*60 -
                            int(sl.get("ora_inizio","00:00")[3:5])
                        ) / 60
                        for sl in occupati
                    )
                    dati.append({
                        "Sede":         s["nome"],
                        "Città":        s["citta"],
                        "Aula":         a["nome"],
                        "Capienza":     a["capienza"],
                        "Slot occupati": len(occupati),
                        "Ore occupate": round(ore, 1),
                    })

        if dati:
            df = pd.DataFrame(dati)
            st.markdown("---")

            # Metriche totali
            col1, col2, col3 = st.columns(3)
            with col1:
                card_metrica("Aule analizzate", len(df))
            with col2:
                card_metrica("Slot totali occupati", int(df["Slot occupati"].sum()))
            with col3:
                card_metrica("Ore totali occupate", round(df["Ore occupate"].sum(), 1))

            st.markdown("---")
            st.subheader("📋 Dettaglio per Aula")
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Grafico per sede
            st.subheader("📊 Ore occupate per Sede")
            df_sede = df.groupby("Sede")["Ore occupate"].sum().reset_index()
            import altair as alt
            chart = alt.Chart(df_sede).mark_bar(color="#1E88E5").encode(
                x=alt.X("Sede:N", sort="-y"),
                y=alt.Y("Ore occupate:Q"),
                tooltip=["Sede", "Ore occupate"],
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)

            # Export CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Scarica CSV",
                data=csv,
                file_name=f"report_saturazione_{data_dal}_{data_al}.csv",
                mime="text/csv",
                use_container_width=True,
            )


def _gestione_utenti():
    st.title("👥 Gestione Utenti")
    st.markdown("---")

    from frontend.api.client import get
    utenti = get("/utenti/") or []

    st.subheader(f"Utenti registrati ({len(utenti)})")
    if utenti:
        righe = [{
            "ID":      u["id"],
            "Nome":    f"{u['nome']} {u['cognome']}",
            "Email":   u["email"],
            "Ruolo":   u["ruolo"].replace("_", " ").title(),
            "Sede":    u.get("sede_id") or "—",
            "Attivo":  "✅" if u.get("attivo") else "❌",
        } for u in utenti]
        st.dataframe(pd.DataFrame(righe), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("➕ Crea Nuovo Utente")

    from frontend.models_enums import RUOLI_OPTIONS
    lista_sedi = api_sedi.get_sedi()

    with st.form("form_nuovo_utente"):
        col1, col2 = st.columns(2)
        with col1:
            nome_u    = st.text_input("Nome")
            cognome_u = st.text_input("Cognome")
            email_u   = st.text_input("Email")
        with col2:
            pwd_u  = st.text_input("Password", type="password")
            ruolo_u = st.selectbox(
                "Ruolo",
                options=["responsabile_corso","responsabile_sede",
                         "segreteria_sede","segreteria_didattica","coordinamento"],
                format_func=lambda x: x.replace("_", " ").title()
            )
            sede_options = {"Nessuna sede": None} | {s["nome"]: s["id"] for s in lista_sedi}
            sede_u_sel = st.selectbox("Sede", options=list(sede_options.keys()))
            sede_u_id  = sede_options[sede_u_sel]

        if st.form_submit_button("➕ Crea Utente"):
            if all([nome_u, cognome_u, email_u, pwd_u]):
                from frontend.api.client import post as api_post
                r = api_post("/utenti/", data={
                    "nome": nome_u, "cognome": cognome_u,
                    "email": email_u, "password": pwd_u,
                    "ruolo": ruolo_u, "sede_id": sede_u_id,
                })
                if r:
                    st.success(f"✅ Utente '{email_u}' creato.")
                    st.rerun()
            else:
                st.error("Compila tutti i campi obbligatori.")


def _gestione_sedi():
    st.title("🏢 Gestione Sedi")
    st.markdown("---")

    lista_sedi = api_sedi.get_sedi()

    st.subheader(f"Sedi attive ({len(lista_sedi)})")
    for s in lista_sedi:
        lista_aule = api_aule.get_aule(sede_id=s["id"])
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.markdown(f"**{s['nome']}** — {s['indirizzo']}, {s['citta']}")
        with col2:
            st.markdown(f"👥 Cap. max: **{s['capienza_massima']}**")
        with col3:
            st.markdown(f"🚪 Aule: **{len(lista_aule)}**")
        with col4:
            st.markdown("🟢 Attiva")
        st.divider()

    st.markdown("---")
    st.subheader("➕ Aggiungi Sede")
    with st.form("form_nuova_sede"):
        col1, col2 = st.columns(2)
        with col1:
            nome_s    = st.text_input("Nome sede", placeholder="Es: Alessandria")
            indirizzo = st.text_input("Indirizzo", placeholder="Es: Via Roma 1")
        with col2:
            citta     = st.text_input("Città")
            capienza  = st.number_input("Capienza massima", min_value=0, value=100)
        if st.form_submit_button("➕ Aggiungi Sede"):
            if nome_s and indirizzo and citta:
                r = api_sedi.crea_sede(nome_s, indirizzo, citta, capienza)
                if r:
                    st.success(f"✅ Sede '{nome_s}' creata.")
                    st.rerun()
            else:
                st.error("Compila tutti i campi obbligatori.")