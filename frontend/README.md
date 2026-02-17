# 🏫 Sistema Prenotazione Aule — Frontend Vue.js

> Migrazione da Streamlit a **Vue 3 + Bootstrap Italia**

---

## Stack tecnologico

| Tecnologia | Versione | Uso |
|---|---|---|
| **Vue 3** | ^3.4 | Framework UI con Composition API |
| **Pinia** | ^2.1 | State management (auth, sessione) |
| **Vue Router** | ^4.3 | Routing SPA con route guard per ruolo |
| **Bootstrap Italia** | ^2.8 | Design system PA italiana |
| **Axios** | ^1.6 | Client HTTP verso FastAPI |
| **Day.js** | ^1.11 | Formattazione date in italiano |
| **Vite** | ^5.0 | Build tool (dev + prod) |

---

## Struttura del progetto

```
frontend-vue/
├── src/
│   ├── api/              # Client HTTP per ogni endpoint
│   │   ├── client.js     # Axios instance con JWT interceptor
│   │   ├── auth.js
│   │   ├── sedi.js
│   │   ├── aule.js
│   │   ├── corsi.js
│   │   ├── prenotazioni.js
│   │   └── utenti.js
│   ├── stores/
│   │   └── auth.js       # Pinia store: token, user, login/logout
│   ├── router/
│   │   └── index.js      # Route + guard ruolo + SIDEBAR_LINKS
│   ├── components/
│   │   ├── layout/
│   │   │   └── AppLayout.vue   # Layout con sidebar + topbar
│   │   └── common/
│   │       ├── StatoBadge.vue  # Badge colorato per stato prenotazione
│   │       └── CardMetrica.vue # Card KPI con icona e colore
│   ├── views/
│   │   ├── LoginView.vue
│   │   ├── responsabile_corso/   (5 pagine)
│   │   ├── segreteria_sede/      (5 pagine)
│   │   ├── responsabile_sede/    (3 pagine)
│   │   ├── segreteria_didattica/ (2 pagine)
│   │   └── coordinamento/        (5 pagine)
│   ├── utils/
│   │   └── helpers.js    # formatData, formatOra, costanti
│   └── assets/
│       └── main.scss     # CSS custom (variabili, layout, componenti)
```

---

## Installazione

```bash
# Dalla cartella del progetto ICE
cd frontend-vue

# Installa le dipendenze
npm install

# Avvia in sviluppo (usa proxy verso FastAPI :8000)
npm run dev
```

Il frontend sarà disponibile su **http://localhost:3000**

---

## Configurazione backend

Il file `vite.config.js` configura un proxy che reindirizza `/api` verso FastAPI:

```js
proxy: {
  '/api': { target: 'http://localhost:8000', changeOrigin: true }
}
```

Non è necessario modificare nulla nel backend FastAPI o nel CORS — il proxy Vite
evita i problemi cross-origin in sviluppo.

> **In produzione**: configurare Nginx/Traefik per servire i file statici Vue
> e fare reverse proxy di `/api` verso FastAPI, come indicato nel Deployment Diagram.

---

## Avvio completo (dev)

**Terminale 1 — Backend FastAPI:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminale 2 — Frontend Vue:**
```bash
cd frontend-vue
npm run dev
```

Apri **http://localhost:3000** e accedi con le credenziali di test.

---

## Routing per ruolo

| Ruolo | Dashboard | Redirect automatico |
|---|---|---|
| `responsabile_corso` | `/dashboard` | Login → `/dashboard` |
| `segreteria_sede` | `/ss/dashboard` | Login → `/ss/dashboard` |
| `responsabile_sede` | `/rs/dashboard` | Login → `/rs/dashboard` |
| `segreteria_didattica` | `/sd/dashboard` | Login → `/sd/dashboard` |
| `coordinamento` | `/co/dashboard` | Login → `/co/dashboard` |

Il route guard in `router/index.js` gestisce:
- Redirect a `/login` se non autenticato
- Redirect al dashboard corretto in base al ruolo

---

## Build produzione

```bash
npm run build
# Output in frontend-vue/dist/
```

Copiare il contenuto di `dist/` nella root servita da Nginx/Traefik.

---

## Differenze rispetto a Streamlit

| Aspetto | Streamlit | Vue 3 + BI |
|---|---|---|
| **Rendering** | Server-side (Python) | Client-side SPA |
| **Performance** | Ogni azione ricarica il componente | Reattività fine-grained, no reload |
| **Autenticazione** | `st.session_state` (server) | `localStorage` + Pinia (client) |
| **Routing** | Pagine simulate con `st.session_state` | Vue Router nativo con URL reali |
| **Stile** | Streamlit default | Bootstrap Italia (design system PA) |
| **Deploy** | Richiede Python runtime | Solo file statici (CDN, Nginx) |
| **Mobile** | Parzialmente responsive | Fully responsive con breakpoint BI |
