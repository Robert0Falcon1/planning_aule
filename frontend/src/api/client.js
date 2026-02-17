// ─────────────────────────────────────────────────────────────────────────────
// Client HTTP centralizzato — Axios con intercettori JWT
// Tutte le chiamate al backend FastAPI passano da qui.
// ─────────────────────────────────────────────────────────────────────────────

import axios from 'axios'

/** Istanza Axios configurata per il backend FastAPI */
const apiClient = axios.create({
  baseURL: '/api/v1',          // Il proxy Vite inoltrerà a http://localhost:8000
  timeout: 10_000,             // 10 secondi di timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
})

// ── Interceptor di richiesta: aggiunge il token JWT se presente ───────────────
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// ── Interceptor di risposta: gestisce 401 (token scaduto) ────────────────────
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Rimuove il token scaduto e reindirizza al login
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_data')
      // Evita importazioni circolari: usa window.location
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

export default apiClient
