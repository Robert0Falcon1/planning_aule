"""
Script di seeding del database con dati realistici.
Crea sedi, aule, utenti, corsi, docenti, allievi, lezioni e prenotazioni
in vari stati per test completi del sistema ICE 1.0.
Eseguire con: python -m backend.seed
"""

from backend.database import SessionLocal, crea_tabelle
from backend.core.security import hash_password
from backend.models import *
from backend.models.enums import (
    TipoFinanziamento, StatoCorso, OreAccertamento, TipoLezione,
    TipologiaDocente, Sesso, Cittadinanza, ResidenzaIn,
    LivelloIstruzione, CondizioneOccupazionale, DisabilitaVulnerabilita,
    SvantaggioAbitativo, StatoPrenotazione, StatoRichiesta, TipoRicorrenza,
)
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
            Sede(nome="Via Livorno 49",  indirizzo="Via Livorno 49",             citta="Torino", capienza_massima=34),
            Sede(nome="Via Livorno 53",  indirizzo="Via Livorno 53",             citta="Torino", capienza_massima=69),
            Sede(nome="Corso Svizzera",  indirizzo="C.so Svizzera 161",          citta="Torino", capienza_massima=99),
            Sede(nome="Cuneo",           indirizzo="Via Cascina Colombaro 26/D", citta="Cuneo",  capienza_massima=41),
            Sede(nome="Asti",            indirizzo="Piazza Roma 13",             citta="Asti",   capienza_massima=56),
            Sede(nome="Novara",          indirizzo="Via Porzio Giovanola 7",     citta="Novara", capienza_massima=95),
            Sede(nome="Biella",          indirizzo="Strada Campagnè 7/A",        citta="Biella", capienza_massima=96),
        ]
        for s in sedi:
            db.add(s)
        db.flush()
        print(f"   ✅ {len(sedi)} sedi create")

        s_liv49, s_liv53, s_svizzera, s_cuneo, s_asti, s_novara, s_biella = sedi

        # ══════════════════════════════════════════════════════════════════════
        # AULE
        # ══════════════════════════════════════════════════════════════════════
        aule = [
            Aula(nome="Aula 1",      capienza=25, sede_id=s_liv53.id),
            Aula(nome="Aula 2",      capienza=21, sede_id=s_liv53.id),
            Aula(nome="Aula Gialla",  capienza=18, sede_id=s_svizzera.id),
            Aula(nome="Aula Arancio", capienza=21, sede_id=s_svizzera.id),
            Aula(nome="Aula Verde",   capienza=25, sede_id=s_svizzera.id),
            Aula(nome="Aula Azzurra", capienza=20, sede_id=s_svizzera.id),
            Aula(nome="Aula Viola",   capienza=25, sede_id=s_svizzera.id),
            Aula(nome="Aula 1",      capienza=15, sede_id=s_cuneo.id),
            Aula(nome="Aula 1",      capienza=21, sede_id=s_asti.id),
            Aula(nome="Aula 2",      capienza=16, sede_id=s_asti.id),
            Aula(nome="Aula 1",      capienza=21, sede_id=s_novara.id),
            Aula(nome="Aula 2",      capienza=17, sede_id=s_novara.id),
            Aula(nome="Aula 3",      capienza=22, sede_id=s_novara.id),
            Aula(nome="Aula 1",      capienza=24, sede_id=s_biella.id),
            Aula(nome="Aula 2",      capienza=23, sede_id=s_biella.id),
            Aula(nome="Aula 3",      capienza=23, sede_id=s_biella.id),
            Aula(nome="Aula 4",      capienza=31, sede_id=s_biella.id),
        ]
        for a in aule:
            db.add(a)
        db.flush()
        print(f"   ✅ {len(aule)} aule create")

        a_sv1, a_sv2, a_sv3, a_sv4, a_sv5 = aule[2], aule[3], aule[4], aule[5], aule[6]
        a_cu1 = aule[7]
        a_as1 = aule[8]

        # ══════════════════════════════════════════════════════════════════════
        # UTENTI
        # ══════════════════════════════════════════════════════════════════════
        utenti = [
            # Responsabile Corso
            Utente(nome="Mario",   cognome="Rossi",    email="responsabile@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_svizzera.id),
            Utente(nome="Luca",    cognome="Ferrari",  email="responsabile2@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_svizzera.id),
            Utente(nome="Elena",   cognome="Conti",    email="resp.asti@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=s_asti.id),

            # Responsabile di Sede
            Utente(nome="Lucia",   cognome="Bianchi",  email="resp.sede@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.RESPONSABILE_SEDE,    sede_id=s_svizzera.id),
            Utente(nome="Carla",   cognome="Esposito", email="resp.cuneo@test.it",
                    password_hash=hash_password("test"),
                    ruolo=RuoloUtente.RESPONSABILE_SEDE,    sede_id=s_cuneo.id),

            # Segreteria di Sede
            Utente(nome="Giulia",  cognome="Verdi",    email="segr.sede@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_SEDE,      sede_id=s_svizzera.id),
            Utente(nome="Roberto", cognome="Marino",   email="segr.cuneo@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_SEDE,      sede_id=s_cuneo.id),

            # Segreteria Didattica
            Utente(nome="Paolo",   cognome="Neri",     email="segr.did@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.SEGRETERIA_DIDATTICA, sede_id=s_svizzera.id),

            # Coordinamento
            Utente(nome="Anna",    cognome="Blu",      email="coord@test.it",
                   password_hash=hash_password("test"),
                   ruolo=RuoloUtente.COORDINAMENTO,        sede_id=None),
        ]

        for u in utenti:
            db.add(u)
        db.flush()
        print(f"   ✅ {len(utenti)} utenti creati")

        mario  = utenti[0]
        giulia = utenti[2]
        luca   = utenti[5]
        elena  = utenti[8]

        # ══════════════════════════════════════════════════════════════════════
        # DOCENTI
        # ══════════════════════════════════════════════════════════════════════
        docenti = [
            Docente(nome="Francesca", cognome="Amato",
                    codice_fiscale="AMTFNC80A41L219X",
                    livello_istruzione=LivelloIstruzione.LAUREA_MAGISTRALE,
                    tipologia=TipologiaDocente.T,
                    webinar=False,
                    ore_di_incarico=120.0, ore_svolte=0.0,
                    unita_formative="Comunicazione efficace,Orientamento al lavoro"),
            Docente(nome="Giorgio",   cognome="Ferretti",
                    codice_fiscale="FRTGRG75C12F205K",
                    livello_istruzione=LivelloIstruzione.LAUREA_TRIENNALE,
                    tipologia=TipologiaDocente.P,
                    webinar=False,
                    ore_di_incarico=80.0,  ore_svolte=0.0,
                    unita_formative="Excel base,Excel avanzato,Power BI"),
            Docente(nome="Simona",    cognome="Ricci",
                    codice_fiscale="RCCSMN82D52G224P",
                    livello_istruzione=LivelloIstruzione.DIPLOMA_SUPERIORE,
                    tipologia=TipologiaDocente.S,
                    webinar=False,
                    ore_di_incarico=60.0,  ore_svolte=0.0,
                    unita_formative="Stage orientamento"),
            Docente(nome="Marco",     cognome="Testa",
                    codice_fiscale="TSTMRC90H10L219Q",
                    livello_istruzione=LivelloIstruzione.LAUREA_MAGISTRALE,
                    tipologia=TipologiaDocente.T,
                    webinar=True,         # Docente remoto
                    ore_di_incarico=40.0,  ore_svolte=0.0,
                    unita_formative="Python per l'automazione,Introduzione AI"),
        ]
        for d in docenti:
            db.add(d)
        db.flush()

        # Assegna sedi ai docenti
        docenti[0].sedi = [s_svizzera, s_cuneo]
        docenti[1].sedi = [s_svizzera]
        docenti[2].sedi = [s_svizzera, s_asti]
        docenti[3].sedi = [s_svizzera]   # webinar → sede formale
        db.flush()
        print(f"   ✅ {len(docenti)} docenti creati")

        # ══════════════════════════════════════════════════════════════════════
        # CORSI
        # ══════════════════════════════════════════════════════════════════════
        corsi = [
            # [0] GOL — Mario — Svizzera
            Corso(codice="GOL-2025-001",
                  titolo="GOL - Orientamento al Lavoro (livello base)",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  stato_del_corso=StatoCorso.IN_CORSO,
                  numero_proposta=1042,
                  id_corso_finanziato=1500234,
                  responsabile_id=mario.id,
                  sede_id=s_svizzera.id,
                  num_partecipanti=15,
                  ore_totali=120.0, ore_erogate=48.0,
                  ore_stage=0.0,
                  ore_selezione_allievi=4.0,
                  data_inizio_corso=date(2025, 1, 7),
                  data_fine_presunta=date(2025, 6, 30),
                  descrizione="Percorso GOL per disoccupati — livello base"),
            # [1] FSE — Mario — Svizzera
            Corso(codice="FSE-2025-001",
                  titolo="FSE - Competenze Digitali Avanzate",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  stato_del_corso=StatoCorso.IN_CORSO,
                  numero_proposta=2018,
                  id_corso_finanziato=1000891,
                  responsabile_id=mario.id,
                  sede_id=s_svizzera.id,
                  num_partecipanti=20,
                  ore_totali=80.0, ore_erogate=24.0,
                  ore_stage=0.0,
                  ore_aggiuntive=4.0,
                  data_inizio_corso=date(2025, 3, 3),
                  data_fine_presunta=date(2025, 9, 30),
                  descrizione="Corso FSE finanziato — competenze informatiche"),
            # [2] IFTS — Mario — Svizzera
            Corso(codice="IFTS-2025-001",
                  titolo="IFTS - Tecnico Superiore per l'Automazione",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  stato_del_corso=StatoCorso.APPROVATO,
                  responsabile_id=mario.id,
                  sede_id=s_svizzera.id,
                  num_partecipanti=25,
                  ore_totali=800.0, ore_erogate=0.0,
                  ore_stage=200.0,
                  data_inizio_corso=date(2025, 9, 15),
                  data_fine_presunta=date(2026, 6, 30),
                  descrizione="Percorso IFTS biennale"),
            # [3] A pagamento — Luca — Svizzera
            Corso(codice="PAG-2025-001",
                  titolo="Corso Excel Avanzato - Aziende",
                  tipo_finanziamento=TipoFinanziamento.A_PAGAMENTO,
                  stato_del_corso=StatoCorso.CONCLUSO,
                  responsabile_id=luca.id,
                  sede_id=s_svizzera.id,
                  num_partecipanti=12,
                  ore_totali=24.0, ore_erogate=24.0,
                  data_inizio_corso=date(2025, 2, 1),
                  data_fine_presunta=date(2025, 4, 30),
                  descrizione="Formazione Excel per aziende private"),
            # [4] GOL Asti — Elena
            Corso(codice="GOL-2025-002",
                  titolo="GOL - Orientamento al Lavoro (Asti)",
                  tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                  stato_del_corso=StatoCorso.IN_CORSO,
                  numero_proposta=1058,
                  id_corso_finanziato=1500402,
                  responsabile_id=elena.id,
                  sede_id=s_asti.id,
                  num_partecipanti=18,
                  ore_totali=120.0, ore_erogate=32.0,
                  ore_stage=0.0,
                  ore_selezione_allievi=3.0,
                  data_inizio_corso=date(2025, 2, 1),
                  data_fine_presunta=date(2025, 7, 31),
                  descrizione="Percorso GOL sede Asti"),
            # [5] Misto 2026 — Mario — Svizzera
            Corso(codice="MIX-2026-001",
                  titolo="Corso Misto - Formazione Continua",
                  tipo_finanziamento=TipoFinanziamento.MISTO,
                  stato_del_corso=StatoCorso.AVVIATO,
                  responsabile_id=mario.id,
                  sede_id=s_svizzera.id,
                  num_partecipanti=16,
                  ore_totali=60.0, ore_erogate=0.0,
                  data_inizio_corso=date(2026, 1, 12),
                  data_fine_presunta=date(2026, 12, 18),
                  descrizione="Percorso formazione continua anno 2026"),
        ]
        for c in corsi:
            db.add(c)
        db.flush()

        c_gol  = corsi[0]
        c_fse  = corsi[1]
        c_ifts = corsi[2]
        c_pag  = corsi[3]
        c_mix  = corsi[5]

        # Assegna docenti ai corsi
        c_gol.docenti  = [docenti[0], docenti[2]]   # Francesca (T) + Simona (S)
        c_fse.docenti  = [docenti[1], docenti[3]]   # Giorgio (P) + Marco webinar (T)
        c_pag.docenti  = [docenti[1]]               # Giorgio (P)
        c_mix.docenti  = [docenti[0]]               # Francesca (T)
        corsi[4].docenti = [docenti[0]]             # GOL Asti — Francesca
        db.flush()

        ids = [c.id for c in corsi]
        print(f"   ✅ {len(corsi)} corsi creati (ID: {', '.join(map(str, ids))})")

        # ══════════════════════════════════════════════════════════════════════
        # ALLIEVI
        # ══════════════════════════════════════════════════════════════════════
        allievi_gol = [
            Allievo(nome="Sara",     cognome="Colombo",
                    codice_fiscale="CLMSR A95C46L219Z",
                    data_nascita=date(1995, 3, 6),
                    sesso=Sesso.F,
                    cittadinanza=Cittadinanza.COMUNITARIA,
                    residente_in=ResidenzaIn.ITALIA,
                    comune_residenza="Torino", provincia_residenza="TO", cap="10125",
                    email="sara.colombo@mail.it",
                    data_iscrizione=date(2025, 1, 7),
                    data_inizio_frequenza=date(2025, 1, 7),
                    livello_istruzione=LivelloIstruzione.DIPLOMA_SUPERIORE,
                    condizione_occupazionale=CondizioneOccupazionale.DISOCCUPATO,
                    disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                    svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                    ore_erogate=48.0, ore_assenza=4.0,
                    posizione_registro_cartaceo=1),
            Allievo(nome="Ahmed",    cognome="Ben Ali",
                    codice_fiscale="BNLHMD88T10Z330K",
                    data_nascita=date(1988, 12, 10),
                    nazione_nascita="Tunisia", sesso=Sesso.M,
                    cittadinanza=Cittadinanza.EXTRA_COMUNITARIA, paese="Tunisia",
                    residente_in=ResidenzaIn.ITALIA,
                    comune_residenza="Torino", provincia_residenza="TO", cap="10152",
                    email="ahmed.benali@mail.it",
                    data_firma_patto_attivazione=date(2025, 1, 6),
                    data_iscrizione=date(2025, 1, 7),
                    data_inizio_frequenza=date(2025, 1, 7),
                    livello_istruzione=LivelloIstruzione.LICENZA_MEDIA,
                    condizione_occupazionale=CondizioneOccupazionale.DISOCCUPATO,
                    disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                    svantaggio_abitativo=SvantaggioAbitativo.SVANTAGGIO,
                   # ore_accertamento_stranieri=True,   # allievo straniero
                    ore_erogate=48.0, ore_assenza=8.0,
                    posizione_registro_cartaceo=2),
            Allievo(nome="Marta",    cognome="Ferrara",
                    codice_fiscale="FRRMRT 90D50H501P",
                    data_nascita=date(1990, 4, 10),
                    sesso=Sesso.F,
                    cittadinanza=Cittadinanza.COMUNITARIA,
                    residente_in=ResidenzaIn.ITALIA,
                    comune_residenza="Moncalieri", provincia_residenza="TO", cap="10024",
                    data_iscrizione=date(2025, 1, 7),
                    data_inizio_frequenza=date(2025, 1, 7),
                    livello_istruzione=LivelloIstruzione.LAUREA_TRIENNALE,
                    condizione_occupazionale=CondizioneOccupazionale.INOCCUPATO,
                    disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                    svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                    ore_erogate=48.0, ore_assenza=0.0,
                    posizione_registro_cartaceo=3),
        ]

        allievi_fse = [
            Allievo(nome="Davide",   cognome="Greco",
                    codice_fiscale="GRCDVD85M20L219R",
                    data_nascita=date(1985, 8, 20),
                    sesso=Sesso.M,
                    cittadinanza=Cittadinanza.COMUNITARIA,
                    residente_in=ResidenzaIn.ITALIA,
                    comune_residenza="Torino", provincia_residenza="TO", cap="10138",
                    email="davide.greco@azienda.it",
                    data_iscrizione=date(2025, 3, 3),
                    data_inizio_frequenza=date(2025, 3, 3),
                    livello_istruzione=LivelloIstruzione.LAUREA_MAGISTRALE,
                    condizione_occupazionale=CondizioneOccupazionale.OCCUPATO_DIPENDENTE,
                    disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                    svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                    ore_erogate=24.0, ore_assenza=0.0,
                    posizione_registro_cartaceo=1),
            Allievo(nome="Chiara",   cognome="Martini",
                    codice_fiscale="MRTCHR92P50L219Y",
                    data_nascita=date(1992, 9, 10),
                    sesso=Sesso.F,
                    cittadinanza=Cittadinanza.COMUNITARIA,
                    residente_in=ResidenzaIn.ITALIA,
                    comune_residenza="Collegno", provincia_residenza="TO", cap="10093",
                    data_iscrizione=date(2025, 3, 3),
                    data_inizio_frequenza=date(2025, 3, 3),
                    livello_istruzione=LivelloIstruzione.DIPLOMA_SUPERIORE,
                    condizione_occupazionale=CondizioneOccupazionale.OCCUPATO_AUTONOMO,
                    disabilita_vulnerabilita=DisabilitaVulnerabilita.DSA,
                    svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                    ore_erogate=24.0, ore_assenza=2.0,
                    posizione_registro_cartaceo=2),
        ]

        # Un allievo ritirato nel GOL per esempio
        allievo_ritirato = Allievo(
            nome="Fabio", cognome="Serra",
            codice_fiscale="SRRF BZ79A01H501W",
            data_nascita=date(1979, 1, 1),
            sesso=Sesso.M,
            cittadinanza=Cittadinanza.COMUNITARIA,
            residente_in=ResidenzaIn.ITALIA,
            comune_residenza="Torino", provincia_residenza="TO", cap="10100",
            data_iscrizione=date(2025, 1, 7),
            data_inizio_frequenza=date(2025, 1, 7),
            data_ritiro=date(2025, 2, 14),
            motivo_ritiro="Inserimento lavorativo",
            livello_istruzione=LivelloIstruzione.QUALIFICA_PROFESSIONALE,
            condizione_occupazionale=CondizioneOccupazionale.DISOCCUPATO,
            disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
            svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
            ore_erogate=20.0, ore_assenza=0.0,
            posizione_registro_cartaceo=4,
        )

        tutti_allievi = allievi_gol + allievi_fse + [allievo_ritirato]
        for al in tutti_allievi:
            db.add(al)
        db.flush()

        # Associa allievi ai corsi
        c_gol.allievi = allievi_gol + [allievo_ritirato]
        c_fse.allievi = allievi_fse
        db.flush()
        print(f"   ✅ {len(tutti_allievi)} allievi creati")

        # ══════════════════════════════════════════════════════════════════════
        # CATALOGO
        # ══════════════════════════════════════════════════════════════════════
        CATALOGO_DEFAULT = [
            Catalogo(
                stato=1,
                profilo_formativo="Addetto magazzino e logistica",
                tipologia_utilizzo_parziale=0,
                formazione_normata=0,
                tipologia="Profili professionali",
                sep="11. Trasporti e logistica",
                area_professionale="SERVIZI COMMERCIALI",
                sottoarea_professionale="TRASPORTI",
                codice_ada=(
                    "ADA.11.01.18 (ex ADA.13.128.383); "
                    "ADA.11.01.20 (ex ADA.13.128.385)"
                ),
                titolo_ada="Gestione attività di magazzino; Operazioni di movimentazione merci",
                competenze=(
                    "1 - Eseguire le operazioni di movimentazione delle merci\n"
                    "2 - Collaborare alla gestione del magazzino\n"
                    "3 - Collaborare alla gestione dei flussi delle merci"
                ),
                titolo_percorso="ADDETTO MAGAZZINO E LOGISTICA",
                titolo_attestato="Addetto magazzino e logistica",
                certificazione_uscita="QUALIFICA PROFESSIONALE",
                tipologia_prova_finale="Prova di agenzia validata, con commissione esterna",
                durata_prova_ore=12.00,
                prova_ingresso_orientamento="Colloquio motivazionale di orientamento",
                ore_corso_minime=200.00, ore_stage_minime=150.00,
                ore_corso_massime=500.00, ore_stage_massime=200.00,
                normativa_riferimento=(
                    "Ai sensi del D.Lgs. n. 13 del 16 gennaio 2013 e s.m.i."
                ),
                ore_assenza_massime=166.67,
                assegnazione_credito_ingresso=1,
                data_inizio_validita=date(2023, 7, 24),
                eta=">= 18",
                livello_minimo_scolarita="Scuola secondaria di I grado",
                obbligo_scolastico_assolto=1,
                esperienze_lavorative_pregresse="Non specificato",
                stato_occupazionale_ammesso="Indifferente",
            ),
        ]
        if db.query(Catalogo).count() == 0:
            for entry in CATALOGO_DEFAULT:
                db.add(entry)
            db.flush()
            print(f"   ✅ {len(CATALOGO_DEFAULT)} voci catalogo create")

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
        # PRENOTAZIONI
        # ══════════════════════════════════════════════════════════════════════
        print("\n   📅 Creazione prenotazioni...")

        crea_singola(a_sv1, c_gol, mario,
                     oggi + timedelta(days=1), 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Prima sessione orientamento")

        crea_singola(a_sv2, c_fse, mario,
                     oggi + timedelta(days=1), 14, 18,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Modulo competenze digitali")

        lunedi_gol = [lun1 + timedelta(weeks=i) for i in range(6)]
        crea_massiva_slot(a_sv3, c_gol, mario, lunedi_gol, 9, 13,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="Ciclo settimanale GOL — lunedì mattina")

        mercoledi_fse = [lun1 + timedelta(days=2, weeks=i) for i in range(8)]
        crea_massiva_slot(a_sv4, c_fse, mario, mercoledi_fse, 14, 18,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="FSE digitale — mercoledì pomeriggio")

        crea_singola(a_sv5, c_mix, mario, lun2, 9, 17,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Giornata intera — corso misto")

        crea_singola(a_sv1, c_pag, luca,
                     oggi + timedelta(days=3), 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="Azienda TechCorp — prima sessione")

        giovedi_excel = [lun1 + timedelta(days=3, weeks=i) for i in range(4)]
        crea_massiva_slot(a_sv2, c_pag, luca, giovedi_excel, 14, 17,
                          StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                          note="Moduli pomeridiani Excel avanzato")

        crea_singola(a_sv3, c_ifts, mario, lun4, 9, 13,
                     StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA,
                     note="Laboratorio IFTS — primo incontro")

        crea_singola(a_sv5, c_mix, mario,
                     lun4 + timedelta(days=1), 14, 18,
                     StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA)

        venerdi_gol = [lun4 + timedelta(days=4, weeks=i) for i in range(5)]
        crea_massiva_slot(a_sv1, c_gol, mario, venerdi_gol, 9, 13,
                          StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA,
                          note="Secondo ciclo GOL — venerdì mattina")

        crea_singola(a_sv4, c_pag, luca,
                     lun4 + timedelta(days=2), 14, 17,
                     StatoPrenotazione.IN_ATTESA, StatoRichiesta.INVIATA,
                     note="Sessione extra Excel — mercoledì")

        # Conflitti
        p_conf = PrenotazioneSingola(
            aula_id=a_sv3.id, corso_id=c_fse.id, richiedente_id=luca.id,
            stato=StatoPrenotazione.CONFLITTO,
            note="Richiesta sovrapposta — attende risoluzione segreteria",
        )
        db.add(p_conf); db.flush()
        db.add(SlotOrario(prenotazione_id=p_conf.id, data=lunedi_gol[0],
                           ora_inizio=time(10, 0), ora_fine=time(14, 0)))
        db.add(RichiestaPrenotazione(prenotazione_id=p_conf.id,
                                      stato=StatoRichiesta.INVIATA, ha_conflitti=True))
        db.flush()

        p_conf2 = PrenotazioneSingola(
            aula_id=a_sv4.id, corso_id=c_mix.id, richiedente_id=mario.id,
            stato=StatoPrenotazione.CONFLITTO,
            note="Sovrapposizione rilevata con FSE pomeriggio",
        )
        db.add(p_conf2); db.flush()
        db.add(SlotOrario(prenotazione_id=p_conf2.id, data=mercoledi_fse[0],
                           ora_inizio=time(13, 0), ora_fine=time(17, 0)))
        db.add(RichiestaPrenotazione(prenotazione_id=p_conf2.id,
                                      stato=StatoRichiesta.INVIATA, ha_conflitti=True))
        db.flush()

        # Rifiutate
        crea_singola(a_sv5, c_gol, mario,
                     oggi - timedelta(days=7), 9, 13,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="Aula Viola già prenotata per attività istituzionale.",
                     note="Tentativo settimana scorsa")

        crea_singola(a_sv1, c_fse, luca,
                     oggi - timedelta(days=3), 14, 18,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="Capienza Aula Gialla insufficiente per 20 partecipanti FSE.",
                     note="Richiesta capienza errata")

        crea_singola(a_sv2, c_ifts, mario,
                     oggi - timedelta(days=14), 9, 17,
                     StatoPrenotazione.RIFIUTATA, StatoRichiesta.RIFIUTATA,
                     note_rifiuto="Data antecedente all'avvio IFTS (15/09/2025). Prenotare da settembre.",
                     note="Giornata intera IFTS — anticipata")

        # Multi-sede
        crea_singola(a_cu1, c_gol, elena, lun1, 9, 13,
                     StatoPrenotazione.CONFERMATA, StatoRichiesta.APPROVATA,
                     note="GOL Cuneo — avvio percorso")

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
            db.add(SlotOrario(prenotazione_id=p_asti.id, data=d,
                               ora_inizio=time(9, 0), ora_fine=time(13, 0)))
        db.add(RichiestaPrenotazione(prenotazione_id=p_asti.id,
                                      stato=StatoRichiesta.INVIATA, ha_conflitti=False))
        db.flush()

        # ══════════════════════════════════════════════════════════════════════
        # LEZIONI (ultime settimane — già svolte)
        # ══════════════════════════════════════════════════════════════════════
        print("\n   📖 Creazione lezioni registro...")

        lezioni_gol = []
        for i, giorno_offset in enumerate([-28, -21, -14, -7]):
            data_lez = oggi + timedelta(days=giorno_offset)
            # Salta weekend
            if data_lez.weekday() >= 5:
                data_lez += timedelta(days=(7 - data_lez.weekday()))
            lez = Lezione(
                corso_id=c_gol.id,
                data=data_lez,
                ora_inizio=time(9, 0),
                ora_fine=time(13, 0),
                tipo_lezione=TipoLezione.NORMALE,
                si_ripete=(i == 0),   # La prima lezione è ricorrente
                numero_variazione=0,
                note=f"Lezione {i+1} — orientamento GOL",
            )
            db.add(lez)
            lezioni_gol.append(lez)
        db.flush()

        # Registra presenze: tutti tranne il ritirato nelle ultime 2 lezioni
        for lez in lezioni_gol:
            lez.allievi_presenti = [allievi_gol[0], allievi_gol[1], allievi_gol[2]]
        # Prima lezione: allievo ritirato era presente
        lezioni_gol[0].allievi_presenti.append(allievo_ritirato)
        lezioni_gol[1].allievi_presenti.append(allievo_ritirato)
        db.flush()

        # 1 lezione FAD per FSE
        lez_fad = Lezione(
            corso_id=c_fse.id,
            data=oggi - timedelta(days=10),
            ora_inizio=time(9, 0),
            ora_fine=time(13, 0),
            tipo_lezione=TipoLezione.FAD,
            si_ripete=False,
            numero_variazione=0,
            note="Modulo asincrono — piattaforma e-learning",
        )
        db.add(lez_fad); db.flush()
        lez_fad.allievi_presenti = allievi_fse

        # 1 lezione di recupero
        lez_recupero = Lezione(
            corso_id=c_gol.id,
            data=oggi - timedelta(days=3),
            ora_inizio=time(14, 0),
            ora_fine=time(17, 0),
            tipo_lezione=TipoLezione.RECUPERO_AMMINISTRATIVO_DIDATTICO,
            si_ripete=False,
            numero_variazione=1,
            note="Recupero lezione del 12/01 — maltempo",
        )
        db.add(lez_recupero); db.flush()
        lez_recupero.allievi_presenti = [allievi_gol[0], allievi_gol[2]]

        db.commit()

        # ══════════════════════════════════════════════════════════════════════
        # RIEPILOGO
        # ══════════════════════════════════════════════════════════════════════
        n_pren  = db.query(Prenotazione).count()
        n_slot  = db.query(SlotOrario).count()
        n_lez   = db.query(Lezione).count()
        n_doc   = db.query(Docente).count()
        n_all   = db.query(Allievo).count()

        print(f"\n✅ Seeding completato!")
        print(f"   • {n_pren} prenotazioni  ("
              f"{db.query(Prenotazione).filter_by(stato=StatoPrenotazione.CONFERMATA).count()} conf. / "
              f"{db.query(Prenotazione).filter_by(stato=StatoPrenotazione.IN_ATTESA).count()} attesa / "
              f"{db.query(Prenotazione).filter_by(stato=StatoPrenotazione.CONFLITTO).count()} conflitto / "
              f"{db.query(Prenotazione).filter_by(stato=StatoPrenotazione.RIFIUTATA).count()} rifiutata)")
        print(f"   • {n_slot} slot orari")
        print(f"   • {n_lez} lezioni registro  |  {n_doc} docenti  |  {n_all} allievi")

        print("\n📋 Credenziali di test:")
        for u in utenti:
            label = f"{u.ruolo.value:<25} ({u.nome} {u.cognome}"
            label += f", {db.query(Sede).get(u.sede_id).nome})" if u.sede_id else ")"
            print(f"   {u.email:<30} / test  → {label}")

        print("\n📚 Corsi disponibili:")
        for c in corsi:
            n_doc_c = len(c.docenti)
            n_all_c = len(c.allievi)
            print(f"   ID {c.id}: {c.codice} — {c.titolo[:45]:<45}  "
                  f"[{c.stato_del_corso.value}]  {n_doc_c}d/{n_all_c}a")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Errore durante il seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()