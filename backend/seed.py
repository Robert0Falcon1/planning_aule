"""
Script di seeding per sistema 2 RUOLI (OPERATIVO + COORDINAMENTO)
Eseguire con: python -m backend.seed_2_ruoli
"""

from backend.database import SessionLocal, crea_tabelle
from backend.core.security import hash_password
from backend.models import *
from backend.models.enums import (
    RuoloUtente, TipoFinanziamento, StatoCorso, StatoPrenotazione, 
    StatoRichiesta, TipoRicorrenza, TipoLezione, TipologiaDocente, 
    Sesso, Cittadinanza, ResidenzaIn, LivelloIstruzione, 
    CondizioneOccupazionale, DisabilitaVulnerabilita, SvantaggioAbitativo
)
from backend.models.prenotazione import (PrenotazioneSingola, PrenotazioneMassiva,
                                          RichiestaPrenotazione)
from backend.models.slot_orario import SlotOrario
from datetime import date, time, datetime, timedelta, timezone


def seed():
    """Popola database con 2 ruoli + test conflitti"""
    crea_tabelle()
    db = SessionLocal()

    try:
        if db.query(Sede).count() > 0:
            print("⚠️  Database già inizializzato. Seed saltato.")
            return

        print("🌱 Seeding database ICE 1.0 - Sistema 2 RUOLI\n")

        # ══════════════════════════════════════════════════════════════
        # SEDI
        # ══════════════════════════════════════════════════════════════
        sedi = [
            Sede(nome="Corso Svizzera", indirizzo="C.so Svizzera 161", citta="Torino", capienza_massima=99),
            Sede(nome="Cuneo", indirizzo="Via Cascina Colombaro 26/D", citta="Cuneo", capienza_massima=41),
            Sede(nome="Asti", indirizzo="Piazza Roma 13", citta="Asti", capienza_massima=56),
        ]
        for s in sedi:
            db.add(s)
        db.flush()
        print(f"   ✅ {len(sedi)} sedi create")

        s_svizzera, s_cuneo, s_asti = sedi

        # ══════════════════════════════════════════════════════════════
        # AULE
        # ══════════════════════════════════════════════════════════════
        aule = [
            Aula(nome="Aula Gialla", capienza=18, sede_id=s_svizzera.id),
            Aula(nome="Aula Arancio", capienza=21, sede_id=s_svizzera.id),
            Aula(nome="Aula Verde", capienza=25, sede_id=s_svizzera.id),
            Aula(nome="Aula 1", capienza=15, sede_id=s_cuneo.id),
            Aula(nome="Aula 1", capienza=21, sede_id=s_asti.id),
        ]
        for a in aule:
            db.add(a)
        db.flush()
        print(f"   ✅ {len(aule)} aule create")

        a_gialla, a_arancio, a_verde, a_cuneo, a_asti = aule

        # ══════════════════════════════════════════════════════════════
        # UTENTI (2 RUOLI)
        # ══════════════════════════════════════════════════════════════
        utenti = [
            # OPERATIVI
            Utente(
                nome="Mario", cognome="Rossi", 
                email="operativo.torino@test.it",
                password_hash=hash_password("test"),
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_svizzera.id
            ),
            Utente(
                nome="Luca", cognome="Ferrari", 
                email="operativo.cuneo@test.it",
                password_hash=hash_password("test"),
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_cuneo.id
            ),
            Utente(
                nome="Elena", cognome="Conti", 
                email="operativo.asti@test.it",
                password_hash=hash_password("test"),
                ruolo=RuoloUtente.OPERATIVO,
                sede_id=s_asti.id
            ),
            # COORDINAMENTO
            Utente(
                nome="Anna", cognome="Blu", 
                email="coordinamento@test.it",
                password_hash=hash_password("test"),
                ruolo=RuoloUtente.COORDINAMENTO,
                sede_id=None  # Vede tutte le sedi
            ),
        ]
        for u in utenti:
            db.add(u)
        db.flush()
        print(f"   ✅ {len(utenti)} utenti creati")

        mario = utenti[0]   # OPERATIVO Torino
        luca = utenti[1]    # OPERATIVO Cuneo
        elena = utenti[2]   # OPERATIVO Asti
        anna = utenti[3]    # COORDINAMENTO

        # ══════════════════════════════════════════════════════════════
        # DOCENTI
        # ══════════════════════════════════════════════════════════════
        docenti = [
            Docente(
                nome="Francesca", cognome="Amato",
                codice_fiscale="AMTFNC80A41L219X",
                livello_istruzione=LivelloIstruzione.LAUREA_MAGISTRALE,
                tipologia=TipologiaDocente.T,
                webinar=False,
                ore_di_incarico=120.0, ore_svolte=48.0,
                unita_formative="Comunicazione,Orientamento"
            ),
            Docente(
                nome="Giorgio", cognome="Ferretti",
                codice_fiscale="FRTGRG75C12F205K",
                livello_istruzione=LivelloIstruzione.LAUREA_TRIENNALE,
                tipologia=TipologiaDocente.P,
                webinar=False,
                ore_di_incarico=80.0, ore_svolte=24.0,
                unita_formative="Excel,Power BI"
            ),
        ]
        for d in docenti:
            db.add(d)
        db.flush()
        docenti[0].sedi = [s_svizzera, s_cuneo]
        docenti[1].sedi = [s_svizzera]
        db.flush()
        print(f"   ✅ {len(docenti)} docenti creati")

        # ══════════════════════════════════════════════════════════════
        # CORSI
        # ══════════════════════════════════════════════════════════════
        corsi = [
            Corso(
                codice="GOL-TO-2026-01",
                titolo="GOL - Segreteria Studio Medico",
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
                descrizione="Percorso GOL Torino"
            ),
            Corso(
                codice="FSE-CU-2026-01",
                titolo="FSE - Manutentore del Verde",
                tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                stato_del_corso=StatoCorso.IN_CORSO,
                numero_proposta=1058,
                id_corso_finanziato=1500402,
                responsabile_id=luca.id,
                sede_id=s_cuneo.id,
                num_partecipanti=12,
                ore_totali=120.0, ore_erogate=24.0,
                data_inizio_corso=date(2026, 2, 15),
                data_fine_presunta=date(2026, 6, 30),
                descrizione="Corso FSE Cuneo"
            ),
        ]
        for c in corsi:
            db.add(c)
        db.flush()

        c_gol = corsi[0]
        c_fse = corsi[1]

        c_gol.docenti = [docenti[0]]
        c_fse.docenti = [docenti[1]]
        db.flush()
        print(f"   ✅ {len(corsi)} corsi creati")

        # ══════════════════════════════════════════════════════════════
        # ALLIEVI
        # ══════════════════════════════════════════════════════════════
        allievi = [
            Allievo(
                nome="Sara", cognome="Colombo",
                codice_fiscale="CLMSRA95C46L219Z",
                data_nascita=date(1995, 3, 6),
                sesso=Sesso.F,
                cittadinanza=Cittadinanza.COMUNITARIA,
                residente_in=ResidenzaIn.ITALIA,
                comune_residenza="Torino", provincia_residenza="TO",
                data_iscrizione=date(2026, 1, 7),
                data_inizio_frequenza=date(2026, 1, 7),
                livello_istruzione=LivelloIstruzione.DIPLOMA_SUPERIORE,
                condizione_occupazionale=CondizioneOccupazionale.DISOCCUPATO,
                disabilita_vulnerabilita=DisabilitaVulnerabilita.NESSUNA,
                svantaggio_abitativo=SvantaggioAbitativo.NESSUNA,
                ore_erogate=48.0, ore_assenza=4.0,
                posizione_registro_cartaceo=1
            ),
        ]
        for al in allievi:
            db.add(al)
        db.flush()

        c_gol.allievi = allievi
        db.flush()
        print(f"   ✅ {len(allievi)} allievi creati")

        # ══════════════════════════════════════════════════════════════
        # PRENOTAZIONI CON AUTO-APPROVAZIONE
        # ══════════════════════════════════════════════════════════════
        print("\n   📅 Creazione prenotazioni...")

        def now_naive():
            return datetime.now(timezone.utc).replace(tzinfo=None)

        oggi = date.today()
        domani = oggi + timedelta(days=1)
        dopodomani = oggi + timedelta(days=2)

        # ──────── Prenotazione 1: CONFERMATA (no conflitto) ────────
        p1 = PrenotazioneSingola(
            aula_id=a_gialla.id,
            corso_id=c_gol.id,
            richiedente_id=mario.id,
            stato=StatoPrenotazione.CONFERMATA,
            note="Prima prenotazione OK"
        )
        db.add(p1)
        db.flush()
        db.add(SlotOrario(
            prenotazione_id=p1.id,
            data=domani,
            ora_inizio=time(9, 0),
            ora_fine=time(12, 0)
        ))
        db.add(RichiestaPrenotazione(
            prenotazione_id=p1.id,
            stato=StatoRichiesta.APPROVATA,  # AUTO-APPROVATA
            ha_conflitti=False,
            data_gestione=now_naive()
        ))

        # ──────── Prenotazione 2: CONFERMATA che crea CONFLITTO ────────
        p2 = PrenotazioneSingola(
            aula_id=a_gialla.id,  # STESSA AULA!
            corso_id=c_fse.id,
            richiedente_id=luca.id,
            stato=StatoPrenotazione.CONFERMATA,
            note="Prenotazione che si sovrappone"
        )
        db.add(p2)
        db.flush()
        db.add(SlotOrario(
            prenotazione_id=p2.id,
            data=domani,  # STESSO GIORNO!
            ora_inizio=time(10, 0),  # SOVRAPPOSTO: 10:00-13:00 vs 9:00-12:00
            ora_fine=time(13, 0)
        ))
        db.add(RichiestaPrenotazione(
            prenotazione_id=p2.id,
            stato=StatoRichiesta.APPROVATA,
            ha_conflitti=True,  # CONFLITTO!
            data_gestione=now_naive()
        ))

        # ──────── Prenotazione 3: OK diversa aula ────────
        p3 = PrenotazioneSingola(
            aula_id=a_arancio.id,  # Aula diversa, nessun conflitto
            corso_id=c_gol.id,
            richiedente_id=mario.id,
            stato=StatoPrenotazione.CONFERMATA,
            note="Seconda sessione"
        )
        db.add(p3)
        db.flush()
        db.add(SlotOrario(
            prenotazione_id=p3.id,
            data=dopodomani,
            ora_inizio=time(14, 0),
            ora_fine=time(18, 0)
        ))
        db.add(RichiestaPrenotazione(
            prenotazione_id=p3.id,
            stato=StatoRichiesta.APPROVATA,
            ha_conflitti=False,
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
        print(f"   • {len(utenti)} utenti (2 ruoli)")
        print(f"   • {len(corsi)} corsi")
        print(f"   • {n_pren} prenotazioni")
        print(f"   • {n_slot} slot orari")

        print("\n📋 CREDENZIALI TEST:")
        for u in utenti:
            label = f"{u.ruolo.value:<15}"
            if u.sede_id:
                sede_nome = db.query(Sede).get(u.sede_id).nome
                label += f" - {sede_nome}"
            else:
                label += " - Tutte le sedi"
            print(f"   {u.email:<30} / test  →  {u.nome} {u.cognome} ({label})")

        print("\n⚠️  CONFLITTO CREATO PER TEST:")
        print(f"   Prenotazione #{p1.id} (Aula Gialla, {domani}, 9:00-12:00)")
        print(f"   vs")
        print(f"   Prenotazione #{p2.id} (Aula Gialla, {domani}, 10:00-13:00)")
        print(f"\n   → Login come COORDINAMENTO per risolverlo!\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Errore: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()