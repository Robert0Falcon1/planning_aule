// ─────────────────────────────────────────────────────────────────────────────
// API — Utenti
// ─────────────────────────────────────────────────────────────────────────────

import { apiGet, apiPost, apiDelete, apiPatch } from './client'

export async function getUtenti() {
  return apiGet('/utenti/')
}

/**
 * Crea utente.
 * @param {{ nome, cognome, email, ruolo, sede_id?, password }} payload
 */
export async function creaUtente(payload) {
  return apiPost('/utenti/', payload)
}

/**
 * Modifica dati utente esistente. Tutti i campi sono opzionali.
 * @param {number} id
 * @param {{ nome?, cognome?, email?, ruolo?, sede_id?, password? }} payload
 */
export async function modificaUtente(id, payload) {
  return apiPatch(`/utenti/${id}`, payload)
}

/**
 * Disattiva utente (soft-delete).
 */
export async function disattivaUtente(id) {
  return apiDelete(`/utenti/${id}`)
}

/**
 * Riattiva utente precedentemente disattivato.
 */
export async function attivaUtente(id) {
  return apiPatch(`/utenti/${id}/riattiva`)
}

// Alias per compatibilità con codice esistente
export const riattivaUtente = attivaUtente