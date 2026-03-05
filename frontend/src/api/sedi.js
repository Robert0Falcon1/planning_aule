// ─────────────────────────────────────────────────────────────────────────────
// API — Sedi
// Schema: { id, nome, indirizzo, citta, capienza_massima }
// ─────────────────────────────────────────────────────────────────────────────

import { apiGet, apiPost } from './client'

export async function getSedi() {
  return apiGet('/sedi/')
}

export async function getSede(id) {
  return apiGet(`/sedi/${id}`)
}

/** @param {{ nome, indirizzo, citta, capienza_massima? }} payload */
export async function creaSede(payload) {
  return apiPost('/sedi/', payload)
}

// NOTA: il backend non espone PUT/PATCH per sedi — modificaSede non disponibile
export async function modificaSede(id, payload) {
  console.warn('modificaSede: endpoint non disponibile nel backend')
  throw new Error('Modifica sede non supportata dal backend')
}

export async function eliminaSede(id) {
  console.warn('eliminaSede: endpoint non disponibile nel backend')
  throw new Error('Eliminazione sede non supportata dal backend')
}