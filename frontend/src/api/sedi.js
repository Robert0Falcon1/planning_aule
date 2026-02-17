// ─────────────────────────────────────────────────────────────────────────────
// API — Sedi
// ─────────────────────────────────────────────────────────────────────────────

import apiClient from './client'

/**
 * Restituisce l'elenco di tutte le sedi attive.
 * @returns {Promise<Sede[]>}
 */
export async function getSedi() {
  const response = await apiClient.get('/sedi/')
  return response.data
}

/**
 * Restituisce il dettaglio di una sede.
 * @param {number} sedeId
 * @returns {Promise<Sede>}
 */
export async function getSede(sedeId) {
  const response = await apiClient.get(`/sedi/${sedeId}`)
  return response.data
}

/**
 * Crea una nuova sede (solo Coordinamento).
 * @param {{ nome, indirizzo, citta, capienza_massima }} dati
 * @returns {Promise<Sede>}
 */
export async function creaSede(dati) {
  const response = await apiClient.post('/sedi/', dati)
  return response.data
}
