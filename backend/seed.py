"""
Script di seeding del database con dati realistici.
Crea sedi, aule, utenti, corsi e prenotazioni in vari stati per test completi.
Eseguire con: python -m backend.seed
"""

from backend.database import SessionLocal, crea_tabelle
from backend.core.security import hash_password
from backend.models import *
from backend.models.enums import (TipoFinanziamento, StatoPrenotazione,
                                   StatoRichiesta, TipoRicorrenza)
from backend.models.prenotazione import (PrenotazioneSingola, PrenotazioneMassiva,
                                          RichiestaPrenotazione)
from backend.models.slot_orario import SlotOrario
from datetime import date, time, datetime, timedelta, timezone


def seed():
    """Popola il database con dati realistici per test completi."""
    crea_tabelle()
    db = SessionLocal()

    try:
        if db.query(Sede).count() > 0:
            print("⚠️  Database già inizializzato. Seed saltato.")
            return

        print("🌱 Avvio seeding database...\n")

        # ══════════════════════════════════════════════════════════════════════
        # SEDI
        # ══════════════════════════════════════════════════════════════════════
        sedi = [
            Sede(nome="Via Livorno 49",  indirizzo="Via Livorno 49",             citta="Torino", capienza_massima=34),  # NO AULE + 15p
            Sede(nome="Via Livorno 53",  indirizzo="Via Livorno 53",             citta="Torino", capienza_massima=69),  # Aula 1: 25p Aula 2: 21p + 7pp
            Sede(nome="Corso Svizzera",  indirizzo="C.so Svizzera 161",          citta="Torino", capienza_massima=99),  # Aula Gialla: 18p Aula Arancio: 21p Aula Verde: 25p Aula Azzurra: 20p Aula Viola: 25p + 3pp
            Sede(nome="Cuneo",           indirizzo="Via Cascina Colombaro 26/D", citta="Cuneo",  capienza_massima=41),  # Aula 1: 15p + 2pp
            Sede(nome="Asti",            indirizzo="Piazza Roma 13",             citta="Asti",   capienza_massima=56),  # Aula 1: 21p Aula 2: 16p + 15p (sala polifunzionale) + 2pp
            Sede(nome="Novara",          indirizzo="Via Porzio Giovanola 7",     citta="Novara", capienza_massima=95),  # Aula 1: 21p Aula 2: 17p Aula 3: 22p + 3pp
            Sede(nome="Biella",          indirizzo="Strada Campagnè 7/A",        citta="Biella", capienza_massima=96),  # Aula 1: 24p Aula 2: 23p Aula 3: 23p Aula 4: 31p + 15p (personale) + 4pp
        ]
        for s in sedi:
            db.add(s)
        db.flush()
        print(f"   ✅ {len(sedi)} sedi create")

        # Alias per leggibilità
        s_liv49, s_liv53, s_svizzera, s_cuneo, s_asti, s_novara, s_biella = sedi

        # ══════════════════════════════════════════════════════════════════════
        # AULE
        # ══════════════════════════════════════════════════════════════════════
        aule = [
            # Via Livorno 49 → NO AULE

            # Via Livorno 53 (2 aule) → indici 0, 1
            Aula(nome="Aula 1", capienza=25, sede_id=s_liv53.id),
            Aula(nome="Aula 2", capienza=21, sede_id=s_liv53.id),

            # Corso Svizzera (5 aule con nomi cromatici) → indici 2, 3, 4, 5, 6
            Aula(nome="Aula Gialla",  capienza=18, sede_id=s_svizzera.id),
            Aula(nome="Aula Arancio", capienza=21, sede_id=s_svizzera.id),  # Informatica
            Aula(nome="Aula Verde",   capienza=25, sede_id=s_svizzera.id),
            Aula(nome="Aula Azzurra", capienza=20, sede_id=s_svizzera.id),
            Aula(nome="Aula Viola",   capienza=25, sede_id=s_svizzera.id),

            # Cuneo (1 aula) → indice 7
            Aula(nome="Aula 1", capienza=15, sede_id=s_cuneo.id),

            # Asti (2 aule) → indici 8, 9
            Aula(nome="Aula 1", capienza=21, sede_id=s_asti.id),
            Aula(nome="Aula 2", capienza=16, sede_id=s_asti.id),

            # Novara (3 aule) → indici 10, 11, 12
            Aula(nome="Aula 1", capienza=21, sede_id=s_novara.id),
            Aula(nome="Aula 2", capienza=17, sede_id=s_novara.id),
            Aula(nome="Aula 3", capienza=22, sede_id=s_novara.id),

            # Biella (4 aule) → indici 13, 14, 15, 16
            Aula(nome="Aula 1", capienza=24, sede_id=s_biella.id),
            Aula(nome="Aula 2", capienza=23, sede_id=s_biella.id),
            Aula(nome="Aula 3", capienza=23, sede_id=s_biella.id),
            Aula(nome="Aula 4", capienza=31, sede_id=s_biella.id),
        ]
        for a in aule:
            db.add(a)
        db.flush()
        print(f"   ✅ {len(aule)} aule create")

        # Alias aule
        a_sv1, a_sv2, a_sv3, a_sv4, a_sv5 = aule[2], aule[3], aule[4], aule[5], aule[6]
        a_cu1 = aule[7]
        a_as1 = aule[8]

        # ══════════════════════════════════════════════════════════════════════
        # UTENTI
        # ══════════════════════════════════════════════════════════════════════
        utenti = [
            # [0] Responsabile corso principale (Mario Rossi)
            Utente(nome="Mario",   cognome="Rossi",    email="responsabile@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_svizzera.id),
            # [1] Responsabile sede
            Utente(nome="Lucia",   cognome="Bianchi",  email="resp.sede@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_SEDE,    sede_id=s_svizzera.id),
            # [2] Segreteria sede
            Utente(nome="Giulia",  cognome="Verdi",    email="segr.sede@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_SEDE,      sede_id=s_svizzera.id),
            # [3] Segreteria didattica
            Utente(nome="Paolo",   cognome="Neri",     email="segr.did@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_DIDATTICA, sede_id=s_svizzera.id),
            # [4] Coordinamento (nessuna sede)
            Utente(nome="Anna",    cognome="Blu",      email="coord@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.COORDINAMENTO,        sede_id=None),
            # [5] Secondo responsabile corso
            Utente(nome="Luca",    cognome="Ferrari",  email="responsabile2@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_svizzera.id),
            # [6] Responsabile sede Cuneo
            Utente(nome="Carla",   cognome="Esposito", email="resp.cuneo@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_SEDE,    sede_id=s_cuneo.id),
            # [7] Segreteria sede Cuneo
            Utente(nome="Roberto", cognome="Marino",   email="segr.cuneo@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_SEDE,      sede_id=s_cuneo.id),
            # [8] Responsabile corso Asti
            Utente(nome="Elena",   cognome="Conti",    email="resp.asti@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_asti.id),
        ]
        for u in utenti:
            db.add(u)
        db.flush()
        print(f"   ✅ {len(utenti)} utenti creati")

        mario   = utenti[0]
        giulia  = utenti[2]
        luca    = utenti[5]
        roberto = utenti[7]
        elena   = utenti[8]

        # ══════════════════════════════════════════════════════════════════════
        # CORSI
        # ══════════════════════════════════════════════════════════════════════
        corsi = [
            # [0] Corso GOL di Mario
            Corso(codice="GOL-2025-001",
                  titolo="GOL - Orientamento al Lavoro (livello base)",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  responsabile_id=mario.id,
                  num_partecipanti=15,
                  data_inizio=date(2025, 1, 7),
                  data_fine=date(2025, 6, 30),
                  descrizione="Percorso GOL per disoccupati — livello base"),
            # [1] Corso FSE di Mario
            Corso(codice="FSE-2025-001",
                  titolo="FSE - Competenze Digitali Avanzate",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  responsabile_id=mario.id,
                  num_partecipanti=20,
                  data_inizio=date(2025, 3, 3),
                  data_fine=date(2025, 9, 30),
                  descrizione="Corso FSE finanziato — competenze informatiche"),
            # [2] Corso IFTS di Mario
            Corso(codice="IFTS-2025-001",
                  titolo="IFTS - Tecnico Superiore per l'Automazione",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  responsabile_id=mario.id,
                  num_partecipanti=25,
                  data_inizio=date(2025, 9, 15),
                  data_fine=date(2026, 6, 30),
                  descrizione="Percorso IFTS biennale"),
            # [3] Corso a pagamento di Luca
            Corso(codice="PAG-2025-001",
                  titolo="Corso Excel Avanzato - Aziende",
                  tipo_finanziamento=TipoFinanziamento.A_PAGAMENTO,
                  responsabile_id=luca.id,
                  num_partecipanti=12,
                  data_inizio=date(2025, 2, 1),
                  data_fine=date(2025, 4, 30),
                  descrizione="Formazione Excel per aziende private"),
            # [4] Corso GOL di Elena (Asti)
            Corso(codice="GOL-2025-002",
                  titolo="GOL - Orientamento al Lavoro (Asti)",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  responsabile_id=elena.id,
                  num_partecipanti=18,
                  data_inizio=date(2025, 2, 1),
                  data_fine=date(2025, 7, 31),
                  descrizione="Percorso GOL sede Asti"),
            # [5] Corso misto di Mario
            Corso(codice="MIX-2026-001",
                  titolo="Corso Misto - Formazione Continua",
                  tipo_finanziamento=TipoFinanziamento.MISTO,
                  responsabile_id=mario.id,
                  num_partecipanti=16,
                  data_inizio=date(2026, 1, 12),
                  data_fine=date(2026, 12, 18),
                  descrizione="Percorso formazione continua anno 2026"),
        ]
        for c in corsi:
            db.add(c)
        db.flush()

        ids = [c.id for c in corsi]
        print(f"   ✅ {len(corsi)} corsi creati (ID: {', '.join(map(str, ids))})")

        c_gol  = corsi[0]
        c_fse  = corsi[1]
        c_ifts = corsi[2]
        c_pag  = corsi[3]
        c_mix  = corsi[5]

        # ══════════════════════════════════════════════════════════════════════
        # HELPERS PRENOTAZIONI
        # ══════════════════════════════════════════════════════════════════════

        def now_naive():
            return datetime.now(timezone.utc).replace(tzinfo=None)

        def crea_singola(aula, corso, richiedente, data, h_ini, h_fin,
                         stato_pren, stato_rich, note_rifiuto=None, note=None):
            p = PrenotazioneSingola(
                aula_id=aula.id, corso_id=corso.id,
                richiedente_id=richiedente.id,
                stato=stato_pren, note=note,
            )
            db.add(p); db.flush()
            db.add(SlotOrario(
                prenotazione_id=p.id, data=data,
                ora_inizio=time(h_ini, 0), ora_fine=time(h_fin, 0),
            ))
            gestita = stato_rich in [StatoRichiesta.APPROVATA, StatoRichiesta.RIFIUTATA]
            r = RichiestaPrenotazione(
                prenotazione_id=p.id, stato=stato_rich,
                ha_conflitti=(stato_pren == StatoPrenotazione.CONFLITTO),
                note_rifiuto=note_rifiuto,
                segreteria_id=giulia.id if gestita else None,
                data_gestione=now_naive() if gestita else None,
            )
            db.add(r); db.flush()
            return p

        def crea_massiva_slot(aula, corso, richiedente, date_list, h_ini, h_fin,
                              stato_pren, stato_rich, note_rifiuto=None, note=None):
            p = PrenotazioneMassiva(
                aula_id=aula.id, corso_id=corso.id,
                richiedente_id=richiedente.id,
                stato=stato_pren, note=note,
                tipo_ricorrenza=TipoRicorrenza.SETTIMANALE,
                giorni_settimana=",".join(str(d.isoweekday()) for d in date_list[:1]),
                data_inizio_range=date_list[0],
                data_fine_range=date_list[-1],
            )
            db.add(p); db.flush()
            for d in date_list:
                db.add(SlotOrario(
                    prenotazione_id=p.id, data=d,
                    ora_inizio=time(h_ini, 0), ora_fine=time(h_fin, 0),
                ))
            gestita = stato_rich in [StatoRichiesta.APPROVATA, StatoRichiesta.RIFIUTATA]
            r = RichiestaPrenotazione(
                prenotazione_id=p.id, stato=stato_rich,
                ha_conflitti=(stato_pren == StatoPrenotazione.CONFLITTO),
                note_rifiuto=note_rifiuto,
                segreteria_id=giulia.id if gestita else None,
                data_gestione=now_naive() if gestita else None,
            )
            db.add(r); db.flush()
            return p

        oggi = date.today()

        def lunedi_da(d, offset_settimane=0):
            lun = d - timedelta(days=d.weekday())
            return lun + timedelta(weeks=offset_settimane)

        lun1 = lunedi_da(oggi, 1)
        lun2 = lunedi_da(oggi, 2)
        lun4 = lunedi_da(oggi, 4)

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI CONFERMATE
        # ══════════════════════════════════════════════════════════════════════
        print("\n   📅 Creazione prenotazioni...")

        # 1. GOL mattina — confermata — Aula Gialla Svizzera
        crea_singola(a_sv1, c_gol, mario,
                     oggi + timedelta(days=1), 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Prima sessione orientamento")

        # 2. FSE pomeriggio — confermata — Aula Arancio Svizzera
        crea_singola(a_sv2, c_fse, mario,
                     oggi + timedelta(days=1), 14, 18,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Modulo competenze digitali")

        # 3. GOL massiva — 6 lunedì mattina — confermata — Aula Verde Svizzera
        lunedi_gol = [lun1 + timedelta(weeks=i) for i in range(6)]
        crea_massiva_slot(a_sv3, c_gol, mario,
                          lunedi_gol, 9, 13,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="Ciclo settimanale GOL — lunedì mattina")

        # 4. FSE massiva — 8 mercoledì pomeriggio — confermata — Aula Azzurra Svizzera
        mercoledi_fse = [lun1 + timedelta(days=2, weeks=i) for i in range(8)]
        crea_massiva_slot(a_sv4, c_fse, mario,
                          mercoledi_fse, 14, 18,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="FSE digitale — mercoledì pomeriggio")

        # 5. Corso misto — confermata — Aula Viola Svizzera
        crea_singola(a_sv5, c_mix, mario,
                     lun2, 9, 17,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Giornata intera — corso misto")

        # 6. Excel Luca — confermata — Aula Gialla Svizzera
        crea_singola(a_sv1, c_pag, luca,
                     oggi + timedelta(days=3), 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Azienda TechCorp — prima sessione")

        # 7. Excel Luca massiva — 4 giovedì — confermata — Aula Arancio Svizzera
        giovedi_excel = [lun1 + timedelta(days=3, weeks=i) for i in range(4)]
        crea_massiva_slot(a_sv2, c_pag, luca,
                          giovedi_excel, 14, 17,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="Moduli pomeridiani Excel avanzato")

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI IN ATTESA
        # ══════════════════════════════════════════════════════════════════════

        # 8. IFTS singola in attesa
        crea_singola(a_sv3, c_ifts, mario,
                     lun4, 9, 13,
                     StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA,
                     note="Laboratorio IFTS — primo incontro")

        # 9. Misto pomeriggio in attesa
        crea_singola(a_sv5, c_mix, mario,
                     lun4 + timedelta(days=1), 14, 18,
                     StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA)

        # 10. GOL massiva futura in attesa — 5 venerdì
        venerdi_gol = [lun4 + timedelta(days=4, weeks=i) for i in range(5)]
        crea_massiva_slot(a_sv1, c_gol, mario,
                          venerdi_gol, 9, 13,
                          StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA,
                          note="Secondo ciclo GOL — venerdì mattina")

        # 11. Excel Luca in attesa
        crea_singola(a_sv4, c_pag, luca,
                     lun4 + timedelta(days=2), 14, 17,
                     StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA,
                     note="Sessione extra Excel — mercoledì")

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI CON CONFLITTO
        # ══════════════════════════════════════════════════════════════════════

        # 12. Conflitto su Aula Verde — stesso giorno di #3
        p_conf = PrenotazioneSingola(
            aula_id=a_sv3.id, corso_id=c_fse.id,
            richiedente_id=luca.id,
            stato=StatoPrenotazione.CONFLITTO,
            note="Richiesta sovrapposta — attende risoluzione segreteria",
        )
        db.add(p_conf); db.flush()
        db.add(SlotOrario(
            prenotazione_id=p_conf.id, data=lunedi_gol[0],
            ora_inizio=time(10, 0), ora_fine=time(14, 0),
        ))
        db.add(RichiestaPrenotazione(
            prenotazione_id=p_conf.id,
            stato=StatoRichiesta.INVIATA,
            ha_conflitti=True,
        ))
        db.flush()

        # 13. Conflitto su Aula Azzurra — mercoledì 1
        p_conf2 = PrenotazioneSingola(
            aula_id=a_sv4.id, corso_id=c_mix.id,
            richiedente_id=mario.id,
            stato=StatoPrenotazione.CONFLITTO,
            note="Sovrapposizione rilevata con FSE pomeriggio",
        )
        db.add(p_conf2); db.flush()
        db.add(SlotOrario(
            prenotazione_id=p_conf2.id, data=mercoledi_fse[0],
            ora_inizio=time(13, 0), ora_fine=time(17, 0),
        ))
        db.add(RichiestaPrenotazione(
            prenotazione_id=p_conf2.id,
            stato=StatoRichiesta.INVIATA,
            ha_conflitti=True,
        ))
        db.flush()

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI RIFIUTATE
        # ══════════════════════════════════════════════════════════════════════

        # 14. GOL rifiutata
        crea_singola(a_sv5, c_gol, mario,
                     oggi - timedelta(days=7), 9, 13,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="Aula Viola già prenotata per attività istituzionale. Richiedere aula alternativa.",
                     note="Tentativo settimana scorsa")

        # 15. FSE rifiutata per capienza
        crea_singola(a_sv1, c_fse, luca,
                     oggi - timedelta(days=3), 14, 18,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="Capienza Aula Gialla insufficiente per 20 partecipanti FSE. Utilizzare Aula Verde o Aula Viola.",
                     note="Richiesta capienza errata")

        # 16. IFTS rifiutata — data fuori periodo
        crea_singola(a_sv2, c_ifts, mario,
                     oggi - timedelta(days=14), 9, 17,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="La data è antecedente all'avvio ufficiale del percorso IFTS (15/09/2025). Prenotare da settembre.",
                     note="Giornata intera IFTS — anticipata")

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI MULTI-SEDE
        # ══════════════════════════════════════════════════════════════════════

        # Cuneo — confermata
        crea_singola(a_cu1, c_gol, elena,
                     lun1, 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="GOL Cuneo — avvio percorso")

        # Asti massiva — in attesa
        martedi_asti = [lun1 + timedelta(days=1, weeks=i) for i in range(4)]
        p_asti = PrenotazioneMassiva(
            aula_id=a_as1.id, corso_id=corsi[4].id,
            richiedente_id=elena.id,
            stato=StatoPrenotazione.IN_ATTESA,
            tipo_ricorrenza=TipoRicorrenza.SETTIMANALE,
            giorni_settimana="2",
            data_inizio_range=martedi_asti[0],
            data_fine_range=martedi_asti[-1],
            note="GOL Asti — martedì mattina",
        )
        db.add(p_asti); db.flush()
        for d in martedi_asti:
            db.add(SlotOrario(
                prenotazione_id=p_asti.id, data=d,
                ora_inizio=time(9, 0), ora_fine=time(13, 0),
            ))
        db.add(RichiestaPrenotazione(
            prenotazione_id=p_asti.id,
            stato=StatoRichiesta.INVIATA,
            ha_conflitti=False,
        ))
        db.flush()

        db.commit()

        # ══════════════════════════════════════════════════════════════════════
        # RIEPILOGO
        # ══════════════════════════════════════════════════════════════════════
        n_pren = db.query(Prenotazione).count()
        n_slot = db.query(SlotOrario).count()

        print(f"\n✅ Seeding completato!")
        print(f"   • {n_pren} prenotazioni  ("
              f"{db.query(Prenotazione).filter_by(stato=StatoPrenotazione.CONFERMATA).count()} conf. / "
              f"{db.query(Prenotazione).filter_by(stato=StatoPrenotazione.IN_ATTESA).count()} attesa / "
              f"{db.query(Prenotazione).filter_by(stato=StatoPrenotazione.CONFLITTO).count()} conflitto / "
              f"{db.query(Prenotazione).filter_by(stato=StatoPrenotazione.RIFIUTATA).count()} rifiutata)")
        print(f"   • {n_slot} slot orari totali")

        print("\n📋 Credenziali di test:")
        print("   responsabile@test.it   / test  → Responsabile Corso (Mario Rossi, Corso Svizzera)")
        print("   responsabile2@test.it  / test  → Responsabile Corso (Luca Ferrari, Corso Svizzera)")
        print("   resp.sede@test.it      / test  → Responsabile Sede  (Corso Svizzera)")
        print("   segr.sede@test.it      / test  → Segreteria Sede    (Corso Svizzera)")
        print("   segr.did@test.it       / test  → Segreteria Didattica (Corso Svizzera)")
        print("   coord@test.it          / test  → Coordinamento      (tutte le sedi)")
        print("   resp.cuneo@test.it     / test  → Responsabile Sede  (Cuneo)")
        print("   segr.cuneo@test.it     / test  → Segreteria Sede    (Cuneo)")
        print("   resp.asti@test.it      / test  → Responsabile Corso (Asti)")

        print("\n📚 Corsi disponibili:")
        for c in corsi:
            print(f"   ID {c.id}: {c.codice} — {c.titolo[:55]}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Errore durante il seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()