// ─────────────────────────────────────────────────────────────────────────────
// API — Utenti
// Endpoints: GET /utenti/, POST /utenti/, DELETE /utenti/{id}, PATCH /utenti/{id}/riattiva
// NOTA: non esiste endpoint PATCH per modifica dati utente
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

// NOTA: non esiste endpoint per modificare i dati utente
export async function modificaUtente(id, payload) {
  console.warn('modificaUtente: endpoint non disponibile nel backend')
  throw new Error('Modifica utente non supportata dal backend')
}