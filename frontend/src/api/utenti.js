// ─────────────────────────────────────────────────────────────────────────────
// API — Utenti (solo Coordinamento)
// ─────────────────────────────────────────────────────────────────────────────

import client from './client'

/** Lista completa degli utenti */
export async function getUtenti() {
  const res = await client.get('/utenti/')
  return res.data
}

/** Crea un nuovo utente */
export async function creaUtente(dati) {
  const res = await client.post('/utenti/', dati)
  return res.data
}

/** Disattiva (soft-delete) un utente */
export async function disattivaUtente(utenteId) {
  const res = await client.delete(`/utenti/${utenteId}`)
  return res.data
}

/** Riattiva un utente precedentemente disattivato */
export async function riattivaUtente(utenteId) {
  const res = await client.patch(`/utenti/${utenteId}/riattiva`)
  return res.data
}
