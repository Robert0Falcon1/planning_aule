// ─────────────────────────────────────────────────────────────────────────────
// API — Sedi
// Schema: { id, nome, indirizzo, citta, capienza_massima }
// ─────────────────────────────────────────────────────────────────────────────

import { apiGet, apiPost, apiPatch } from './client'

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

/** @param {number} id @param {{ nome?, indirizzo?, citta?, capienza_massima? }} payload */
export async function modificaSede(id, payload) {
  return apiPatch(`/sedi/${id}`, payload)
}