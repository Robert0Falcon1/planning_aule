# 🏫 Sistema Prenotazione Aule
### Agenzia Formativa — Manuale Utente e Documentazione Tecnica

> Versione 1.0 | Python + FastAPI + Streamlit + SQLite

---

## 📋 Indice

1. [Panoramica del sistema](#1-panoramica-del-sistema)
2. [Requisiti di sistema](#2-requisiti-di-sistema)
3. [Installazione e avvio](#3-installazione-e-avvio)
4. [Struttura del progetto](#4-struttura-del-progetto)
5. [Accesso al sistema](#5-accesso-al-sistema)
6. [Guida per Responsabile Corso](#6-guida-per-responsabile-corso)
7. [Guida per Segreteria di Sede](#7-guida-per-segreteria-di-sede)
8. [Guida per Responsabile di Sede](#8-guida-per-responsabile-di-sede)
9. [Guida per Segreteria Didattica](#9-guida-per-segreteria-didattica)
10. [Guida per il Coordinamento](#10-guida-per-il-coordinamento)
11. [Gestione dei conflitti](#11-gestione-dei-conflitti)
12. [Sedi e aule disponibili](#12-sedi-e-aule-disponibili)
13. [Credenziali di test](#13-credenziali-di-test)
14. [API e documentazione tecnica](#14-api-e-documentazione-tecnica)
15. [Risoluzione problemi comuni](#15-risoluzione-problemi-comuni)

---

## 1. Panoramica del sistema

Il **Sistema Prenotazione Aule** è un'applicazione web ad uso interno per la gestione delle prenotazioni degli spazi formativi dell'Agenzia. Consente di pianificare, validare e monitorare l'occupazione delle aule nelle sedi di **Torino, Cuneo, Asti, Novara e Biella**.

### Funzionalità principali

| Funzione | Descrizione |
|---|---|
| **Prenotazione singola** | Richiesta di un'aula per una data e fascia oraria specifica |
| **Prenotazione massiva** | Generazione automatica di slot ricorrenti (es. ogni lunedì per 3 mesi) |
| **Rilevamento conflitti** | Segnalazione automatica di sovrapposizioni, con possibilità di procedere comunque |
| **Workflow di approvazione** | Le richieste transitano da *In Attesa* → *Confermata* o *Rifiutata* |
| **Verifica capienza** | Controllo del limite di persone presenti contemporaneamente in sede |
| **Dashboard per ruolo** | Ogni utente vede solo le informazioni e le azioni pertinenti al suo ruolo |
| **Report saturazione** | Analisi dell'occupazione degli spazi per sede, aula e periodo |

### Architettura

```
┌─────────────────────┐         ┌──────────────────────┐
│   Frontend          │  HTTP   │   Backend            │
│   Streamlit :8501   │◄───────►│   FastAPI :8000      │
│   (browser)         │  REST   │   + SQLAlchemy ORM   │
└─────────────────────┘         └──────────┬───────────┘
                                            │
                                 ┌──────────▼───────────┐
                                 │   Database           │
                                 │   SQLite (dev)       │
                                 │   MySQL (prod)       │
                                 └──────────────────────┘
```

---

## 2. Requisiti di sistema

| Componente | Versione minima |
|---|---|
| Python | 3.11+ |
| pip | 23.0+ |
| Browser | Chrome 90+, Firefox 88+, Edge 90+ |
| Sistema operativo | Windows 10+, macOS 12+, Ubuntu 20.04+ |
| RAM | 4 GB consigliati |

---

## 3. Installazione e avvio

### 3.1 Prima installazione

```bash
# 1. Scarica o clona il progetto nella cartella desiderata
cd "ICE 1.0 - Planning Aule"

# 2. Crea l'ambiente virtuale Python
python -m venv ice_venv

# 3. Attiva l'ambiente virtuale
#    Windows:
ice_venv\Scripts\activate
#    Linux/Mac:
source ice_venv/bin/activate

# 4. Installa tutte le dipendenze
pip install -r requirements.txt

# 5. Crea il database e popola i dati iniziali (sedi, aule, utenti di test)
python -m backend.seed
```

### 3.2 Avvio quotidiano

Apri **due terminali separati** nella cartella del progetto, con l'ambiente virtuale attivo.

**Terminale 1 — Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminale 2 — Frontend:**
```bash
streamlit run frontend/app.py --server.port 8501
```

Apri il browser e vai su: **http://localhost:8501**

### 3.3 Verifica che tutto funzioni

- ✅ Backend attivo: http://localhost:8000 → risponde `{"status": "online"}`
- ✅ Frontend attivo: http://localhost:8501 → mostra la schermata di login
- ✅ API docs: http://localhost:8000/api/docs → Swagger UI interattivo

### 3.4 Variabili d'ambiente (file `.env`)

Il file `.env` nella root del progetto contiene le impostazioni principali:

```env
SECRET_KEY=cambia_questa_chiave_in_produzione
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
DATABASE_URL=sqlite:///./prenotazione_aule.db
```

> ⚠️ **In produzione**: sostituire `SECRET_KEY` con una stringa casuale lunga almeno 32 caratteri e cambiare `DATABASE_URL` con la stringa di connessione MySQL.

---

## 4. Struttura del progetto

```
ICE 1.0 - Planning Aule/
│
├── .env                          # Variabili d'ambiente
├── requirements.txt              # Dipendenze Python
├── README.md                     # Questo file
├── prenotazione_aule.db          # Database SQLite (generato automaticamente)
│
├── backend/                      # Server FastAPI
│   ├── main.py                   # Entry point + configurazione router
│   ├── config.py                 # Impostazioni applicazione
│   ├── database.py               # Connessione SQLAlchemy
│   ├── seed.py                   # Popolamento dati iniziali
│   ├── models/                   # Modelli ORM (tabelle database)
│   │   ├── enums.py              # Enumerazioni (ruoli, stati, tipi)
│   │   ├── utente.py             # Utenti e ruoli (STI)
│   │   ├── sede.py               # Sedi
│   │   ├── aula.py               # Aule
│   │   ├── corso.py              # Corsi
│   │   ├── slot_orario.py        # Slot temporali
│   │   ├── prenotazione.py       # Prenotazioni + Richieste + Conflitti
│   │   └── attrezzatura.py       # Attrezzature e richieste
│   ├── schemas/                  # Validazione dati Pydantic
│   ├── core/                     # Sicurezza, permessi, dipendenze
│   │   ├── security.py           # JWT + bcrypt
│   │   ├── permissions.py        # Matrice RBAC per 5 ruoli
│   │   └── dependencies.py       # Dependency injection FastAPI
│   ├── routers/                  # Endpoint API per area
│   └── services/                 # Logica di business
│       ├── booking_service.py    # Creazione prenotazioni
│       └── conflict_service.py   # Rilevamento conflitti
│
└── frontend/                     # Interfaccia Streamlit
    ├── app.py                    # Entry point frontend
    ├── config.py                 # Configurazione UI
    ├── api/                      # Client HTTP verso il backend
    ├── components/               # Componenti riutilizzabili (login, sidebar, alert)
    ├── pages/                    # Dashboard per ogni ruolo
    └── utils/                    # Funzioni di utilità
```

---

## 5. Accesso al sistema

### 5.1 Login

1. Apri **http://localhost:8501** nel browser
2. Inserisci la tua **email** e **password**
3. Clicca **Entra →**

La dashboard si adatta automaticamente al tuo ruolo: ogni utente vede solo le sezioni e le azioni che gli competono.

### 5.2 Logout

Clicca il pulsante **🚪 Logout** in fondo alla barra laterale sinistra.

### 5.3 Sessione

La sessione rimane attiva per **8 ore** dalla data di login. Alla scadenza verrai reindirizzato automaticamente alla pagina di login.

---

## 6. Guida per Responsabile Corso

> **Ruolo**: Richiede prenotazioni per i corsi di cui è responsabile.

### 6.1 Dashboard

La dashboard mostra un riepilogo delle tue prenotazioni:
- **Totale prenotazioni** inviate
- **In Attesa** di validazione
- **Confermate** dalla Segreteria
- **Con Conflitti** segnalati

Le *Prossime prenotazioni confermate* sono visibili nella sezione principale.

### 6.2 Nuova Prenotazione Singola

Usa questa funzione per prenotare un'aula per **una singola data e orario**.

**Passaggi:**

1. Dal menu laterale seleziona **📅 Nuova Prenotazione**
2. Scegli la **Sede** dall'elenco a tendina
3. Scegli l'**Aula** disponibile in quella sede
4. Seleziona il **Corso** da associare alla prenotazione
5. Indica la **Data** desiderata
6. Imposta l'**Ora di inizio** e l'**Ora di fine**
7. Aggiungi eventuali **Note** (facoltativo)
8. Clicca **📤 Invia Richiesta**

> 💡 **Nota sui conflitti**: se l'aula risulta già occupata in quella fascia oraria, il sistema lo segnala come **avviso** ma ti permette comunque di inviare la richiesta. Sarà la Segreteria di Sede a gestire la situazione.

**Esiti possibili:**
- ✅ *Richiesta inviata* → la Segreteria la validerà a breve
- ⚠️ *Richiesta inviata con conflitti* → la Segreteria è avvisata e gestirà il caso

### 6.3 Prenotazione Massiva (Ricorrente)

Usa questa funzione per prenotare un'aula per **più date ricorrenti** in automatico. Ideale per corsi che si svolgono ogni settimana per mesi.

**Esempio**: *Ogni lunedì e giovedì dalle 9:00 alle 13:00, dal 3 marzo al 30 giugno.*

**Passaggi:**

1. Dal menu seleziona **🔄 Prenotazione Massiva**
2. Scegli **Sede** e **Aula**
3. Seleziona il **Corso**
4. Imposta il **periodo** (data di inizio e data di fine)
5. Imposta l'**orario** (ora inizio e ora fine — uguale per tutti i giorni)
6. Scegli il **Tipo di ricorrenza**:
   - *Settimanale*: si ripete ogni settimana nei giorni selezionati
   - *Bisettimanale*: si ripete ogni due settimane
   - *Giornaliera*: ogni giorno lavorativo
   - *Mensile*: una volta al mese
7. Seleziona i **Giorni della settimana** (es. Lunedì e Giovedì)
8. Il sistema mostra una **stima del numero di slot** che verranno generati
9. Clicca **📤 Invia Richiesta Massiva**

> ⚠️ **Attenzione**: la prenotazione massiva genera tutti gli slot in una volta. Verifica attentamente il periodo e i giorni prima di confermare.

### 6.4 Le Mie Prenotazioni

Mostra l'elenco completo di tutte le tue prenotazioni con possibilità di filtrare per:
- **Stato**: In Attesa, Confermata, Rifiutata, Annullata, Conflitto
- **Periodo**: data di inizio e fine da esaminare

Ogni prenotazione è espandibile per vedere i dettagli degli slot.

**Legenda stati:**

| Stato | Significato |
|---|---|
| ⏳ **In Attesa** | Richiesta inviata, in attesa di validazione dalla Segreteria |
| ✅ **Confermata** | Approvata dalla Segreteria, l'aula è riservata |
| ❌ **Rifiutata** | Non approvata. Consulta le note di rifiuto per il motivo |
| ⚠️ **Conflitto** | Inviata ma con sovrapposizioni rilevate, in gestione |
| 🚫 **Annullata** | Cancellata |

### 6.5 Verifica Slot Disponibili

Usa questa funzione **prima** di inviare una richiesta per verificare se un'aula è libera.

**Passaggi:**

1. Seleziona **🔍 Slot Disponibili** dal menu
2. Scegli la Sede e l'Aula
3. Seleziona la data da verificare
4. Clicca **🔍 Verifica disponibilità**

Il sistema mostra gli **slot già occupati** in quella data. Se non ci sono occupazioni, l'aula è completamente libera.

---

## 7. Guida per Segreteria di Sede

> **Ruolo**: Valida, inserisce e gestisce le prenotazioni per la propria sede.

### 7.1 Dashboard

La dashboard mostra:
- Numero di richieste **da validare** (in attesa)
- Prenotazioni con **conflitti** da gestire
- Prenotazioni **confermate** nel mese
- Le prime 3 richieste pendenti con accesso rapido

### 7.2 Richieste Pendenti

Questa è la sezione principale del lavoro quotidiano: gestisci tutte le richieste in attesa di validazione.

**Per ogni richiesta puoi:**

**Approvare:**
1. Leggi i dettagli della prenotazione (aula, corso, slot, note)
2. Verifica l'assenza di problemi reali
3. Clicca **✅ Approva**
4. La prenotazione passa automaticamente allo stato *Confermata*

**Rifiutare:**
1. Scrivi il **motivo del rifiuto** nel campo di testo apposito
2. Clicca **❌ Rifiuta**
3. La prenotazione passa allo stato *Rifiutata* e il Responsabile Corso viene notificato

> ⚠️ **Richieste con conflitti**: le richieste contrassegnate con ⚠️ hanno sovrapposizioni con altre prenotazioni. Puoi comunque approvarle (se ritieni il conflitto gestibile) oppure rifiutarle spiegando il motivo.

### 7.3 Gestione Conflitti

Mostra esclusivamente le prenotazioni nello stato *Conflitto*. Per ognuna puoi:
- Leggere la descrizione del conflitto (tipo, orario sovrapposto, prenotazione esistente)
- **Approvare comunque** se il conflitto è risolvibile (es. aule diverse nel frattempo liberate)
- **Rifiutare** con motivazione

### 7.4 Calendario Sede

Visualizzazione cronologica di tutte le prenotazioni della sede in un intervallo di date.

**Come usarla:**
1. Imposta il periodo con **Dal** e **Al**
2. Le prenotazioni appaiono raggruppate per giorno
3. Per ogni giorno sono visibili: orario, aula, corso e stato

Utile per avere una fotografia giornaliera dell'occupazione degli spazi.

### 7.5 Gestione Aule

Permette di visualizzare le aule della sede e aggiungerne di nuove.

**Aggiungere un'aula:**
1. Scorri in fondo alla pagina *Gestione Aule*
2. Inserisci **Nome**, **Capienza** e **Note** (opzionale)
3. Clicca **➕ Aggiungi**

---

## 8. Guida per Responsabile di Sede

> **Ruolo**: Supervisiona lo stato degli spazi della propria sede, senza poter modificare le prenotazioni.

### 8.1 Dashboard

Panoramica immediata della sede con:
- Totale prenotazioni nella sede
- Prenotazioni di **oggi** (confermate)
- Richieste in attesa e conflitti aperti
- Metriche sintetiche per prendere decisioni rapide

### 8.2 Prenotazioni della Sede

Elenco completo delle prenotazioni della sede con filtri per:
- **Stato** (tutti, confermata, in attesa, ecc.)
- **Periodo** (data dal / al)

I risultati vengono mostrati in una tabella con: ID, tipo, aula, corso, stato, numero di slot e data del primo slot.

### 8.3 Saturazione Spazi

Analisi dell'occupazione delle aule nel **mese corrente**.

**Cosa mostra:**
- Per ogni aula: numero di slot occupati e ore totali occupate
- Tabella riepilogativa comparativa tra le aule
- **Grafico a barre** dell'occupazione per aula

Questa sezione risponde alla domanda: *"Le nostre aule vengono usate abbastanza? Quali sono sotto o sovra-utilizzate?"*

---

## 9. Guida per Segreteria Didattica

> **Ruolo**: Monitora le prenotazioni associate ai corsi di propria competenza.

### 9.1 Dashboard

Mostra:
- Numero di corsi gestiti
- Totale prenotazioni associate a questi corsi
- Riepilogo espandibile per ogni corso con: date, partecipanti, tipo di finanziamento e numero di prenotazioni confermate

### 9.2 Prenotazioni per Corso

Analisi dettagliata delle prenotazioni di un corso specifico.

**Come usarla:**
1. Seleziona il **Corso** dall'elenco a tendina
2. Filtra opzionalmente per **Stato**
3. Visualizza la tabella con tutte le prenotazioni: aula, stato, tipo, numero slot, date di inizio e fine

Utile per rispondere a domande come: *"Il corso X ha tutte le aule prenotate per il suo calendario?"*

---

## 10. Guida per il Coordinamento

> **Ruolo**: Visibilità globale su tutte le sedi, gestione utenti e reportistica completa.

### 10.1 Dashboard

Panoramica multi-sede con:
- Metriche aggregate (sedi attive, prenotazioni totali, confermate, in attesa, conflitti)
- **Tabella per sede**: confronto del numero di prenotazioni tra tutte le sedi
- **Grafico a torta**: distribuzione degli stati su tutte le prenotazioni

### 10.2 Vista Globale

Elenco completo di tutte le prenotazioni di tutte le sedi con filtri combinati:
- **Sede** specifica o tutte
- **Stato**
- **Periodo** (dal / al)

Esportabile per analisi esterne.

### 10.3 Report Saturazione

Genera un report di occupazione degli spazi per tutte le sedi in un periodo personalizzabile.

**Come generare un report:**
1. Imposta il periodo con **Dal** e **Al**
2. Clicca **📊 Genera Report**
3. Il sistema calcola per ogni aula di ogni sede: slot occupati e ore totali
4. Visualizza le metriche aggregate, la tabella dettagliata e il **grafico per sede**
5. Clicca **📥 Scarica CSV** per esportare i dati

**Metriche disponibili:**
- Aule analizzate
- Slot totali occupati nel periodo
- Ore totali occupate nel periodo
- Confronto per sede tramite grafico

### 10.4 Gestione Utenti

Visualizza tutti gli utenti registrati e crea nuovi account.

**Creare un nuovo utente:**
1. Vai in **👥 Gestione Utenti**
2. Nella sezione *Crea Nuovo Utente* compila:
   - **Nome** e **Cognome**
   - **Email** (sarà il nome utente per il login)
   - **Password** iniziale (comunicarla all'utente, che la cambierà)
   - **Ruolo** (vedi tabella sotto)
   - **Sede** di appartenenza (non necessaria per il Coordinamento)
3. Clicca **➕ Crea Utente**

**Ruoli disponibili:**

| Ruolo | Uso tipico |
|---|---|
| `responsabile_corso` | Docente o coordinatore del corso che prenota le aule |
| `responsabile_sede` | Referente della sede che monitora gli spazi |
| `segreteria_sede` | Operatore che valida e inserisce le prenotazioni |
| `segreteria_didattica` | Staff che gestisce il piano corsi |
| `coordinamento` | Direzione o staff centrale con visibilità globale |

### 10.5 Gestione Sedi

Visualizza tutte le sedi con le rispettive aule e aggiunge nuove sedi al sistema.

**Aggiungere una nuova sede:**
1. Scorri fino a *Aggiungi Sede*
2. Compila: **Nome sede**, **Indirizzo**, **Città**, **Capienza massima** (numero massimo di persone contemporaneamente presenti)
3. Clicca **➕ Aggiungi Sede**

---

## 11. Gestione dei conflitti

Il sistema di rilevamento conflitti è **non bloccante**: segnala il problema ma permette comunque di procedere con la richiesta. Questo consente flessibilità gestionale.

### Tipi di conflitto

| Tipo | Quando si verifica |
|---|---|
| **Sovrapposizione slot** | Un'altra prenotazione occupa già quell'aula in quella fascia oraria |
| **Capienza superata** | Il numero complessivo di persone in sede supera il limite configurato |
| **Attrezzatura non disponibile** | L'attrezzatura richiesta non è disponibile in quella data |

### Flusso di gestione

```
Responsabile Corso invia richiesta
         │
         ▼
  Conflitti presenti?
  ┌───── Sì ──────────────────────────────────┐
  │                                           │
  │  Stato → CONFLITTO                        │
  │  Segreteria riceve avviso ⚠️              │
  │                                           │
  │  Segreteria valuta:                       │
  │  ┌─ APPROVA → stato CONFERMATA            │
  │  └─ RIFIUTA (con motivo) → RIFIUTATA      │
  └───────────────────────────────────────────┘
         │
         No
         ▼
  Stato → IN_ATTESA
  Segreteria valida normalmente
         │
  ┌─ APPROVA → CONFERMATA
  └─ RIFIUTA → RIFIUTATA
```

---

## 12. Sedi e aule disponibili

| Sede | Città | N. Aule | Capienza max sede |
|---|---|---|---|
| Via Livorno 49 | Torino | 1 | 30 |
| Via Livorno 53 A | Torino | 1 | 50 |
| Via Livorno 53 B | Torino | 1 | 50 |
| Corso Svizzera 161 | Torino | 5 | 150 |
| Via Roma 1 | Cuneo | 2 | 60 |
| Corso Alba 10 | Asti | 3 | 80 |
| Via Biglieri 5 | Novara | 4 | 100 |
| Via Galileo 3 | Biella | 4 | 100 |

**Totale: 8 sedi | 21 aule**

---

## 13. Credenziali di test

> ⚠️ Queste credenziali sono **solo per l'ambiente di sviluppo/test**. In produzione vanno cambiate immediatamente tramite la funzione Gestione Utenti.

| Email | Password | Ruolo | Sede |
|---|---|---|---|
| `responsabile@test.it` | `Test1234!` | Responsabile Corso | Corso Svizzera |
| `resp.sede@test.it` | `Test1234!` | Responsabile di Sede | Corso Svizzera |
| `segr.sede@test.it` | `Test1234!` | Segreteria di Sede | Corso Svizzera |
| `segr.did@test.it` | `Test1234!` | Segreteria Didattica | Corso Svizzera |
| `coord@test.it` | `Test1234!` | Coordinamento | — |

---

## 14. API e documentazione tecnica

Il backend espone una REST API completa documentata automaticamente tramite **Swagger UI**.

### Accesso alla documentazione API

- **Swagger UI** (interattivo): http://localhost:8000/api/docs
- **ReDoc** (leggibile): http://localhost:8000/api/redoc

### Endpoint principali

| Metodo | Endpoint | Descrizione | Ruolo richiesto |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Login e ottenimento token JWT | Tutti |
| GET | `/api/v1/auth/me` | Profilo utente corrente | Tutti |
| GET | `/api/v1/sedi/` | Lista sedi | Tutti |
| GET | `/api/v1/aule/` | Lista aule (filtro per sede) | Tutti |
| POST | `/api/v1/prenotazioni/singola` | Nuova prenotazione singola | Responsabile Corso |
| POST | `/api/v1/prenotazioni/massiva` | Nuova prenotazione massiva | Responsabile Corso |
| GET | `/api/v1/prenotazioni/` | Lista prenotazioni (filtrata per ruolo) | Tutti |
| POST | `/api/v1/prenotazioni/richieste/{id}/approva` | Approva richiesta | Segreteria Sede |
| POST | `/api/v1/prenotazioni/richieste/{id}/rifiuta` | Rifiuta richiesta | Segreteria Sede |
| GET | `/api/v1/prenotazioni/slot-liberi/{aula_id}` | Slot occupati per aula | Tutti |
| GET | `/api/v1/utenti/` | Lista utenti | Coordinamento |
| POST | `/api/v1/utenti/` | Crea utente | Coordinamento |

### Autenticazione API

Tutte le chiamate (eccetto login) richiedono il token JWT nell'header:

```
Authorization: Bearer <token>
```

---

## 15. Risoluzione problemi comuni

### ❌ "No module named 'frontend'" all'avvio di Streamlit

**Causa**: Streamlit non trova il package `frontend` nel path Python.

**Soluzione**: Assicurati di lanciare il comando dalla **root del progetto**:
```bash
cd "ICE 1.0 - Planning Aule"
streamlit run frontend/app.py
```

---

### ❌ "Impossibile connettersi al backend"

**Causa**: Il server FastAPI non è avviato.

**Soluzione**:
1. Apri un terminale separato
2. Attiva l'ambiente virtuale
3. Esegui: `uvicorn backend.main:app --reload --port 8000`
4. Verifica che http://localhost:8000 risponda

---

### ❌ "Credenziali non valide" al login

**Causa**: Email o password errate, oppure account non ancora creato.

**Soluzione**:
- Verifica che il seed sia stato eseguito: `python -m backend.seed`
- Usa le credenziali di test dalla tabella al punto 13
- Se l'account non esiste, chiedi al Coordinamento di crearlo

---

### ❌ Il database non si crea / "Table not found"

**Causa**: Il seed non è stato eseguito o è fallito.

**Soluzione**:
```bash
# Elimina il database esistente (se corrotto)
del prenotazione_aule.db        # Windows
rm prenotazione_aule.db         # Linux/Mac

# Ricrea tutto
python -m backend.seed
```

---

### ❌ "Sessione scaduta" durante l'uso

**Causa**: Il token JWT è scaduto (default: 8 ore).

**Soluzione**: Clicca **Logout** e riesegui il login. La sessione riparte da zero.

---

### ⚠️ La prenotazione mostra stato "Conflitto" subito dopo l'invio

**Causa**: Il sistema ha rilevato una sovrapposizione con un'altra prenotazione nella stessa aula.

**Soluzione**: Non è un errore. La richiesta è stata comunque inviata. La Segreteria di Sede gestirà il conflitto e approverà o rifiuterà la prenotazione con motivazione. Puoi verificare preventivamente la disponibilità tramite **🔍 Slot Disponibili**.

---

### ❌ Errore all'avvio: "error reading bcrypt version"

**Causa**: Versione di `passlib` incompatibile con `bcrypt >= 4.0`.

**Soluzione**: Il progetto usa `bcrypt` direttamente (senza `passlib`). Verifica che `passlib` non sia installato:
```bash
pip uninstall passlib -y
pip install bcrypt==5.0.0
```

---

## Note finali

Per segnalare bug, richiedere nuove funzionalità o ottenere supporto tecnico, contattare il team di sviluppo allegando:
1. Lo screenshot del messaggio di errore
2. I passaggi eseguiti prima dell'errore
3. Il tuo ruolo nel sistema

---

*Gestionale ICE v1.0 — InforCoopEcipa*
