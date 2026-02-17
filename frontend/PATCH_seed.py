# ─────────────────────────────────────────────────────────────────────────────
# PATCH per backend/seed.py
# Aggiunge un corso di test affinché le prenotazioni possano essere create.
# 
# ISTRUZIONI: nel tuo backend/seed.py, dopo la creazione degli utenti
# (dopo il db.flush() degli utenti) e prima del db.commit() finale,
# aggiungi questo blocco:
# ─────────────────────────────────────────────────────────────────────────────

from backend.models.corso import Corso
from backend.models.enums import TipoFinanziamento
from datetime import date

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
