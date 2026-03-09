// ─────────────────────────────────────────────────────────────────────────────
// API — Prenotazioni
// ─────────────────────────────────────────────────────────────────────────────

import { apiGet, apiPost, apiPatch, apiDelete } from './client'

/**
 * Lista prenotazioni con filtri opzionali.
 * @param {{ sede_id?, corso_id?, stato?, data_dal?, data_al? }} params
 */
export async function getPrenotazioni(params = {}) {
  const qs = new URLSearchParams()
  if (params.sede_id)  qs.set('sede_id',  params.sede_id)
  if (params.corso_id) qs.set('corso_id', params.corso_id)
  if (params.stato)    qs.set('stato',    params.stato)
  if (params.data_dal) qs.set('data_dal', params.data_dal)
  if (params.data_al)  qs.set('data_al',  params.data_al)
  const query = qs.toString() ? `?${qs}` : ''
  return apiGet(`/prenotazioni/${query}`)
}

/**
 * Le mie prenotazioni — filtra lato client dall'elenco completo.
 * (Non esiste endpoint /mie nel backend)
 */
export async function getMiePrenotazioni(params = {}) {
  return getPrenotazioni(params)
}

/**
 * Crea prenotazione singola.
 * @param {{ aula_id, corso_id, slot: { data, ora_inizio, ora_fine }, note? }} payload
 */
export async function creaPrenotazione(payload) {
  return apiPost('/prenotazioni/singola', payload)
}

/**
 * Crea prenotazione massiva (ricorrente).
 * @param {{ aula_id, corso_id, data_inizio, data_fine, ora_inizio, ora_fine, tipo_ricorrenza, giorni_settimana?, note? }} payload
 */
export async function creaPrenotazioneMassiva(payload) {
  return apiPost('/prenotazioni/massiva', payload)
}

/**
 * Dettaglio singola prenotazione.
 */
export async function getPrenotazione(id) {
  return apiGet(`/prenotazioni/${id}`)
}

/**
 * Modifica prenotazione singola.
 * @param {{ aula_id?, corso_id?, slot?: { data, ora_inizio, ora_fine }, note? }} payload
 */
export async function modificaPrenotazione(id, payload) {
  return apiPatch(`/prenotazioni/${id}`, payload)
}

/**
 * Elimina/cancella prenotazione.
 */
export async function annullaSlot(prenotazioneId, slotId) {
  return apiDelete(`/prenotazioni/${prenotazioneId}/slots/${slotId}`)
}

export async function cancellaPrenotazione(id) {
  return apiDelete(`/prenotazioni/${id}`)
}

/**
 * Slot occupati per un'aula in un range di date.
 * Utile per calcolare disponibilità.
 */
export async function getSlotLiberi(aulaId, dataDal, dataAl) {
  return apiGet(`/prenotazioni/slot-liberi/${aulaId}?data_dal=${dataDal}&data_al=${dataAl}`)
}

/**
 * Calendario (usa lista prenotazioni con range date).
 */
export async function getCalendario(dataInizio, dataFine, sedeId = null) {
  const params = { data_dal: dataInizio, data_al: dataFine }
  if (sedeId) params.sede_id = sedeId
  return getPrenotazioni(params)
}

/**
 * Esporta CSV (non ancora implementato nel backend — placeholder).
 */
export async function esportaCsv(params = {}) {
  console.warn('esportaCsv: endpoint non disponibile nel backend')
}

// ─── Conflitti ───────────────────────────────────────────────────────────────
// NOTA: i conflitti usano /conflitti/ (senza /api/v1/)

const BASE_CONFLITTI = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace('/api/v1', '')

async function fetchConflitti(path, options = {}) {
  const token = localStorage.getItem('ice_token')
  const res = await fetch(`${BASE_CONFLITTI}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    ...options,
  })
  if (!res.ok) {
    let msg = `Errore ${res.status}`
    try { const e = await res.json(); msg = e.detail || msg } catch (_) {}
    throw new Error(msg)
  }
  return res.json()
}

export async function getConflitti(params = {}) {
  const qs = new URLSearchParams()
  if (params.sede_id)    qs.set('sede_id', params.sede_id)
  if (params.solo_attivi !== undefined) qs.set('solo_attivi', params.solo_attivi)
  const query = qs.toString() ? `?${qs}` : ''
  return fetchConflitti(`/conflitti/${query}`)
}

export async function getConflitto(id) {
  return fetchConflitti(`/conflitti/${id}`)
}

export async function risolviConflitto(id, azione, note = '') {
  return fetchConflitti(`/conflitti/${id}/risolvi?azione=${azione}&note=${encodeURIComponent(note)}`, { method: 'POST' })
}

export async function getStatsConflitti(sedeId = null) {
  const query = sedeId ? `?sede_id=${sedeId}` : ''
  return fetchConflitti(`/conflitti/stats/summary${query}`)
}