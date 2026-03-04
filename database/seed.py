"""
Script di seeding COMPLETO per sistema 2 RUOLI - BASATO SU DATI REALI
Eseguire con: python -m database.seed
"""

from backend.database import SessionLocal, crea_tabelle
from backend.core.security import hash_password
from backend.models.sede import Sede
from backend.models.aula import Aula
from backend.models.utente import Utente
from backend.models.docente import Docente
from backend.models.corso import Corso
from backend.models.allievo import Allievo
from backend.models.prenotazione import Prenotazione, RichiestaPrenotazione
from backend.models.slot_orario import SlotOrario
from backend.models.enums import (
    RuoloUtente, TipoFinanziamento, StatoCorso, StatoPrenotazione, 
    StatoRichiesta, TipologiaDocente, 
    Sesso, Cittadinanza, ResidenzaIn, LivelloIstruzione, 
    CondizioneOccupazionale, DisabilitaVulnerabilita, SvantaggioAbitativo,
    TipoPrenotazione
)
from datetime import date, time, datetime, timedelta, timezone


def seed():
    """Popola database con dati reali del backup - adattati al sistema 2 ruoli"""
    crea_tabelle()
    db = SessionLocal()

    try:
        if db.query(Sede).count() > 0:
            print("⚠️  Database già inizializzato. Seed saltato.")
            return

        print("🌱 Seeding database ICE 1.0 - Sistema 2 RUOLI - DATI REALI\n")

        # ══════════════════════════════════════════════════════════════
        # SEDI (7 - come nel backup)
        # ══════════════════════════════════════════════════════════════
        sedi = [
            Sede(nome="Via Livorno 49", indirizzo="Via Livorno 49", citta="Torino", capienza_massima=34),
            Sede(nome="Via Livorno 53", indirizzo="Via Livorno 53", citta="Torino", capienza_massima=69),
            Sede(nome="Corso Svizzera", indirizzo="C.so Svizzera 161", citta="Torino", capienza_massima=99),
            Sede(nome="Cuneo", indirizzo="Via Cascina Colombaro 26/D", citta="Cuneo", capienza_massima=41),
            Sede(nome="Asti", indirizzo="Piazza Roma 13", citta="Asti", capienza_massima=56),
            Sede(nome="Novara", indirizzo="Via Porzio Giovanola 7", citta="Novara", capienza_massima=95),
            Sede(nome="Biella", indirizzo="Strada Campagnè 7/A", citta="Biella", capienza_massima=96),
        ]
        for s in sedi:
            db.add(s)
        db.flush()
        print(f"   ✅ {len(sedi)} sedi create")

        s_livorno49, s_livorno53, s_svizzera, s_cuneo, s_asti, s_novara, s_biella = sedi

        # ══════════════════════════════════════════════════════════════
        # AULE (17 - come nel backup)
        # ══════════════════════════════════════════════════════════════
        aule = [
            # Via Livorno 53 (2 aule)
            Aula(nome="Aula 1", capienza=25, sede_id=s_livorno53.id),
            Aula(nome="Aula 2", capienza=21, sede_id=s_livorno53.id),
            
            # Corso Svizzera (5 aule)
            Aula(nome="Aula Gialla", capienza=18, sede_id=s_svizzera.id),
            Aula(nome="Aula Arancio", capienza=21, sede_id=s_svizzera.id),
            Aula(nome="Aula Verde", capienza=25, sede_id=s_svizzera.id),
            Aula(nome="Aula Azzurra", capienza=20, sede_id=s_svizzera.id),
            Aula(nome="Aula Viola", capienza=25, sede_id=s_svizzera.id),
            
            # Cuneo (1 aula)
            Aula(nome="Aula 1", capienza=15, sede_id=s_cuneo.id),
            
            # Asti (2 aule)
            Aula(nome="Aula 1", capienza=21, sede_id=s_asti.id),
            Aula(nome="Aula 2", capienza=16, sede_id=s_asti.id),
            
            # Novara (3 aule)
            Aula(nome="Aula 1", capienza=21, sede_id=s_novara.id),
            Aula(nome="Aula 2", capienza=17, sede_id=s_novara.id),
            Aula(nome="Aula 3", capienza=22, sede_id=s_novara.id),
            
            # Biella (4 aule)
            Aula(nome="Aula 1", capienza=24, sede_id=s_biella.id),
            Aula(nome="Aula 2", capienza=23, sede_id=s_biella.id),
            Aula(nome="Aula 3", capienza=23, sede_id=s_biella.id),
            Aula(nome="Aula 4", capienza=31, sede_id=s_biella.id),
        ]
        for a in aule:
            db.add(a)
        db.flush()
        print(f"   ✅ {len(aule)} aule create")

        # ══════════════════════════════════════════════════════════════
        # UTENTI (9 - mappati al sistema 2 ruoli)
        # ══════════════════════════════════════════════════════════════
        # MAPPING RUOLI:
        # - RESPONSABILE_CORSO → OPERATIVO
        # - RESPONSABILE_SEDE → OPERATIVO
        # - SEGRETERIA_SEDE → OPERATIVO
        # - SEGRETERIA_DIDATTICA → OPERATIVO
        # - COORDINAMENTO → COORDINAMENTO
        
        utenti = [
            # Ex RESPONSABILE_CORSO → OPERATIVO
            Utente(
                nome="Mario", cognome="Rossi",
                email="responsabile@test.it",
                password_hash="$2b$12$O1vmnNsw7qDKKyOcgzZepeGluqy2NxfW7MXbZCNwklnDb0CTossNS",
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_svizzera.id,
                attivo=True
            ),
            Utente(
                nome="Luca", cognome="Ferrari",
                email="responsabile2@test.it",
                password_hash="$2b$12$QBOCBUF0JQ35pJfxPyGnp.OP0n3i0oUbdEROPD2CLP2TuH5Vmmqhi",
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_svizzera.id,
                attivo=True
            ),
            Utente(
                nome="Elena", cognome="Conti",
                email="resp.asti@test.it",
                password_hash="$2b$12$iack.Lp9HqqJKKki3ZrA1eLUJHvmoO0aImR7vfGvxYGx2O2shorY2",
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_asti.id,
                attivo=True
            ),
            
            # Ex RESPONSABILE_SEDE → OPERATIVO
            Utente(
                nome="Lucia", cognome="Bianchi",
                email="resp.sede@test.it",
                password_hash="$2b$12$MlG2wwNWH/4wB0/1e5Oa.OZFTmdldRenXr7V.SPWQbqFT6.ywNPSW",
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_svizzera.id,
                attivo=True
            ),
            Utente(
                nome="Carla", cognome="Esposito",
                email="resp.cuneo@test.it",
                password_hash="$2b$12$7xv6pG2LbfmQ4Cs5GK2KzufI1Zub/TEfvkaB3t8FddMq20EOdWica",
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_cuneo.id,
                attivo=True
            ),
            
            # Ex SEGRETERIA_SEDE → OPERATIVO
            Utente(
                nome="Giulia", cognome="Verdi",
                email="segr.sede@test.it",
                password_hash="$2b$12$zM0Il2hNhhfASvtE9w6qa.qUf6h7fozOOGc1Bh3QclwCiG1vBUO4y",
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_svizzera.id,
                attivo=True
            ),
            Utente(
                nome="Roberto", cognome="Marino",
                email="segr.cuneo@test.it",
                password_hash="$2b$12$4Wmc6uG0/ZlF0gqxAIF5TO5gaORlWqgyBPa8Pv4qSaeqWwAbnf7GO",
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_cuneo.id,
                attivo=True
            ),
            
            # Ex SEGRETERIA_DIDATTICA → OPERATIVO
            Utente(
                nome="Paolo", cognome="Neri",
                email="segr.did@test.it",
                password_hash="$2b$12$15AK04TCYSkNbg4PbOqtaec/SgoLQ.xVXckbmldrGSmXwxLQBOg36",
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_svizzera.id,
                attivo=True
            ),
            
            # COORDINAMENTO → COORDINAMENTO
            Utente(
                nome="Anna", cognome="Blu",
                email="coord@test.it",
                password_hash="$2b$12$/CowKRayXfkwNQgEd6rxlOneDFmwnN0J9FgvJVWj0FNNqIAQ.1TUe",
                ruolo=RuoloUtente.COORDINAMENTO,
                sede_id=None,
                attivo=True
            ),
        ]
        for u in utenti:
            db.add(u)
        db.flush()
        print(f"   ✅ {len(utenti)} utenti creati (8 OPERATIVI + 1 COORDINAMENTO)")

        mario, luca, elena, lucia, carla, giulia, roberto, paolo, anna = utenti

        # ══════════════════════════════════════════════════════════════
        # DOCENTI (4 - come nel backup)
        # ══════════════════════════════════════════════════════════════
        docenti = [
            Docente(
                nome="Francesca", cognome="Amato",
                codice_fiscale="AMTFNC80A41L219X",
                livello_istruzione=LivelloIstruzione.LAUREA_MAGISTRALE,
                tipologia=TipologiaDocente.T,
                webinar=False,
                ore_di_incarico=120.0, ore_svolte=0.0,
                unita_formative="Comunicazione efficace,Orientamento al lavoro"
            ),
            Docente(
                nome="Giorgio", cognome="Ferretti",
                codice_fiscale="FRTGRG75C12F205K",
                livello_istruzione=LivelloIstruzione.LAUREA_TRIENNALE,
                tipologia=TipologiaDocente.P,
                webinar=False,
                ore_di_incarico=80.0, ore_svolte=0.0,
                unita_formative="Excel base,Excel avanzato,Power BI"
            ),
            Docente(
                nome="Simona", cognome="Ricci",
                codice_fiscale="RCCSMN82D52G224P",
                livello_istruzione=LivelloIstruzione.DIPLOMA_SUPERIORE,
                tipologia=TipologiaDocente.S,
                webinar=False,
                ore_di_incarico=60.0, ore_svolte=0.0,
                unita_formative="Stage orientamento"
            ),
            Docente(
                nome="Marco", cognome="Testa",
                codice_fiscale="TSTMRC90H10L219Q",
                livello_istruzione=LivelloIstruzione.LAUREA_MAGISTRALE,
                tipologia=TipologiaDocente.T,
                webinar=True,
                ore_di_incarico=40.0, ore_svolte=0.0,
                unita_formative="Python per l'automazione,Introduzione AI"
            ),
        ]
        for d in docenti:
            db.add(d)
        db.flush()
        
        # Assegna docenti a sedi (come nel backup)
        docenti[0].sedi = [s_svizzera, s_cuneo]  # Francesca
        docenti[1].sedi = [s_svizzera]  # Giorgio
        docenti[2].sedi = [s_svizzera, s_asti]  # Simona
        docenti[3].sedi = [s_svizzera]  # Marco
        db.flush()
        print(f"   ✅ {len(docenti)} docenti creati")

        # ══════════════════════════════════════════════════════════════
        # CORSI (3 - come nel backup)
        # ══════════════════════════════════════════════════════════════
        corsi = [
            Corso(
                codice="SSMTO-2026-01",
                titolo="GOL - Segreteria Studio Medico",
                descrizione="Percorso GOL per disoccupati — Segreteria Studio Medico",
                tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                stato_del_corso=StatoCorso.IN_CORSO,
                numero_proposta=1042,
                id_corso_finanziato=1500234,
                responsabile_id=mario.id,
                sede_id=s_svizzera.id,
                num_partecipanti=15,
                ore_totali=144.0, ore_erogate=48.0,
                ore_stage=100.0,
                data_inizio_corso=date(2026, 2, 1),
                data_fine_presunta=date(2026, 5, 7),
                attivo=True
            ),
            Corso(
                codice="CARRTO-2025-10",
                titolo="GOL - Carrellisti",
                descrizione="Percorso GOL per disoccupati — Carrellisti",
                tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                stato_del_corso=StatoCorso.IN_CORSO,
                numero_proposta=2018,
                id_corso_finanziato=1000891,
                responsabile_id=mario.id,
                sede_id=s_svizzera.id,
                num_partecipanti=20,
                ore_totali=12.0, ore_erogate=9.0,
                ore_stage=0.0,
                data_inizio_corso=date(2025, 3, 3),
                data_fine_presunta=date(2025, 9, 30),
                attivo=True
            ),
            Corso(
                codice="VERAT2026-01",
                titolo="FSE - Manutentore del Verde (Asti)",
                descrizione="Corso FSE finanziato - Manutentore del verde",
                tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                stato_del_corso=StatoCorso.IN_CORSO,
                numero_proposta=1058,
                id_corso_finanziato=1500402,
                responsabile_id=elena.id,
                sede_id=s_asti.id,
                num_partecipanti=18,
                ore_totali=172.0, ore_erogate=32.0,
                ore_stage=0.0,
                data_inizio_corso=date(2025, 2, 1),
                data_fine_presunta=date(2025, 7, 31),
                attivo=True
            ),
        ]
        for c in corsi:
            db.add(c)
        db.flush()
        
        # Assegna docenti a corsi (come nel backup)
        corsi[0].docenti = [docenti[0], docenti[2]]  # GOL SSM: Francesca + Simona
        corsi[1].docenti = [docenti[1], docenti[3]]  # GOL Carrellisti: Giorgio + Marco
        corsi[2].docenti = [docenti[0]]  # FSE Verde: Francesca
        db.flush()
        print(f"   ✅ {len(corsi)} corsi creati")

        # ══════════════════════════════════════════════════════════════
        # ALLIEVI (6 - come nel backup)
        # ══════════════════════════════════════════════════════════════
        allievi = [
            Allievo(
                nome="Sara", cognome="Colombo",
                codice_fiscale="CLMSRA95C46L219Z",
                data_nascita=date(1995, 3, 6),
                sesso=Sesso.F,
                cittadinanza=Cittadinanza.COMUNITARIA,
                residente_in=ResidenzaIn.ITALIA,
                provincia_residenza="TO",
                comune_residenza="Torino",
                data_iscrizione=date(2025, 1, 7),
                data_inizio_frequenza=date(2025, 1, 7),
                livello_istruzione=LivelloIstruzione.DIPLOMA_SUPERIORE,
                condizione_occupazionale=CondizioneOccupazionale.DISOCCUPATO,
                disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                ore_erogate=48.0, ore_assenza=4.0,
                posizione_registro_cartaceo=1
            ),
            Allievo(
                nome="Ahmed", cognome="Ben Ali",
                codice_fiscale="BNLHMD88T10Z330K",
                data_nascita=date(1988, 12, 10),
                sesso=Sesso.M,
                cittadinanza=Cittadinanza.EXTRA_COMUNITARIA,
                residente_in=ResidenzaIn.ITALIA,
                provincia_residenza="TO",
                comune_residenza="Torino",
                data_iscrizione=date(2025, 1, 7),
                data_inizio_frequenza=date(2025, 1, 7),
                livello_istruzione=LivelloIstruzione.LICENZA_MEDIA,
                condizione_occupazionale=CondizioneOccupazionale.DISOCCUPATO,
                disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                svantaggio_abitativo=SvantaggioAbitativo.SVANTAGGIO,
                ore_erogate=48.0, ore_assenza=8.0,
                posizione_registro_cartaceo=2
            ),
            Allievo(
                nome="Marta", cognome="Ferrara",
                codice_fiscale="FRRMRT90D50H501P",
                data_nascita=date(1990, 4, 10),
                sesso=Sesso.F,
                cittadinanza=Cittadinanza.COMUNITARIA,
                residente_in=ResidenzaIn.ITALIA,
                provincia_residenza="TO",
                comune_residenza="Moncalieri",
                data_iscrizione=date(2025, 1, 7),
                data_inizio_frequenza=date(2025, 1, 7),
                livello_istruzione=LivelloIstruzione.LAUREA_TRIENNALE,
                condizione_occupazionale=CondizioneOccupazionale.INOCCUPATO,
                disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                ore_erogate=48.0, ore_assenza=0.0,
                posizione_registro_cartaceo=3
            ),
            Allievo(
                nome="Davide", cognome="Greco",
                codice_fiscale="GRCDVD85M20L219R",
                data_nascita=date(1985, 8, 20),
                sesso=Sesso.M,
                cittadinanza=Cittadinanza.COMUNITARIA,
                residente_in=ResidenzaIn.ITALIA,
                provincia_residenza="TO",
                comune_residenza="Torino",
                data_iscrizione=date(2025, 3, 3),
                data_inizio_frequenza=date(2025, 3, 3),
                livello_istruzione=LivelloIstruzione.LAUREA_MAGISTRALE,
                condizione_occupazionale=CondizioneOccupazionale.OCCUPATO_DIPENDENTE,
                disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                ore_erogate=24.0, ore_assenza=0.0,
                posizione_registro_cartaceo=1
            ),
            Allievo(
                nome="Chiara", cognome="Martini",
                codice_fiscale="MRTCHR92P50L219Y",
                data_nascita=date(1992, 9, 10),
                sesso=Sesso.F,
                cittadinanza=Cittadinanza.COMUNITARIA,
                residente_in=ResidenzaIn.ITALIA,
                provincia_residenza="TO",
                comune_residenza="Collegno",
                data_iscrizione=date(2025, 3, 3),
                data_inizio_frequenza=date(2025, 3, 3),
                livello_istruzione=LivelloIstruzione.DIPLOMA_SUPERIORE,
                condizione_occupazionale=CondizioneOccupazionale.OCCUPATO_AUTONOMO,
                disabilita_vulnerabilita=DisabilitaVulnerabilita.DSA,
                svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                ore_erogate=24.0, ore_assenza=2.0,
                posizione_registro_cartaceo=2
            ),
            Allievo(
                nome="Fabio", cognome="Serra",
                codice_fiscale="SRRFBZ79A01H501W",
                data_nascita=date(1979, 1, 1),
                sesso=Sesso.M,
                cittadinanza=Cittadinanza.COMUNITARIA,
                residente_in=ResidenzaIn.ITALIA,
                provincia_residenza="TO",
                comune_residenza="Torino",
                data_iscrizione=date(2025, 1, 7),
                data_inizio_frequenza=date(2025, 1, 7),
                data_ritiro=date(2025, 2, 14),
                motivo_ritiro="Inserimento lavorativo",
                livello_istruzione=LivelloIstruzione.QUALIFICA_PROFESSIONALE,
                condizione_occupazionale=CondizioneOccupazionale.DISOCCUPATO,
                disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                ore_erogate=20.0, ore_assenza=0.0,
                posizione_registro_cartaceo=4
            ),
        ]
        for al in allievi:
            db.add(al)
        db.flush()
        
        # Assegna allievi a corsi (come nel backup)
        corsi[0].allievi = [allievi[0], allievi[1], allievi[2], allievi[5]]  # GOL SSM
        corsi[1].allievi = [allievi[3], allievi[4]]  # GOL Carrellisti
        db.flush()
        print(f"   ✅ {len(allievi)} allievi creati")

        # ══════════════════════════════════════════════════════════════
        # PRENOTAZIONI - Auto-approvate (sistema 2 ruoli)
        # ══════════════════════════════════════════════════════════════
        print("\n   📅 Creazione prenotazioni di esempio...")

        def now_naive():
            return datetime.now(timezone.utc).replace(tzinfo=None)

        oggi = date.today()
        
        # Prenotazioni di esempio
        prenotazioni_data = [
            # Corso Svizzera - GOL SSM
            (aule[2].id, corsi[0].id, mario.id, oggi + timedelta(days=1), time(9, 0), time(12, 0), "Lezione orientamento"),
            (aule[3].id, corsi[0].id, mario.id, oggi + timedelta(days=2), time(14, 0), time(17, 0), "Excel base"),
            (aule[4].id, corsi[0].id, mario.id, oggi + timedelta(days=3), time(9, 0), time(13, 0), "Comunicazione efficace"),
            
            # Corso Svizzera - GOL Carrellisti
            (aule[5].id, corsi[1].id, luca.id, oggi + timedelta(days=1), time(14, 0), time(16, 0), "Teoria sicurezza"),
            (aule[6].id, corsi[1].id, luca.id, oggi + timedelta(days=2), time(9, 0), time(11, 0), "Pratica guida"),
            
            # Asti - FSE Verde
            (aule[8].id, corsi[2].id, elena.id, oggi + timedelta(days=1), time(9, 0), time(12, 0), "Botanica"),
            (aule[9].id, corsi[2].id, elena.id, oggi + timedelta(days=2), time(14, 0), time(18, 0), "Pratica potatura"),
        ]
        
        for aula_id, corso_id, rich_id, data_slot, ora_inizio, ora_fine, note in prenotazioni_data:
            p = Prenotazione(
                aula_id=aula_id,
                corso_id=corso_id,
                richiedente_id=rich_id,
                stato=StatoPrenotazione.CONFERMATA,
                tipo=TipoPrenotazione.SINGOLA,
                note=note
            )
            db.add(p)
            db.flush()
            
            db.add(SlotOrario(
                prenotazione_id=p.id,
                data=data_slot,
                ora_inizio=ora_inizio,
                ora_fine=ora_fine
            ))
            
            db.add(RichiestaPrenotazione(
                prenotazione_id=p.id,
                stato=StatoRichiesta.APPROVATA,
                ha_conflitti=False,
                data_gestione=now_naive()
            ))
        
        # Crea 2 prenotazioni in conflitto per test
        p1 = Prenotazione(
            aula_id=aule[2].id,  # Aula Gialla Corso Svizzera
            corso_id=corsi[0].id,
            richiedente_id=mario.id,
            stato=StatoPrenotazione.CONFERMATA,
            tipo=TipoPrenotazione.SINGOLA,
            note="TEST CONFLITTO 1"
        )
        db.add(p1)
        db.flush()
        db.add(SlotOrario(
            prenotazione_id=p1.id,
            data=oggi + timedelta(days=5),
            ora_inizio=time(10, 0),
            ora_fine=time(13, 0)
        ))
        db.add(RichiestaPrenotazione(
            prenotazione_id=p1.id,
            stato=StatoRichiesta.APPROVATA,
            ha_conflitti=False,
            data_gestione=now_naive()
        ))
        
        p2 = Prenotazione(
            aula_id=aule[2].id,  # STESSA AULA!
            corso_id=corsi[1].id,
            richiedente_id=luca.id,
            stato=StatoPrenotazione.CONFERMATA,
            tipo=TipoPrenotazione.SINGOLA,
            note="TEST CONFLITTO 2"
        )
        db.add(p2)
        db.flush()
        db.add(SlotOrario(
            prenotazione_id=p2.id,
            data=oggi + timedelta(days=5),  # STESSO GIORNO!
            ora_inizio=time(11, 0),  # SOVRAPPOSTO
            ora_fine=time(14, 0)
        ))
        db.add(RichiestaPrenotazione(
            prenotazione_id=p2.id,
            stato=StatoRichiesta.APPROVATA,
            ha_conflitti=True,
            data_gestione=now_naive()
        ))
        
        db.commit()

        # ══════════════════════════════════════════════════════════════
        # RIEPILOGO
        # ══════════════════════════════════════════════════════════════
        n_pren = db.query(Prenotazione).count()
        n_slot = db.query(SlotOrario).count()

        print(f"\n✅ Seeding completato!")
        print(f"   • {len(sedi)} sedi")
        print(f"   • {len(aule)} aule")
        print(f"   • {len(utenti)} utenti (8 OPERATIVI + 1 COORDINAMENTO)")
        print(f"   • {len(docenti)} docenti")
        print(f"   • {len(corsi)} corsi")
        print(f"   • {len(allievi)} allievi")
        print(f"   • {n_pren} prenotazioni")
        print(f"   • {n_slot} slot orari")

        print("\n📋 CREDENZIALI TEST (password originali dal backup):")
        print("\n   OPERATIVI (ex vari ruoli):")
        print(f"   responsabile@test.it       / test  →  Mario Rossi (ex RESPONSABILE_CORSO)")
        print(f"   responsabile2@test.it      / test  →  Luca Ferrari (ex RESPONSABILE_CORSO)")
        print(f"   resp.asti@test.it          / test  →  Elena Conti (ex RESPONSABILE_CORSO)")
        print(f"   resp.sede@test.it          / test  →  Lucia Bianchi (ex RESPONSABILE_SEDE)")
        print(f"   resp.cuneo@test.it         / test  →  Carla Esposito (ex RESPONSABILE_SEDE)")
        print(f"   segr.sede@test.it          / test  →  Giulia Verdi (ex SEGRETERIA_SEDE)")
        print(f"   segr.cuneo@test.it         / test  →  Roberto Marino (ex SEGRETERIA_SEDE)")
        print(f"   segr.did@test.it           / test  →  Paolo Neri (ex SEGRETERIA_DIDATTICA)")
        
        print("\n   COORDINAMENTO:")
        print(f"   coord@test.it              / test  →  Anna Blu")

        print(f"\n⚠️  CONFLITTO CREATO PER TEST:")
        print(f"   Prenotazione #{p1.id} vs #{p2.id}")
        print(f"   Aula Gialla Corso Svizzera - {oggi + timedelta(days=5)}")
        print(f"   10:00-13:00 vs 11:00-14:00")
        print(f"\n   → Login come COORDINAMENTO per risolverlo!\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()