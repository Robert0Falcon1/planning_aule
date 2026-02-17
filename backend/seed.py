"""
Script di seeding del database con dati iniziali.
Crea le sedi, le aule e un utente per ogni ruolo per i test.
Eseguire con: python -m backend.seed
"""

from backend.database import SessionLocal, crea_tabelle
from backend.core.security import hash_password
from backend.models import *
from backend.models.enums import TipoFinanziamento
from datetime import date


def seed():
    """Popola il database con i dati iniziali."""
    crea_tabelle()
    db = SessionLocal()

    try:
        # ── Verifica se il DB è già stato inizializzato ───────────────────────
        if db.query(Sede).count() > 0:
            print("⚠️  Database già inizializzato. Seed saltato.")
            return

        print("🌱 Avvio seeding database...")

        # ── SEDI ─────────────────────────────────────────────────────────────
        sedi_dati = [
            Sede(nome="Via Livorno 49",   indirizzo="Via Livorno 49",   citta="Torino", capienza_massima=30),
            Sede(nome="Via Livorno 53 A", indirizzo="Via Livorno 53 A", citta="Torino", capienza_massima=50),
            Sede(nome="Via Livorno 53 B", indirizzo="Via Livorno 53 B", citta="Torino", capienza_massima=50),
            Sede(nome="Corso Svizzera",   indirizzo="C.so Svizzera 161",citta="Torino", capienza_massima=150),
            Sede(nome="Cuneo",            indirizzo="Via Roma 1",       citta="Cuneo",  capienza_massima=60),
            Sede(nome="Asti",             indirizzo="Corso Alba 10",    citta="Asti",   capienza_massima=80),
            Sede(nome="Novara",           indirizzo="Via Biglieri 5",   citta="Novara", capienza_massima=100),
            Sede(nome="Biella",           indirizzo="Via Galileo 3",    citta="Biella", capienza_massima=100),
        ]
        for s in sedi_dati:
            db.add(s)
        db.flush()
        print(f"   ✅ {len(sedi_dati)} sedi create")




        # ── AULE ─────────────────────────────────────────────────────────────
        aule_dati = [
            # Via Livorno 49: 1 aula
            Aula(nome="Aula 1",  capienza=20, sede_id=sedi_dati[0].id),
            # Via Livorno 53 A: 1 aula
            Aula(nome="Aula 1",  capienza=25, sede_id=sedi_dati[1].id),
            # Via Livorno 53 B: 1 aula
            Aula(nome="Aula 2",  capienza=25, sede_id=sedi_dati[2].id),
            # Corso Svizzera 161: 5 aule
            Aula(nome="Aula 1",  capienza=30, sede_id=sedi_dati[3].id),
            Aula(nome="Aula 2",  capienza=30, sede_id=sedi_dati[3].id),
            Aula(nome="Aula 3",  capienza=25, sede_id=sedi_dati[3].id),
            Aula(nome="Aula 4",  capienza=25, sede_id=sedi_dati[3].id),
            Aula(nome="Aula 5",  capienza=20, sede_id=sedi_dati[3].id),
            # Cuneo: 2 aule
            Aula(nome="Aula 1",  capienza=30, sede_id=sedi_dati[4].id),
            Aula(nome="Aula 2",  capienza=30, sede_id=sedi_dati[4].id),
            # Asti: 3 aule
            Aula(nome="Aula 1",  capienza=25, sede_id=sedi_dati[5].id),
            Aula(nome="Aula 2",  capienza=25, sede_id=sedi_dati[5].id),
            Aula(nome="Aula 3",  capienza=25, sede_id=sedi_dati[5].id),
            # Novara: 4 aule
            Aula(nome="Aula 1",  capienza=25, sede_id=sedi_dati[6].id),
            Aula(nome="Aula 2",  capienza=25, sede_id=sedi_dati[6].id),
            Aula(nome="Aula 3",  capienza=25, sede_id=sedi_dati[6].id),
            Aula(nome="Aula 4",  capienza=25, sede_id=sedi_dati[6].id),
            # Biella: 4 aule
            Aula(nome="Aula 1",  capienza=25, sede_id=sedi_dati[7].id),
            Aula(nome="Aula 2",  capienza=25, sede_id=sedi_dati[7].id),
            Aula(nome="Aula 3",  capienza=25, sede_id=sedi_dati[7].id),
            Aula(nome="Aula 4",  capienza=25, sede_id=sedi_dati[7].id),
        ]
        for a in aule_dati:
            db.add(a)
        db.flush()
        print(f"   ✅ {len(aule_dati)} aule create")

        # ── UTENTI DI TEST (uno per ruolo) ────────────────────────────────────
        utenti_dati = [
            Utente(nome="Mario",    cognome="Rossi",     email="responsabile@test.it",
                   password_hash=hash_password("Test1234!"),
                   ruolo=RuoloUtente.RESPONSABILE_CORSO,   sede_id=sedi_dati[3].id),
            Utente(nome="Lucia",    cognome="Bianchi",   email="resp.sede@test.it",
                   password_hash=hash_password("Test1234!"),
                   ruolo=RuoloUtente.RESPONSABILE_SEDE,    sede_id=sedi_dati[3].id),
            Utente(nome="Giulia",   cognome="Verdi",     email="segr.sede@test.it",
                   password_hash=hash_password("Test1234!"),
                   ruolo=RuoloUtente.SEGRETERIA_SEDE,      sede_id=sedi_dati[3].id),
            Utente(nome="Paolo",    cognome="Neri",      email="segr.did@test.it",
                   password_hash=hash_password("Test1234!"),
                   ruolo=RuoloUtente.SEGRETERIA_DIDATTICA, sede_id=sedi_dati[3].id),
            Utente(nome="Anna",     cognome="Blu",       email="coord@test.it",
                   password_hash=hash_password("Test1234!"),
                   ruolo=RuoloUtente.COORDINAMENTO,        sede_id=None),
        ]
        for u in utenti_dati:
            db.add(u)
        db.flush()
        print(f"   ✅ {len(utenti_dati)} utenti di test creati")

        corsi_dati = [
            Corso(
                codice='GOL-2024-001',
                titolo='Corso GOL - Orientamento al Lavoro',
                tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                responsabile_id=utenti_dati[0].id,   # Mario Rossi (responsabile@test.it)
                num_partecipanti=15,
                data_inizio=date(2024, 1, 1),
                data_fine=date(2024, 12, 31),
                descrizione='Corso GOL di test',
            ),
            Corso(
                codice='FSE-2024-001',
                titolo='Corso FSE - Formazione Professionale',
                tipo_finanziamento=TipoFinanziamento.FINANZIATO_PUBBLICO,
                responsabile_id=utenti_dati[0].id,
                num_partecipanti=20,
                data_inizio=date(2024, 1, 1),
                data_fine=date(2024, 12, 31),
                descrizione='Corso FSE di test',
            ),
        ]
        for c in corsi_dati:
            db.add(c)
        db.flush()
        print(f"   ✅ {len(corsi_dati)} corsi di test creati (ID: {corsi_dati[0].id}, {corsi_dati[1].id})")


        db.commit()
        print("\n✅ Seeding completato!")
        print("\n📋 Credenziali di test:")
        print("   responsabile@test.it  / Test1234!  → Responsabile Corso")
        print("   resp.sede@test.it     / Test1234!  → Responsabile Sede")
        print("   segr.sede@test.it     / Test1234!  → Segreteria Sede")
        print("   segr.did@test.it      / Test1234!  → Segreteria Didattica")
        print("   coord@test.it         / Test1234!  → Coordinamento")

    except Exception as e:
        db.rollback()
        print(f"❌ Errore durante il seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()