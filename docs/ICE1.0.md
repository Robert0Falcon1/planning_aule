PLANNING PRENOTAZIONE AULE per lo svolgimento dei corsi
Sistema ad uso interno che consenta utilizzi diversificati di prenotazione spazi

LE AULE
    Torino:
        1 aula in Via Livorno 49
        2 aule in Via Livorno 53/B
        5 aule in C.so Svizzera 161
    Cuneo:
        2 aule
    Asti:ule
    Novara:
        4 aule
    Biella:
        4 aule

GLI OBIETTIVI
    -RENDERE PIU’ AGILE IL SISTEMA DI PRENOTAZIONE AULE
    -UNIFORMARE GLI STRUMENTI IN USO ALLE SEDI
    -RIDURRE L’ERRORE UMANO NEL PROCESSO DI PRENOTAZIONE
    -RACCOGLIERE DATI CIRCA LA SATURAZIONE DEGLI SPAZI
    -FORNIRE FOTOGRAFIE PRECISE DI CIO’ CHE ACCADE IN OGNI SEDE

I RUOLI
    -RESPONSABILE_CORSO: Richiede la prenotazione dell’aula per il suo corso
    -RESPONSABILE DI SEDE: Verifica la situazione delle prenotazioni per la sua sede
    -SEGRETERIA DI SEDE: Valida e inserisce le prenotazioni (volendo le rifiuta?)
    -SEGRETERIA DIDATTICA: Verifica la situazione delle prenotazioni per i suoi corsi
    -COORDINAMENTO: Verifica la situazione complessiva delle prenotazioni

COSA DOVRA’ CONSENTIRE IL SISTEMA
    -PRENOTAZIONI MASSIVE (es: tutti i lunedì da una certa data ad un’altra)
    -VERIFICA DELLE CAPIENZE (limite di persone presenti per sede complessivamente)
    -RICHIESTE DI ATTREZZATURE (es: pc)
    -VISUALIZZARE SLOT LIBERI PER AULA
    -SEGNALARE COME PROBLEMA, MA CONSENTIRE RICHIESTA PRENOTAZIONE PER SLOT GIA’ BLOCCATI
    -LAVORARE ON CLOUD
    -CONSENTIRE PERMESSI E AZIONI DIVERSIFICATE A SECONDA DEI RUOLI

------ versione corretta ------

SENSO
    - Saturare gli spazi
    - Raccogliere dati per valutare l'uso degli spazi
    - Chiarire modalità di prenotazione

OBIETTIVO
    - Rendere agile il processo di prenotazione
    - Ridurre il margine di errore umano
    - Ottimizzare gli spazi
    - Omogenizzare lo strumento di lavoro tra le sedi
    - Dare uno strumento di supervisione

RUOLI
    OPERATIVO
    COORDINAMENTO

    - RESPONSABILE_CORSO / SEGRETERIA_DIDATTICA / SEGRETERIA_DI_SEDE (SUPERVISIONE + OPERATIVO)

    Permessi OPERATIVI
        Prenotare le aule > Confermare / Modificare / Disdire SOLO le proprie prenotazioni
        (Campo Note da scrivere a mano per indicare eventuali DOCENTI e ATTREZZATURE)

    Permessi SUPERVISIONE (limitati)
        Visualizza le prenotazioni della sede
        Riceve la situazione complessiva del libero e del prenotato

    - RESPONSABILE_SEDE / COORDINAMENTO (SUPERVISIONE + SUPERADMIN)

    Permessi SUPERVISIONE
        Visualizza le prenotazioni della sede
        Riceve la situazione complessiva del libero e del prenotato
        Dati sulla saturazione di sedi e aule giorno per giorno
        Esporta i dati in formato CSV

    Permessi SUPERADMIN (limitati)
        Risolve eventuali conflitti generati dagli OPERATIVI
        Aggiunge / Elimina / Modifica gli account di tipo OPERATIVO

# Sistema Prenotazione Aule - Modifiche Backend v2.0

## 📋 Riepilogo Modifiche

### ✅ Cosa è Cambiato

#### 1. **Prenotazione Diretta (NO Workflow Approvazione)**

- ❌ **RIMOSSO**: Workflow approvazione (tabella `richieste_prenotazione`)
- ✅ **NUOVO**: Conferma immediata - stato default `CONFERMATA`
- Stati disponibili: `CONFERMATA`, `ANNULLATA`, `CONFLITTO`

#### 2. **Conflitti come WARNING (Non Bloccanti)**

- Conflitti rilevati automaticamente ma NON impediscono la creazione
- Stato `CONFLITTO` indica sovrapposizioni (solo WARNING)
- Solo COORDINAMENTO può risolvere conflitti

#### 3. **Attrezzature nelle Note**

- ❌ **RIMOSSE**: Tabelle `attrezzature`, `richieste_attrezzatura`
- ✅ **NUOVO**: Campo `note` include: docenti, attrezzature, indicazioni varie

#### 4. **RBAC Semplificato (2 Gruppi)**

**GRUPPO OPERATIVO**(Responsabile Corso, Segreteria Didattica, Segreteria Sede)

- ✅ Prenotano direttamente (conferma immediata)
- ✅ Vedono tutte le prenotazioni della SEDE
- ✅ Modificano/Eliminano SOLO le proprie prenotazioni
- ✅ Vedono saturazione della sede

**GRUPPO COORDINAMENTO**(Responsabile Sede, Coordinamento)

- ✅ Tutti i permessi di OPERATIVO
- ✅ Risolve conflitti
- ✅ Modifica/Elimina prenotazioni di chiunque
- ✅ Gestisce utenti (crea/modifica/elimina OPERATIVI)
- ✅ Export CSV, saturazione globale

---

## 🗂️ File Modificati

### Modelli ORM

- ✏️ `backend/models/enums.py` - Rimossi stati `IN_ATTESA`, `RIFIUTATA`, enum `StatoRichiesta`
- ✏️ `backend/models/prenotazione.py` - Rimossa `RichiestaPrenotazione`, modificato `Conflitto`
- ✏️ `backend/models/__init__.py` - Aggiornati import

### Core Business Logic

- ✏️ `backend/core/permissions.py` - Nuovo RBAC secondo 2 gruppi
- ✏️ `backend/services/booking_service.py` - Conferma immediata, conflitti non bloccanti
- ✏️ `backend/services/conflict_service.py` - INVARIATO (riutilizzato)

### API Endpoints

- ✏️ `backend/routers/prenotazioni.py` - Rimossi endpoint approva/rifiuta, aggiunti conflitti
- ✏️ `backend/schemas/prenotazione.py` - Nuovi schemi (rimosso `RichiestaEmbedded`)

### Database

- 📄 `backend_modified/migration.sql` - Script migrazione database

---

## 🚀 Istruzioni Aggiornamento

### 1. Backup Database

```bash
# MySQL/MariaDB
mysqldump -u root -p prenotazione_aule > backup_prenotazione_aule_$(date +%Y%m%d).sql

# Oppure copia directory dati (se sviluppo locale)
cp -r /var/lib/mysql/prenotazione_aule /path/to/backup/
```

### 2. Applica Migrazione Database

```bash
mysql -u root -p prenotazione_aule < backend_modified/migration.sql
```

### 3. Sostituisci File Backend

```bash
# Backup vecchi file
cp -r backend backend_backup_$(date +%Y%m%d)

# Copia nuovi file
cp backend_modified/models/enums.py backend/models/
cp backend_modified/models/prenotazione.py backend/models/
cp backend_modified/models/__init__.py backend/models/
cp backend_modified/core/permissions.py backend/core/
cp backend_modified/services/booking_service.py backend/services/
cp backend_modified/routers/prenotazioni.py backend/routers/
cp backend_modified/schemas/prenotazione.py backend/schemas/
```

### 4. Reinstalla Dipendenze (se necessario)

```bash
pip install -r requirements.txt
```

### 5. Testa Applicazione

```bash
# Avvia server sviluppo
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Verifica documentazione API
# Apri browser: http://localhost:8000/api/docs
```

### 6. Verifica Funzionalità

**Test RBAC:**

```bash
# Login come RC (Responsabile Corso)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=responsabile@test.it&password=test"

# Crea prenotazione (deve confermare immediatamente)
# Prova a modificare prenotazione altrui (deve essere negato)
```

**Test Conflitti:**

```bash
# Crea 2 prenotazioni sovrapposte
# Verifica che entrambe vengano create (stato CONFLITTO)
# Lista conflitti: GET /api/v1/prenotazioni/conflitti/lista
```

---

## 📊 Cosa NON è Cambiato

### ✅ Mantenuto Invariato

1. **Prenotazioni Singole e Massive**

   - Logica generazione slot ricorrenti (settimanale, bisettimanale, mensile)
   - Tutte le funzioni `genera_date_ricorrenza()` invariate
2. **Gestione Slot Orari**

   - Tabella `slot_orari` invariata
   - Annullamento singoli slot per massive
3. **Conflict Detection**

   - Algoritmo rilevamento sovrapposizioni invariato
   - `rileva_conflitti_slot()` riutilizzato identico
4. **Modelli Corsi/Docenti/Allievi**

   - Nessuna modifica a: `corso.py`, `docente.py`, `allievo.py`, `lezione.py`
   - Catalogo regionale invariato
5. **Autenticazione e Utenti**

   - JWT e security invariati
   - Gestione utenti identica

---

## 🔄 Endpoints API Modificati

### ❌ Rimossi

```
POST   /api/v1/prenotazioni/richieste/{id}/approva
POST   /api/v1/prenotazioni/richieste/{id}/rifiuta
```

### ✏️ Modificati

```
POST   /api/v1/prenotazioni/singola
       → Ora conferma immediata (stato: CONFERMATA)
     
POST   /api/v1/prenotazioni/massiva
       → Ora conferma immediata (stato: CONFERMATA)

PATCH  /api/v1/prenotazioni/{id}
       → RBAC: operativi solo proprie, coordinamento tutte

DELETE /api/v1/prenotazioni/{id}
       → RBAC: operativi solo proprie, coordinamento tutte

GET    /api/v1/prenotazioni/
       → RBAC: operativi vedono sede, coordinamento tutto
```

### ✅ Aggiunti

```
GET    /api/v1/prenotazioni/conflitti/lista
       → Lista conflitti (RBAC applicato)

POST   /api/v1/prenotazioni/conflitti/{id}/risolvi
       → Risolvi conflitto (solo COORDINAMENTO)
```

---

## 🔒 Matrice Permessi RBAC

| Azione                 | RC | SD | SS | RS | CO |
| ---------------------- | -- | -- | -- | -- | -- |
| **Prenotazioni** |    |    |    |    |    |
| Creare                 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Modificare proprie     | ✅ | ✅ | ✅ | ✅ | ✅ |
| Eliminare proprie      | ✅ | ✅ | ✅ | ✅ | ✅ |
| Modificare qualsiasi   | ❌ | ❌ | ❌ | ✅ | ✅ |
| Eliminare qualsiasi    | ❌ | ❌ | ❌ | ✅ | ✅ |
| Vedere proprie         | ✅ | ✅ | ✅ | ✅ | ✅ |
| Vedere sede            | ✅ | ✅ | ✅ | ✅ | ✅ |
| Vedere tutte           | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Conflitti**    |    |    |    |    |    |
| Vedere                 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Risolvere              | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Report**       |    |    |    |    |    |
| Saturazione sede       | ✅ | ✅ | ✅ | ✅ | ✅ |
| Saturazione globale    | ❌ | ❌ | ❌ | ✅ | ✅ |
| Export CSV             | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Utenti**       |    |    |    |    |    |
| Creare/Modificare      | ❌ | ❌ | ❌ | ✅ | ✅ |

**Legenda:**
RC=Responsabile Corso | SD=Segreteria Didattica | SS=Segreteria Sede
RS=Responsabile Sede | CO=Coordinamento

---

## 🐛 Troubleshooting

### Errore: "Column 'stato' cannot be null"

```sql
-- Verifica stati prenotazioni
SELECT stato, COUNT(*) FROM prenotazioni GROUP BY stato;

-- Se ci sono valori NULL
UPDATE prenotazioni SET stato = 'confermata' WHERE stato IS NULL;
```

### Errore: "Table 'richieste_prenotazione' doesn't exist"

```bash
# Verifica che il vecchio codice non importi più quella tabella
grep -r "RichiestaPrenotazione" backend/

# Se trova riferimenti, rimuovili manualmente
```

### Conflitti Non Rilevati

```python
# Verifica che conflict_service.py sia aggiornato
# Parametro escludi_prenotazione_id deve essere passato
```

---

## 📞 Supporto

Per problemi o domande:

1. Controlla i log: `tail -f logs/backend.log`
2. Verifica documentazione API: `http://localhost:8000/api/docs`
3. Consulta questo README

---

## 📝 Note Finali

- ✅ Database migrato conserva TUTTI i dati storici
- ✅ Prenotazioni "in_attesa" convertite in "confermata"
- ✅ Prenotazioni "rifiutate" convertite in "annullata"
- ✅ Backup automatico prima della migrazione
- ✅ Rollback possibile tramite backup SQL

**IMPORTANTE**: Dopo aver verificato che tutto funzioni correttamente, rimuovi le tabelle di backup:

```sql
DROP TABLE _backup_prenotazioni;
DROP TABLE _backup_richieste_prenotazione;
DROP TABLE _backup_conflitti;
```
