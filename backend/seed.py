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
from datetime import date, time, datetime, timedelta


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
            Sede(nome="Via Livorno 49",   indirizzo="Via Livorno 49",    citta="Torino", capienza_massima=30),
            Sede(nome="Via Livorno 53 A", indirizzo="Via Livorno 53 A",  citta="Torino", capienza_massima=50),
            Sede(nome="Via Livorno 53 B", indirizzo="Via Livorno 53 B",  citta="Torino", capienza_massima=50),
            Sede(nome="Corso Svizzera",   indirizzo="C.so Svizzera 161", citta="Torino", capienza_massima=150),
            Sede(nome="Cuneo",            indirizzo="Via Roma 1",        citta="Cuneo",  capienza_massima=60),
            Sede(nome="Asti",             indirizzo="Corso Alba 10",     citta="Asti",   capienza_massima=80),
            Sede(nome="Novara",           indirizzo="Via Biglieri 5",    citta="Novara", capienza_massima=100),
            Sede(nome="Biella",           indirizzo="Via Galileo 3",     citta="Biella", capienza_massima=100),
        ]
        for s in sedi:
            db.add(s)
        db.flush()
        print(f"   ✅ {len(sedi)} sedi create")

        # Alias per leggibilità
        s_liv49, s_liv53a, s_liv53b, s_svizzera, s_cuneo, s_asti, s_novara, s_biella = sedi

        # ══════════════════════════════════════════════════════════════════════
        # AULE
        # ══════════════════════════════════════════════════════════════════════
        aule = [
            # Via Livorno 49 (1 aula)
            Aula(nome="Aula 1", capienza=20, sede_id=s_liv49.id),
            # Via Livorno 53 A (1 aula)
            Aula(nome="Aula 1", capienza=25, sede_id=s_liv53a.id),
            # Via Livorno 53 B (1 aula)
            Aula(nome="Aula 2", capienza=25, sede_id=s_liv53b.id),
            # Corso Svizzera (5 aule)
            Aula(nome="Aula 1", capienza=30, sede_id=s_svizzera.id),
            Aula(nome="Aula 2", capienza=30, sede_id=s_svizzera.id),
            Aula(nome="Aula 3", capienza=25, sede_id=s_svizzera.id),
            Aula(nome="Aula 4", capienza=25, sede_id=s_svizzera.id),
            Aula(nome="Aula 5", capienza=20, sede_id=s_svizzera.id),
            # Cuneo (2 aule)
            Aula(nome="Aula 1", capienza=30, sede_id=s_cuneo.id),
            Aula(nome="Aula 2", capienza=30, sede_id=s_cuneo.id),
            # Asti (3 aule)
            Aula(nome="Aula 1", capienza=25, sede_id=s_asti.id),
            Aula(nome="Aula 2", capienza=25, sede_id=s_asti.id),
            Aula(nome="Aula 3", capienza=25, sede_id=s_asti.id),
            # Novara (4 aule)
            Aula(nome="Aula 1", capienza=25, sede_id=s_novara.id),
            Aula(nome="Aula 2", capienza=25, sede_id=s_novara.id),
            Aula(nome="Aula 3", capienza=25, sede_id=s_novara.id),
            Aula(nome="Aula 4", capienza=25, sede_id=s_novara.id),
            # Biella (4 aule)
            Aula(nome="Aula 1", capienza=25, sede_id=s_biella.id),
            Aula(nome="Aula 2", capienza=25, sede_id=s_biella.id),
            Aula(nome="Aula 3", capienza=25, sede_id=s_biella.id),
            Aula(nome="Aula 4", capienza=25, sede_id=s_biella.id),
        ]
        for a in aule:
            db.add(a)
        db.flush()
        print(f"   ✅ {len(aule)} aule create")

        # Alias aule Corso Svizzera (usate nelle prenotazioni)
        a_sv1, a_sv2, a_sv3, a_sv4, a_sv5 = aule[3], aule[4], aule[5], aule[6], aule[7]
        a_cu1 = aule[8]
        a_as1 = aule[10]

        # ══════════════════════════════════════════════════════════════════════
        # UTENTI
        # ══════════════════════════════════════════════════════════════════════
        # Utenti principali per i test (uno per ruolo, tutti su Corso Svizzera)
        utenti = [
            # [0] Responsabile corso principale (Mario Rossi)
            Utente(nome="Mario",    cognome="Rossi",     email="responsabile@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_svizzera.id),
            # [1] Responsabile sede
            Utente(nome="Lucia",    cognome="Bianchi",   email="resp.sede@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_SEDE,    sede_id=s_svizzera.id),
            # [2] Segreteria sede
            Utente(nome="Giulia",   cognome="Verdi",     email="segr.sede@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_SEDE,      sede_id=s_svizzera.id),
            # [3] Segreteria didattica
            Utente(nome="Paolo",    cognome="Neri",      email="segr.did@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_DIDATTICA, sede_id=s_svizzera.id),
            # [4] Coordinamento (nessuna sede)
            Utente(nome="Anna",     cognome="Blu",       email="coord@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.COORDINAMENTO,        sede_id=None),
            # [5] Secondo responsabile corso (per simulare prenotazioni da utenti diversi)
            Utente(nome="Luca",     cognome="Ferrari",   email="responsabile2@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_svizzera.id),
            # [6] Responsabile sede Cuneo
            Utente(nome="Carla",    cognome="Esposito",  email="resp.cuneo@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_SEDE,    sede_id=s_cuneo.id),
            # [7] Segreteria sede Cuneo
            Utente(nome="Roberto",  cognome="Marino",    email="segr.cuneo@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_SEDE,      sede_id=s_cuneo.id),
            # [8] Responsabile corso Asti
            Utente(nome="Elena",    cognome="Conti",     email="resp.asti@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_asti.id),
        ]
        for u in utenti:
            db.add(u)
        db.flush()
        print(f"   ✅ {len(utenti)} utenti creati")

        mario    = utenti[0]
        giulia   = utenti[2]   # segreteria sede svizzera
        luca     = utenti[5]   # secondo resp. corso
        roberto  = utenti[7]   # segreteria sede cuneo
        elena    = utenti[8]   # resp. corso asti

        # ══════════════════════════════════════════════════════════════════════
        # CORSI
        # ══════════════════════════════════════════════════════════════════════
        corsi = [
            # [0] Corso GOL di Mario — ID 1
            Corso(codice="GOL-2025-001",
                  titolo="GOL - Orientamento al Lavoro (livello base)",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  responsabile_id=mario.id,
                  num_partecipanti=15,
                  data_inizio=date(2025, 1, 7),
                  data_fine=date(2025, 6, 30),
                  descrizione="Percorso GOL per disoccupati — livello base"),
            # [1] Corso FSE di Mario — ID 2
            Corso(codice="FSE-2025-001",
                  titolo="FSE - Competenze Digitali Avanzate",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  responsabile_id=mario.id,
                  num_partecipanti=20,
                  data_inizio=date(2025, 3, 3),
                  data_fine=date(2025, 9, 30),
                  descrizione="Corso FSE finanziato — competenze informatiche"),
            # [2] Corso IFTS di Mario — ID 3
            Corso(codice="IFTS-2025-001",
                  titolo="IFTS - Tecnico Superiore per l'Automazione",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  responsabile_id=mario.id,
                  num_partecipanti=25,
                  data_inizio=date(2025, 9, 15),
                  data_fine=date(2026, 6, 30),
                  descrizione="Percorso IFTS biennale"),
            # [3] Corso a pagamento di Luca — ID 4
            Corso(codice="PAG-2025-001",
                  titolo="Corso Excel Avanzato - Aziende",
                  tipo_finanziamento=TipoFinanziamento.A_PAGAMENTO,
                  responsabile_id=luca.id,
                  num_partecipanti=12,
                  data_inizio=date(2025, 2, 1),
                  data_fine=date(2025, 4, 30),
                  descrizione="Formazione Excel per aziende private"),
            # [4] Corso GOL di Elena (Asti) — ID 5
            Corso(codice="GOL-2025-002",
                  titolo="GOL - Orientamento al Lavoro (Asti)",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  responsabile_id=elena.id,
                  num_partecipanti=18,
                  data_inizio=date(2025, 2, 1),
                  data_fine=date(2025, 7, 31),
                  descrizione="Percorso GOL sede Asti"),
            # [5] Corso misto di Mario — ID 6
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

        c_gol   = corsi[0]   # ID 1
        c_fse   = corsi[1]   # ID 2
        c_ifts  = corsi[2]   # ID 3
        c_pag   = corsi[3]   # ID 4
        c_mix   = corsi[5]   # ID 6

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI CON TUTTI GLI STATI
        # Ogni prenotazione ha:
        #   - la Prenotazione stessa (tipo + stato)
        #   - i SlotOrario collegati
        #   - la RichiestaPrenotazione (con eventuale note_rifiuto)
        # ══════════════════════════════════════════════════════════════════════

        def crea_singola(aula, corso, richiedente, data, h_ini, h_fin,
                         stato_pren, stato_rich, note_rifiuto=None, note=None):
            """Helper: crea prenotazione singola + slot + richiesta."""
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
            r = RichiestaPrenotazione(
                prenotazione_id=p.id, stato=stato_rich,
                ha_conflitti=(stato_pren == StatoPrenotazione.CONFLITTO),
                note_rifiuto=note_rifiuto,
                segreteria_id=giulia.id if stato_rich in [StatoRichiesta.APPROVATA,
                                                           StatoRichiesta.RIFIUTATA] else None,
                data_gestione=datetime.utcnow() if stato_rich in [StatoRichiesta.APPROVATA,
                                                                    StatoRichiesta.RIFIUTATA] else None,
            )
            db.add(r); db.flush()
            return p

        def crea_massiva_slot(aula, corso, richiedente, date_list, h_ini, h_fin,
                              stato_pren, stato_rich, note_rifiuto=None, note=None):
            """Helper: crea prenotazione massiva + n slot + richiesta."""
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
            r = RichiestaPrenotazione(
                prenotazione_id=p.id, stato=stato_rich,
                ha_conflitti=(stato_pren == StatoPrenotazione.CONFLITTO),
                note_rifiuto=note_rifiuto,
                segreteria_id=giulia.id if stato_rich in [StatoRichiesta.APPROVATA,
                                                           StatoRichiesta.RIFIUTATA] else None,
                data_gestione=datetime.utcnow() if stato_rich in [StatoRichiesta.APPROVATA,
                                                                    StatoRichiesta.RIFIUTATA] else None,
            )
            db.add(r); db.flush()
            return p

        oggi = date.today()

        # ── Lunedì prossimo per calcoli ───────────────────────────────────────
        def lunedi_da(d, offset_settimane=0):
            """Restituisce il lunedì della settimana d + offset settimane."""
            lun = d - timedelta(days=d.weekday())
            return lun + timedelta(weeks=offset_settimane)

        lun0 = lunedi_da(oggi, 0)   # lunedì di questa settimana
        lun1 = lunedi_da(oggi, 1)   # lunedì prossima settimana
        lun2 = lunedi_da(oggi, 2)
        lun4 = lunedi_da(oggi, 4)
        lun8 = lunedi_da(oggi, 8)

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI CONFERMATE (storia passata + futuro pianificato)
        # ══════════════════════════════════════════════════════════════════════
        print("\n   📅 Creazione prenotazioni...")

        # 1. GOL mattina — confermata — Aula 1 Svizzera
        crea_singola(a_sv1, c_gol, mario,
                     oggi + timedelta(days=1), 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Prima sessione orientamento")

        # 2. FSE pomeriggio — confermata — Aula 2 Svizzera
        crea_singola(a_sv2, c_fse, mario,
                     oggi + timedelta(days=1), 14, 18,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Modulo competenze digitali")

        # 3. GOL massiva — 6 lunedì mattina — confermata — Aula 3 Svizzera
        lunedi_gol = [lun1 + timedelta(weeks=i) for i in range(6)]
        crea_massiva_slot(a_sv3, c_gol, mario,
                          lunedi_gol, 9, 13,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="Ciclo settimanale GOL — lunedì mattina")

        # 4. FSE massiva — 8 mercoledì pomeriggio — confermata — Aula 4 Svizzera
        mercoledi_fse = [lun1 + timedelta(days=2, weeks=i) for i in range(8)]
        crea_massiva_slot(a_sv4, c_fse, mario,
                          mercoledi_fse, 14, 18,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="FSE digitale — mercoledì pomeriggio")

        # 5. Corso misto — confermata — Aula 5 Svizzera
        crea_singola(a_sv5, c_mix, mario,
                     lun2, 9, 17,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Giornata intera — corso misto")

        # 6. Excel Luca — confermata — Aula 1 Svizzera (mattina diversa)
        crea_singola(a_sv1, c_pag, luca,
                     oggi + timedelta(days=3), 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Azienda TechCorp — prima sessione")

        # 7. Excel Luca massiva — 4 giovedì — confermata — Aula 2 Svizzera
        giovedi_excel = [lun1 + timedelta(days=3, weeks=i) for i in range(4)]
        crea_massiva_slot(a_sv2, c_pag, luca,
                          giovedi_excel, 14, 17,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="Moduli pomeridiani Excel avanzato")

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI IN ATTESA (da gestire dalla segreteria)
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

        # 11. Excel Luca in attesa (pomeriggio distinto)
        crea_singola(a_sv4, c_pag, luca,
                     lun4 + timedelta(days=2), 14, 17,
                     StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA,
                     note="Sessione extra Excel — mercoledì")

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI CON CONFLITTO
        # (stessa aula, stesso giorno, orario sovrapposto a una confermata)
        # ══════════════════════════════════════════════════════════════════════

        # 12. Conflitto su Aula 3 Svizzera — stesso giorno di #3 (lunedì 1)
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
        r_conf = RichiestaPrenotazione(
            prenotazione_id=p_conf.id,
            stato=StatoRichiesta.INVIATA,
            ha_conflitti=True,
        )
        db.add(r_conf); db.flush()

        # 13. Secondo conflitto — Aula 4, mercoledì 1
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
        r_conf2 = RichiestaPrenotazione(
            prenotazione_id=p_conf2.id,
            stato=StatoRichiesta.INVIATA,
            ha_conflitti=True,
        )
        db.add(r_conf2); db.flush()

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONI RIFIUTATE (con motivo — per testare Test 9)
        # ══════════════════════════════════════════════════════════════════════

        # 14. GOL rifiutata — Aula 5 già occupata in quella data
        crea_singola(a_sv5, c_gol, mario,
                     oggi - timedelta(days=7), 9, 13,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="Aula 5 già prenotata per attività istituzionale in quella giornata. Richiedere aula alternativa.",
                     note="Tentativo settimana scorsa")

        # 15. FSE rifiutata per capienza insufficiente
        crea_singola(a_sv1, c_fse, luca,
                     oggi - timedelta(days=3), 14, 18,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="Capienza Aula 1 insufficiente per 20 partecipanti FSE. Utilizzare Aula 2 o Aula 3.",
                     note="Richiesta capienza errata")

        # 16. IFTS rifiutata — data fuori periodo corso
        crea_singola(a_sv2, c_ifts, mario,
                     oggi - timedelta(days=14), 9, 17,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="La data richiesta è antecedente all'avvio ufficiale del percorso IFTS (15/09/2025). Prenotare da settembre in poi.",
                     note="Giornata intera IFTS — anticipata")

        # ══════════════════════════════════════════════════════════════════════
        # PRENOTAZIONE SEDE CUNEO (per test multi-sede)
        # ══════════════════════════════════════════════════════════════════════

        crea_singola(a_cu1, c_gol, elena,
                     lun1, 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="GOL Cuneo — avvio percorso")

        # massiva Asti
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
        print(f"   • {n_pren} prenotazioni  ({db.query(Prenotazione).filter_by(stato=StatoPrenotazione.CONFERMATA).count()} conf. / "
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