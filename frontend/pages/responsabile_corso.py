"""
Dashboard per il Responsabile Corso.
Funzioni: nuova prenotazione singola/massiva, visualizza proprie prenotazioni, slot disponibili.
"""

import streamlit as st
from datetime import date, timedelta
from frontend.api import sedi, aule, corsi, prenotazioni
from frontend.components.alerts import mostra_conflitto_warning, mostra_stato_badge, card_metrica
from frontend.utils.helpers import formato_data, formato_ora, stato_badge, giorni_da_numeri
from frontend.config import GIORNI_SETTIMANA, RICORRENZA_LABELS


def mostra(pagina: str):
    """Entry point: smista verso la sotto-pagina corretta."""
    if pagina == "dashboard":
        _dashboard()
    elif pagina == "nuova_prenotazione":
        _nuova_prenotazione()
    elif pagina == "prenotazione_massiva":
        _prenotazione_massiva()
    elif pagina == "mie_prenotazioni":
        _mie_prenotazioni()
    elif pagina == "slot_disponibili":
        _slot_disponibili()


# ── Dashboard ─────────────────────────────────────────────────────────────────

def _dashboard():
    nome = st.session_state.get("nome", "")
    st.title(f"👋 Benvenuto, {nome}!")
    st.markdown("---")

    # Carica prenotazioni dell'utente
    tutte = prenotazioni.get_prenotazioni()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metrica("Prenotazioni Totali", len(tutte), colore="#1E88E5")
    with col2:
        in_att = [p for p in tutte if p.get("stato") == "in_attesa"]
        card_metrica("In Attesa", len(in_att), colore="#FFA500")
    with col3:
        conf = [p for p in tutte if p.get("stato") == "confermata"]
        card_metrica("Confermate", len(conf), colore="#28A745")
    with col4:
        confl = [p for p in tutte if p.get("stato") == "conflitto"]
        card_metrica("Con Conflitti", len(confl), colore="#FFC107")

    st.markdown("---")
    st.subheader("📅 Prossime prenotazioni confermate")

    oggi = date.today().isoformat()
    prossime = [
        p for p in tutte
        if p.get("stato") == "confermata"
        and any(s.get("data", "") >= oggi for s in p.get("slots", []))
    ][:5]

    if prossime:
        for p in prossime:
            slots = p.get("slots", [])
            prossimo_slot = min(
                (s for s in slots if s.get("data", "") >= oggi),
                key=lambda s: s.get("data", ""),
                default=None
            )
            if prossimo_slot:
                with st.container():
                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        st.markdown(f"**Prenotazione #{p['id']}**")
                        st.caption(f"Aula ID: {p['aula_id']} | Corso ID: {p['corso_id']}")
                    with c2:
                        st.markdown(f"📅 {formato_data(prossimo_slot['data'])}")
                        st.caption(f"⏰ {formato_ora(prossimo_slot['ora_inizio'])} - {formato_ora(prossimo_slot['ora_fine'])}")
                    with c3:
                        mostra_stato_badge(p.get("stato", ""))
                    st.divider()
    else:
        st.info("Nessuna prenotazione confermata nel futuro prossimo.")

    st.markdown("---")
    st.markdown("**Azioni rapide:**")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ Nuova Prenotazione Singola", use_container_width=True):
            st.session_state["pagina_corrente"] = "nuova_prenotazione"
            st.rerun()
    with c2:
        if st.button("🔄 Nuova Prenotazione Massiva", use_container_width=True):
            st.session_state["pagina_corrente"] = "prenotazione_massiva"
            st.rerun()


# ── Nuova Prenotazione Singola ─────────────────────────────────────────────────

def _nuova_prenotazione():
    st.title("📅 Nuova Prenotazione Singola")
    st.markdown("---")

    # Carica dati per i select
    lista_sedi  = sedi.get_sedi()
    lista_corsi = corsi.get_corsi()

    if not lista_corsi:
        st.warning("⚠️ Nessun corso disponibile. Contatta la Segreteria Didattica.")
        return

    with st.form("form_prenotazione_singola"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📍 Aula")
            # Selezione sede
            sede_options = {s["nome"]: s["id"] for s in lista_sedi}
            sede_sel = st.selectbox("Sede", options=list(sede_options.keys()))
            sede_id  = sede_options.get(sede_sel)

            # Selezione aula basata sulla sede
            lista_aule = aule.get_aule(sede_id=sede_id) if sede_id else []
            if lista_aule:
                aula_options = {
                    f"{a['nome']} (cap. {a['capienza']})": a["id"]
                    for a in lista_aule
                }
                aula_sel = st.selectbox("Aula", options=list(aula_options.keys()))
                aula_id  = aula_options.get(aula_sel)
            else:
                st.warning("Nessuna aula disponibile per questa sede.")
                aula_id = None

        with col2:
            st.subheader("📚 Corso e Orario")
            # Selezione corso
            corso_options = {
                f"[{c['codice']}] {c['titolo']}": c["id"]
                for c in lista_corsi
            }
            corso_sel = st.selectbox("Corso", options=list(corso_options.keys()))
            corso_id  = corso_options.get(corso_sel)

            # Data e orario
            data_prenotazione = st.date_input(
                "Data", value=date.today() + timedelta(days=1),
                min_value=date.today()
            )
            col_ora1, col_ora2 = st.columns(2)
            with col_ora1:
                ora_inizio = st.time_input("Ora inizio", value=None)
            with col_ora2:
                ora_fine = st.time_input("Ora fine", value=None)

        note = st.text_area("Note (opzionale)", height=80)

        st.markdown("---")
        submitted = st.form_submit_button(
            "📤 Invia Richiesta", use_container_width=True
        )

    if submitted:
        # Validazioni
        if not aula_id:
            st.error("Seleziona un'aula.")
        elif not corso_id:
            st.error("Seleziona un corso.")
        elif not ora_inizio or not ora_fine:
            st.error("Inserisci l'orario completo.")
        elif ora_fine <= ora_inizio:
            st.error("L'ora di fine deve essere successiva all'ora di inizio.")
        else:
            with st.spinner("Invio richiesta in corso..."):
                risultato = prenotazioni.crea_prenotazione_singola(
                    aula_id=aula_id,
                    corso_id=corso_id,
                    data=data_prenotazione.isoformat(),
                    ora_inizio=ora_inizio.strftime("%H:%M:%S"),
                    ora_fine=ora_fine.strftime("%H:%M:%S"),
                    note=note if note else None,
                )

            if risultato:
                stato = risultato.get("stato", "")
                if stato == "conflitto":
                    st.warning(
                        "⚠️ **Richiesta inviata con conflitti.**\n\n"
                        "La Segreteria di Sede valuterà la situazione."
                    )
                else:
                    st.success(
                        f"✅ **Richiesta inviata con successo!** "
                        f"(Prenotazione #{risultato.get('id')})\n\n"
                        "La Segreteria di Sede la approverà a breve."
                    )


# ── Prenotazione Massiva ───────────────────────────────────────────────────────

def _prenotazione_massiva():
    st.title("🔄 Nuova Prenotazione Massiva")
    st.info(
        "💡 La prenotazione massiva genera automaticamente tutti gli slot ricorrenti. "
        "Es: ogni lunedì e mercoledì dalle 9:00 alle 12:00 da marzo a giugno."
    )
    st.markdown("---")

    lista_sedi  = sedi.get_sedi()
    lista_corsi = corsi.get_corsi()

    if not lista_corsi:
        st.warning("Nessun corso disponibile.")
        return

    with st.form("form_prenotazione_massiva"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📍 Aula")
            sede_options = {s["nome"]: s["id"] for s in lista_sedi}
            sede_sel = st.selectbox("Sede", options=list(sede_options.keys()), key="sede_mass")
            sede_id  = sede_options.get(sede_sel)

            lista_aule = aules = aule.get_aule(sede_id=sede_id) if sede_id else []
            if lista_aule:
                aula_options = {
                    f"{a['nome']} (cap. {a['capienza']})": a["id"]
                    for a in lista_aule
                }
                aula_sel = st.selectbox("Aula", options=list(aula_options.keys()), key="aula_mass")
                aula_id  = aula_options.get(aula_sel)
            else:
                aula_id = None

            st.subheader("📚 Corso")
            corso_options = {
                f"[{c['codice']}] {c['titolo']}": c["id"]
                for c in lista_corsi
            }
            corso_sel = st.selectbox("Corso", options=list(corso_options.keys()), key="corso_mass")
            corso_id  = corso_options.get(corso_sel)

        with col2:
            st.subheader("📅 Periodo e Orario")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                data_inizio = st.date_input(
                    "Dal", value=date.today() + timedelta(days=1),
                    min_value=date.today(), key="di_mass"
                )
            with col_d2:
                data_fine = st.date_input(
                    "Al", value=date.today() + timedelta(days=90),
                    min_value=date.today(), key="df_mass"
                )

            col_o1, col_o2 = st.columns(2)
            with col_o1:
                ora_inizio = st.time_input("Ora inizio", value=None, key="oi_mass")
            with col_o2:
                ora_fine = st.time_input("Ora fine", value=None, key="of_mass")

            st.subheader("🔄 Ricorrenza")
            tipo_ricorrenza = st.selectbox(
                "Tipo",
                options=list(RICORRENZA_LABELS.keys()),
                format_func=lambda x: RICORRENZA_LABELS[x],
                key="tipo_mass"
            )

            giorni_sel = st.multiselect(
                "Giorni della settimana",
                options=list(GIORNI_SETTIMANA.keys()),
                format_func=lambda x: GIORNI_SETTIMANA[x],
                default=[1],  # Lunedì di default
                key="giorni_mass"
            )

        note = st.text_area("Note (opzionale)", height=60, key="note_mass")

        if giorni_sel and data_inizio and data_fine:
            # Anteprima numero di occorrenze
            from datetime import timedelta as td
            n_settimane = (data_fine - data_inizio).days // 7 + 1
            stima = len(giorni_sel) * n_settimane
            st.info(f"📊 Stima approssimativa: circa **{stima} slot** verranno generati.")

        st.markdown("---")
        submitted = st.form_submit_button(
            "📤 Invia Richiesta Massiva", use_container_width=True
        )

    if submitted:
        if not aula_id:
            st.error("Seleziona un'aula.")
        elif not corso_id:
            st.error("Seleziona un corso.")
        elif not ora_inizio or not ora_fine:
            st.error("Inserisci l'orario completo.")
        elif ora_fine <= ora_inizio:
            st.error("L'ora di fine deve essere successiva all'ora di inizio.")
        elif not giorni_sel:
            st.error("Seleziona almeno un giorno della settimana.")
        elif data_fine <= data_inizio:
            st.error("La data di fine deve essere successiva alla data di inizio.")
        else:
            with st.spinner("Generazione slot e invio richiesta..."):
                risultato = prenotazioni.crea_prenotazione_massiva(
                    aula_id=aula_id,
                    corso_id=corso_id,
                    data_inizio=data_inizio.isoformat(),
                    data_fine=data_fine.isoformat(),
                    ora_inizio=ora_inizio.strftime("%H:%M:%S"),
                    ora_fine=ora_fine.strftime("%H:%M:%S"),
                    tipo_ricorrenza=tipo_ricorrenza,
                    giorni_settimana=giorni_sel,
                    note=note if note else None,
                )

            if risultato:
                n_slots = len(risultato.get("slots", []))
                stato   = risultato.get("stato", "")
                if stato == "conflitto":
                    st.warning(
                        f"⚠️ Richiesta massiva inviata con **{n_slots} slot** generati.\n\n"
                        "Sono stati rilevati alcuni conflitti. La Segreteria di Sede li gestirà."
                    )
                else:
                    st.success(
                        f"✅ Richiesta massiva inviata! **{n_slots} slot** generati.\n\n"
                        f"Prenotazione #{risultato.get('id')} in attesa di approvazione."
                    )


# ── Le Mie Prenotazioni ────────────────────────────────────────────────────────

def _mie_prenotazioni():
    st.title("📋 Le Mie Prenotazioni")
    st.markdown("---")

    # Filtri
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_stato = st.selectbox(
            "Filtra per stato",
            options=["Tutti", "in_attesa", "confermata", "rifiutata", "annullata", "conflitto"],
            format_func=lambda x: "Tutti" if x == "Tutti" else x.replace("_", " ").title()
        )
    with col2:
        data_dal = st.date_input("Dal", value=None, key="dal_mie")
    with col3:
        data_al  = st.date_input("Al",  value=None, key="al_mie")

    # Recupera prenotazioni
    lista = prenotazioni.get_prenotazioni(
        stato=filtro_stato if filtro_stato != "Tutti" else None,
        data_dal=data_dal.isoformat() if data_dal else None,
        data_al=data_al.isoformat()   if data_al  else None,
    )

    st.caption(f"**{len(lista)}** prenotazioni trovate")
    st.markdown("---")

    if not lista:
        st.info("Nessuna prenotazione trovata con i filtri selezionati.")
        return

    for p in lista:
        with st.expander(
            f"#{p['id']} | Aula {p['aula_id']} | Corso {p['corso_id']} | "
            f"{stato_badge(p.get('stato', ''))}",
            expanded=False
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Tipo:** {p.get('tipo', '').replace('_', ' ').title()}")
                st.markdown(f"**Creata il:** {formato_data(p.get('data_creazione', ''))}")
                if p.get("note"):
                    st.markdown(f"**Note:** {p['note']}")
            with col2:
                slots = p.get("slots", [])
                st.markdown(f"**Slot totali:** {len(slots)}")
                # Mostra i primi 5 slot
                for s in slots[:5]:
                    st.markdown(
                        f"• {formato_data(s['data'])} "
                        f"{formato_ora(s['ora_inizio'])} - {formato_ora(s['ora_fine'])}"
                    )
                if len(slots) > 5:
                    st.caption(f"... e altri {len(slots) - 5} slot")


# ── Slot Disponibili ───────────────────────────────────────────────────────────

def _slot_disponibili():
    st.title("🔍 Verifica Disponibilità Aula")
    st.markdown("---")

    lista_sedi = sedi.get_sedi()
    if not lista_sedi:
        st.warning("Nessuna sede disponibile.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        sede_options = {s["nome"]: s["id"] for s in lista_sedi}
        sede_sel = st.selectbox("Sede", options=list(sede_options.keys()), key="sede_disp")
        sede_id  = sede_options.get(sede_sel)
    with col2:
        lista_aule = aule.get_aule(sede_id=sede_id) if sede_id else []
        if lista_aule:
            aula_options = {
                f"{a['nome']} (cap. {a['capienza']})": a["id"]
                for a in lista_aule
            }
            aula_sel = st.selectbox("Aula", options=list(aula_options.keys()), key="aula_disp")
            aula_id  = aula_options.get(aula_sel)
        else:
            aula_id = None
            st.warning("Nessuna aula.")
    with col3:
        data_consulta = st.date_input(
            "Data da verificare",
            value=date.today() + timedelta(days=1),
            min_value=date.today()
        )

    if aula_id and data_consulta:
        if st.button("🔍 Verifica disponibilità", use_container_width=True):
            slot_occupati = aule.get_slot_occupati(
                aula_id=aula_id,
                data_dal=data_consulta.isoformat(),
                data_al=data_consulta.isoformat(),
            )

            st.markdown("---")
            if slot_occupati:
                st.warning(f"⚠️ **{len(slot_occupati)} slot occupati** il {formato_data(data_consulta)}:")
                for s in slot_occupati:
                    st.markdown(
                        f"🔴 `{formato_ora(s['ora_inizio'])} - {formato_ora(s['ora_fine'])}` "
                        f"(Prenotazione #{s.get('prenotazione_id', '?')})"
                    )
            else:
                st.success(
                    f"✅ **L'aula è completamente libera** il {formato_data(data_consulta)}!"
                )