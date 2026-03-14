// ─────────────────────────────────────────────────────────────────────────────
// API — Autenticazione
// ─────────────────────────────────────────────────────────────────────────────

import { apiGet, apiPost, BASE_URL } from './client'


/**
 * Login con credenziali.
 * Il backend FastAPI si aspetta form-data (OAuth2PasswordRequestForm).
 *
 * @param {string} username
 * @param {string} password
 * @returns {Promise<{ access_token, token_type, ruolo, nome_completo, email, sede_id }>}
 */
export async function login(username, password) {
  // OAuth2 richiede application/x-www-form-urlencoded — usiamo fetch diretto
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params,
  })

  if (!res.ok) {
    let msg = `Errore ${res.status}`
    try {
      const err = await res.json()
      msg = err.detail || err.message || msg
    } catch (_) {}
    throw new Error(msg)
  }

  return res.json()
}

/**
 * Recupera il profilo dell'utente autenticato.
 * @returns {Promise<UtenteRisposta>}
 */
export async function getMe() {
  return apiGet('/auth/me')
}

/**
 * Logout lato backend (invalida il token se il backend lo supporta).
 * Non obbligatorio — il logout client-side è sufficiente per JWT stateless.
 */
export async function logout() {
  try {
    await apiPost('/auth/logout')
  } catch (_) {
    // silenzioso: anche se fallisce, il token viene rimosso lato client
  }
}