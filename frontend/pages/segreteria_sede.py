"""
Dashboard per la Segreteria di Sede.
Funzioni: validazione richieste, gestione conflitti, calendario sede.
"""

import streamlit as st
from datetime import date, timedelta
from frontend.api import prenotazioni as api_pren, aule, sedi
from frontend.components.alerts import mostra_stato_badge, card_metrica
from frontend.utils.helpers import formato_data, formato_ora, stato_badge


def mostra(pagina: str):
    if pagina == "dashboard":
        _dashboard()
    elif pagina == "richieste_pendenti":
        _richieste_pendenti()
    elif pagina == "conflitti":
        _gestione_conflitti()
    elif pagina == "calendario_sede":
        _calendario_sede()
    elif pagina == "gestione_aule":
        _gestione_aule()


def _dashboard():
    st.title("📋 Dashboard Segreteria di Sede")
    sede_id = st.session_state.get("sede_id")
    st.markdown("---")

    tutte    = api_pren.get_prenotazioni(sede_id=sede_id)
    pendenti = [p for p in tutte if p.get("stato") == "in_attesa"]
    conflitti = [p for p in tutte if p.get("stato") == "conflitto"]
    confermate = [p for p in tutte if p.get("stato") == "confermata"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metrica("Totale Prenotazioni", len(tutte))
    with col2:
        card_metrica("Da Validare", len(pendenti), colore="#FFA500")
    with col3:
        card_metrica("Con Conflitti", len(conflitti), colore="#FFC107")
    with col4:
        card_metrica("Confermate", len(confermate), colore="#28A745")

    st.markdown("---")

    if pendenti:
        st.subheader(f"📥 Richieste da validare ({len(pendenti)})")
        for p in pendenti[:3]:
            _card_richiesta(p, compatta=True)
        if len(pendenti) > 3:
            if st.button(f"Vedi tutte le {len(pendenti)} richieste →"):
                st.session_state["pagina_corrente"] = "richieste_pendenti"
                st.rerun()
    else:
        st.success("✅ Nessuna richiesta in attesa di validazione.")

    if conflitti:
        st.markdown("---")
        st.subheader(f"⚠️ Prenotazioni con conflitti ({len(conflitti)})")
        for p in conflitti[:3]:
            _card_richiesta(p, compatta=True)


def _richieste_pendenti():
    st.title("📥 Richieste Pendenti")
    sede_id = st.session_state.get("sede_id")
    st.markdown("---")

    lista = api_pren.get_richieste_pendenti(sede_id=sede_id)

    if not lista:
        st.success("✅ Nessuna richiesta in attesa.")
        return

    st.info(f"**{len(lista)}** richieste da validare")

    for p in lista:
        _card_richiesta(p, compatta=False)


def _card_richiesta(p: dict, compatta: bool = False):
    """Renderizza una card per una prenotazione con azioni approva/rifiuta."""
    richiesta = p.get("richiesta") or {}
    richiesta_id = richiesta.get("id") if isinstance(richiesta, dict) else None

    slots  = p.get("slots", [])
    stato  = p.get("stato", "")
    ha_conflitti = richiesta.get("ha_conflitti", False) if isinstance(richiesta, dict) else False

    titolo = (
        f"{'⚠️' if ha_conflitti else '📄'} "
        f"Prenotazione #{p['id']} | "
        f"Aula {p['aula_id']} | Corso {p['corso_id']}"
    )

    with st.expander(titolo, expanded=not compatta):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.markdown(f"**Tipo:** {p.get('tipo', '').replace('_',' ').title()}")
            st.markdown(f"**Slot:** {len(slots)}")
            if slots:
                primo = slots[0]
                st.markdown(
                    f"**Primo slot:** {formato_data(primo['data'])} "
                    f"{formato_ora(primo['ora_inizio'])}-{formato_ora(primo['ora_fine'])}"
                )
            if p.get("note"):
                st.markdown(f"**Note:** {p['note']}")

        with col2:
            st.markdown(f"**Stato attuale:**")
            mostra_stato_badge(stato)
            if ha_conflitti:
                st.warning("⚠️ Conflitti rilevati")

        with col3:
            if richiesta_id:
                if st.button("✅ Approva", key=f"appr_{p['id']}", use_container_width=True):
                    with st.spinner("Approvazione..."):
                        esito = api_pren.approva_richiesta(richiesta_id)
                    if esito:
                        st.success("Approvata!")
                        st.rerun()

                motivo = st.text_input("Motivo rifiuto", key=f"mot_{p['id']}", placeholder="Inserisci motivo...")
                if st.button("❌ Rifiuta", key=f"rif_{p['id']}", use_container_width=True):
                    if not motivo:
                        st.error("Inserisci un motivo per il rifiuto.")
                    else:
                        with st.spinner("Rifiuto..."):
                            esito = api_pren.rifiuta_richiesta(richiesta_id, motivo)
                        if esito:
                            st.success("Rifiutata.")
                            st.rerun()
            else:
                st.caption("ID richiesta non disponibile")


def _gestione_conflitti():
    st.title("⚠️ Prenotazioni con Conflitti")
    sede_id = st.session_state.get("sede_id")
    st.markdown("---")

    lista = api_pren.get_prenotazioni_conflitto(sede_id=sede_id)

    if not lista:
        st.success("✅ Nessun conflitto attivo.")
        return

    st.warning(f"**{len(lista)}** prenotazioni con conflitti da gestire")
    st.info(
        "💡 Le prenotazioni con conflitto sono state comunque accettate dal sistema. "
        "Puoi approvarle ignorando il conflitto, oppure rifiutarle."
    )

    for p in lista:
        _card_richiesta(p, compatta=False)


def _calendario_sede():
    st.title("📅 Calendario Sede")
    sede_id = st.session_state.get("sede_id")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        data_dal = st.date_input("Dal", value=date.today())
    with col2:
        data_al  = st.date_input("Al",  value=date.today() + timedelta(days=7))

    lista = api_pren.get_prenotazioni(
        sede_id=sede_id,
        data_dal=data_dal.isoformat(),
        data_al=data_al.isoformat(),
    )

    st.caption(f"**{len(lista)}** prenotazioni nel periodo selezionato")
    st.markdown("---")

    # Raggruppa per data
    per_data: dict[str, list] = {}
    for p in lista:
        for s in p.get("slots", []):
            d = s.get("data", "")
            if data_dal.isoformat() <= d <= data_al.isoformat():
                per_data.setdefault(d, []).append({**p, "_slot": s})

    if not per_data:
        st.info("Nessuna prenotazione nel periodo selezionato.")
        return

    for giorno in sorted(per_data.keys()):
        st.subheader(f"📅 {formato_data(giorno)}")
        eventi = sorted(per_data[giorno], key=lambda x: x["_slot"].get("ora_inizio", ""))
        for e in eventi:
            s = e["_slot"]
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.markdown(
                    f"⏰ **{formato_ora(s['ora_inizio'])} - {formato_ora(s['ora_fine'])}**"
                )
            with col2:
                st.markdown(f"Aula {e['aula_id']} | Corso {e['corso_id']}")
            with col3:
                mostra_stato_badge(e.get("stato", ""))
        st.divider()


def _gestione_aule():
    st.title("🏢 Gestione Aule")
    sede_id = st.session_state.get("sede_id")
    st.markdown("---")

    lista = aule.get_aule(sede_id=sede_id)
    st.subheader(f"Aule della sede ({len(lista)})")

    if lista:
        for a in lista:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{a['nome']}**")
                if a.get("note"):
                    st.caption(a["note"])
            with col2:
                st.markdown(f"👥 Capienza: **{a['capienza']}**")
            with col3:
                st.markdown("🟢 Attiva" if a.get("attiva") else "🔴 Inattiva")
            st.divider()
    else:
        st.info("Nessuna aula per questa sede.")

    st.markdown("---")
    st.subheader("➕ Aggiungi Aula")
    with st.form("form_nuova_aula"):
        col1, col2 = st.columns(2)
        with col1:
            nome_aula = st.text_input("Nome aula", placeholder="Es: Aula 6")
        with col2:
            capienza  = st.number_input("Capienza", min_value=1, max_value=200, value=20)
        note_aula = st.text_input("Note (opzionale)")
        if st.form_submit_button("➕ Aggiungi"):
            if nome_aula and sede_id:
                r = aules_new = aule.crea_aula(nome_aula, capienza, sede_id, note_aula or None)
                if r:
                    st.success(f"✅ Aula '{nome_aula}' creata.")
                    st.rerun()