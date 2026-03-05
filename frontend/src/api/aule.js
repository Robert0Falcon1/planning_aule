// ─────────────────────────────────────────────────────────────────────────────
// API — Aule
// Schema: { id, nome, capienza, sede_id, note }
// NOTA: il backend NON ha campo "attiva" nelle aule
// ─────────────────────────────────────────────────────────────────────────────

import { apiGet, apiPost } from './client'

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

// NOTA: il backend non espone PUT/PATCH per aule
export async function modificaAula(id, payload) {
  console.warn('modificaAula: endpoint non disponibile nel backend')
  throw new Error('Modifica aula non supportata dal backend')
}