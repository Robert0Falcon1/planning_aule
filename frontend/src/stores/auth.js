// ─────────────────────────────────────────────────────────────────────────────
// Store — Autenticazione
// TokenResponse: { access_token, token_type, ruolo, nome, cognome, email, sede_id }
// ─────────────────────────────────────────────────────────────────────────────

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiGet } from '@/api/client'
import { login as apiLogin } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // ─── State ────────────────────────────────────────────────────────────────
  const raw     = localStorage.getItem('ice_utente')
  const utente  = ref(raw && raw !== 'undefined' && raw !== 'null' ? JSON.parse(raw) : null)
  const token   = ref(localStorage.getItem('ice_token') || null)
  const loading = ref(false)
  const errore  = ref(null)
  const inizializzato = ref(false)

  // ─── Computed ─────────────────────────────────────────────────────────────
  const isAuthenticated = computed(() => !!token.value && !!utente.value)
  const ruolo           = computed(() => utente.value?.ruolo || null)
  const isCoordinamento = computed(() => ruolo.value === 'COORDINAMENTO')
  const isOperativo     = computed(() => ruolo.value === 'OPERATIVO')

  // nome/cognome separati nel backend
  const nomeUtente = computed(() => {
    if (!utente.value) return ''
    const full = `${utente.value.nome || ''} ${utente.value.cognome || ''}`.trim()
    return full || utente.value.email || ''
  })

  // Solo il nome
  const nomeUtenteInformale = computed(() => utente.value?.nome || '')

  // ─── Actions ──────────────────────────────────────────────────────────────
  async function login(username, password) {
    loading.value = true
    errore.value  = null
    try {
      // 1. Login → riceve TokenResponse con i dati base
      const data = await apiLogin(username, password)
      token.value = data.access_token
      localStorage.setItem('ice_token', data.access_token)

      // 2. Salva subito i dati base dal token (nome, cognome, ruolo, sede_id)
      const utenteBase = {
        nome:     data.nome,
        cognome:  data.cognome,
        email:    data.email,
        ruolo:    data.ruolo,
        sede_id:  data.sede_id,
      }
      utente.value = utenteBase
      localStorage.setItem('ice_utente', JSON.stringify(utenteBase))

      // 3. Arricchisce con profilo completo da /auth/me (id, attivo, ecc.)
      try {
        const me = await apiGet('/auth/me')
        utente.value = { ...utenteBase, ...me }
        localStorage.setItem('ice_utente', JSON.stringify(utente.value))
      } catch (_) {
        // /auth/me fallita — va bene, usiamo i dati base
      }

      return true
    } catch (e) {
      errore.value = e.message || 'Credenziali non valide'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try { await apiGet('/auth/logout') } catch (_) { /* ignora */ }
    token.value  = null
    utente.value = null
    localStorage.removeItem('ice_token')
    localStorage.removeItem('ice_utente')
  }

  async function refreshMe() {
    if (!token.value) {
      inizializzato.value = true
      return
    }
    try {
      const me = await apiGet('/auth/me')
      utente.value = me
      localStorage.setItem('ice_utente', JSON.stringify(me))
    } catch (_) {
      await logout()
    } finally {
      inizializzato.value = true
    }
  }

  return {
    utente, token, loading, errore, inizializzato,
    isAuthenticated, ruolo, nomeUtente, nomeUtenteInformale, isCoordinamento, isOperativo,
    login, logout, refreshMe,
  }
})