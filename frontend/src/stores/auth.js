// ─────────────────────────────────────────────────────────────────────────────
// Store — Autenticazione (Pinia)
// Gestisce token JWT, dati utente e persistenza su localStorage.
// ─────────────────────────────────────────────────────────────────────────────

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, getMe } from '@/api/auth'
import { RUOLI } from '@/utils/constants'

export const useAuthStore = defineStore('auth', () => {
  // ── Stato ──────────────────────────────────────────────────────────────────
  const token  = ref(localStorage.getItem('access_token') ?? null)
  const user   = ref(
    localStorage.getItem('user_data')
      ? JSON.parse(localStorage.getItem('user_data'))
      : null,
  )
  /** True dopo che init() ha completato la verifica del token */
  const inizializzato = ref(false)

  // ── Getter (computed) ──────────────────────────────────────────────────────
  /** True solo se il token è presente ED i dati utente sono stati validati */
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const ruolo        = computed(() => user.value?.ruolo ?? null)
  const sedeId       = computed(() => user.value?.sede_id ?? null)
  const nomeCompleto = computed(() =>
    user.value ? `${user.value.nome} ${user.value.cognome}` : '',
  )

  const hasRole = (...roles) => roles.includes(ruolo.value)

  const isResponsabileCorso   = computed(() => ruolo.value === RUOLI.RESPONSABILE_CORSO)
  const isSegreteriaSede      = computed(() => ruolo.value === RUOLI.SEGRETERIA_SEDE)
  const isResponsabileSede    = computed(() => ruolo.value === RUOLI.RESPONSABILE_SEDE)
  const isSegreteriaDidattica = computed(() => ruolo.value === RUOLI.SEGRETERIA_DIDATTICA)
  const isCoordinamento       = computed(() => ruolo.value === RUOLI.COORDINAMENTO)

  // ── Azioni ────────────────────────────────────────────────────────────────

  /**
   * Chiamato UNA VOLTA al boot in main.js prima del mount.
   * Verifica che il token in localStorage sia ancora valido.
   * Se il backend risponde 401 (token scaduto/invalido), fa logout silenzioso.
   */
  async function init() {
    if (!token.value) {
      // Nessun token salvato: utente non autenticato, vai al login
      inizializzato.value = true
      return
    }
    try {
      // Chiamata reale al backend: lancia eccezione se token invalido/scaduto
      const me = await getMe()
      user.value = me
      localStorage.setItem('user_data', JSON.stringify(me))
    } catch {
      // Token invalido, scaduto o backend irraggiungibile: pulizia silenziosa
      _clearSession()
    } finally {
      inizializzato.value = true
    }
  }

  /** Esegue il login e salva token + dati utente. */
  async function login(email, password) {
    const data = await apiLogin(email, password)
    token.value = data.access_token
    localStorage.setItem('access_token', data.access_token)
    const { access_token, token_type, ...userData } = data
    user.value = userData
    localStorage.setItem('user_data', JSON.stringify(userData))
  }

  /** Cancella la sessione e forza il redirect al login. */
  function logout() {
    _clearSession()
  }

  function _clearSession() {
    token.value = null
    user.value  = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_data')
  }

  return {
    token, user, inizializzato, isAuthenticated,
    ruolo, sedeId, nomeCompleto, hasRole,
    isResponsabileCorso, isSegreteriaSede, isResponsabileSede,
    isSegreteriaDidattica, isCoordinamento,
    init, login, logout,
  }
})
