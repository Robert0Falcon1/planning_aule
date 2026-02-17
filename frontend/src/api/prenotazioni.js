// ─────────────────────────────────────────────────────────────────────────────
// API — Prenotazioni
// ─────────────────────────────────────────────────────────────────────────────

import apiClient from './client'

/**
 * Crea una prenotazione singola.
 * @param {{ aula_id, corso_id, slot: { data, ora_inizio, ora_fine }, note }} dati
 * @returns {Promise<Prenotazione>}
 */
export async function creaPrenotazioneSingola(dati) {
  const response = await apiClient.post('/prenotazioni/singola', dati)
  return response.data
}

/**
 * Crea una prenotazione massiva (ricorrente).
 * @param {{ aula_id, corso_id, data_inizio, data_fine, ora_inizio, ora_fine,
 *           tipo_ricorrenza, giorni_settimana, note }} dati
 * @returns {Promise<Prenotazione>}
 */
export async function creaPrenotazioneMassiva(dati) {
  const response = await apiClient.post('/prenotazioni/massiva', dati)
  return response.data
}

/**
 * Restituisce le prenotazioni visibili all'utente (filtrate lato backend per ruolo).
 * @param {{ sede_id?, corso_id?, stato?, data_dal?, data_al? }} filtri
 * @returns {Promise<Prenotazione[]>}
 */
export async function getPrenotazioni(filtri = {}) {
  // Rimuove le chiavi con valore null/undefined/stringa vuota
  const params = Object.fromEntries(
    Object.entries(filtri).filter(([, v]) => v !== null && v !== undefined && v !== ''),
  )
  const response = await apiClient.get('/prenotazioni/', { params })
  return response.data
}

/**
 * Restituisce il dettaglio di una singola prenotazione.
 * @param {number} id
 * @returns {Promise<Prenotazione>}
 */
export async function getPrenotazione(id) {
  const response = await apiClient.get(`/prenotazioni/${id}`)
  return response.data
}

/**
 * Approva una richiesta di prenotazione (Segreteria Sede).
 * @param {number} richiestaId
 * @returns {Promise<RichiestaPrenotazione>}
 */
export async function approvaRichiesta(richiestaId) {
  const response = await apiClient.post(`/prenotazioni/richieste/${richiestaId}/approva`)
  return response.data
}

/**
 * Rifiuta una richiesta di prenotazione con motivazione.
 * @param {number} richiestaId
 * @param {string} motivo
 * @returns {Promise<RichiestaPrenotazione>}
 */
export async function rifiutaRichiesta(richiestaId, motivo) {
  const response = await apiClient.post(
    `/prenotazioni/richieste/${richiestaId}/rifiuta`,
    null,
    { params: { motivo } },
  )
  return response.data
}
