// ─────────────────────────────────────────────────────────────────────────────
// API — Autenticazione (login, profilo corrente)
// ─────────────────────────────────────────────────────────────────────────────

import apiClient from './client'

/**
 * Esegue il login e restituisce il token JWT con i dati utente.
 * Il backend FastAPI si aspetta form-data (OAuth2PasswordRequestForm).
 *
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{ access_token, token_type, ruolo, nome, cognome, email, sede_id }>}
 */
export async function login(email, password) {
  // OAuth2 richiede application/x-www-form-urlencoded
  const params = new URLSearchParams()
  params.append('username', email)
  params.append('password', password)

  const response = await apiClient.post('/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

/**
 * Recupera il profilo dell'utente autenticato tramite il token JWT.
 * @returns {Promise<UtenteRisposta>}
 */
export async function getMe() {
  const response = await apiClient.get('/auth/me')
  return response.data
}
