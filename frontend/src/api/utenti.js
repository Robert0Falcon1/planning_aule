// ─────────────────────────────────────────────────────────────────────────────
// API — Utenti (solo Coordinamento)
// ─────────────────────────────────────────────────────────────────────────────

import apiClient from './client'

/**
 * Restituisce tutti gli utenti registrati.
 * @returns {Promise<Utente[]>}
 */
export async function getUtenti() {
  const response = await apiClient.get('/utenti/')
  return response.data
}

/**
 * Crea un nuovo utente nel sistema.
 * @param {{ nome, cognome, email, password, ruolo, sede_id? }} dati
 * @returns {Promise<Utente>}
 */
export async function creaUtente(dati) {
  const response = await apiClient.post('/utenti/', dati)
  return response.data
}
