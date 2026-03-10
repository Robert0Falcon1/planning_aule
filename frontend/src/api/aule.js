// ─────────────────────────────────────────────────────────────────────────────
// API — Aule
// Schema: { id, nome, capienza, sede_id, note, attiva }
// ─────────────────────────────────────────────────────────────────────────────

import { apiGet, apiPost, apiPut } from './client'

/** @param {{ sede_id? }} params */
export async function getAule(params = {}) {
  const qs = params.sede_id ? `?sede_id=${params.sede_id}` : ''
  return apiGet(`/aule/${qs}`)
}

export async function getAuleBySede(sedeId) {
  return apiGet(`/aule/?sede_id=${sedeId}`)
}

export async function getAula(id) {
  return apiGet(`/aule/${id}`)
}

/** @param {{ nome, capienza, sede_id, note? }} payload */
export async function creaAula(payload) {
  return apiPost('/aule/', payload)
}

/** @param {number} id @param {{ nome?, capienza?, note?, attiva? }} payload */
export async function modificaAula(id, payload) {
  return apiPut(`/aule/${id}`, payload)
}