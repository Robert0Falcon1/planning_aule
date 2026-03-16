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
 * Crea Prenotazione massiva.
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
 * Annulla uno slot specifico di una prenotazione.
 */
export async function annullaSlot(prenotazioneId, slotId) {
  return apiDelete(`/prenotazioni/${prenotazioneId}/slots/${slotId}`)
}

/**
 * Elimina/cancella l'intera prenotazione.
 */
export async function cancellaPrenotazione(id) {
  return apiDelete(`/prenotazioni/${id}`)
}

/**
 * Slot occupati per un'aula in un range di date.
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

// ─── Conflitti ────────────────────────────────────────────────────────────────
// FIX: rimosso fetchConflitti/BASE_CONFLITTI custom.
// Ora usano il client standard (VITE_API_URL + /api/v1 già incluso nel client).

export async function getConflitti(params = {}) {
  const qs = new URLSearchParams()
  if (params.sede_id !== undefined)     qs.set('sede_id',     params.sede_id)
  if (params.solo_attivi !== undefined) qs.set('solo_attivi', params.solo_attivi)
  const query = qs.toString() ? `?${qs}` : ''
  return apiGet(`/conflitti/${query}`)
}

export async function getConflitto(id) {
  return apiGet(`/conflitti/${id}`)
}

export async function risolviConflitto(id, azione, note = '') {
  const qs = new URLSearchParams({ azione })
  if (note) qs.set('note', note)
  return apiPost(`/conflitti/${id}/risolvi?${qs}`)
}

export async function getStatsConflitti(sedeId = null) {
  const query = sedeId ? `?sede_id=${sedeId}` : ''
  return apiGet(`/conflitti/stats/summary${query}`)
}

export async function modificaSlot(prenotazioneId, slotId, payload) {
  return apiPatch(`/prenotazioni/${prenotazioneId}/slots/${slotId}`, payload)
}