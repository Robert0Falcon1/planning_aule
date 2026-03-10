// ─────────────────────────────────────────────────────────────────────────────
// API — Corsi
// ─────────────────────────────────────────────────────────────────────────────
// TODO: integrare getCorsi() in NuovaPrenotazionePage.vue per sostituire
//       l'input numerico corso_id con una <select> caricata da backend.
//       Uso: const corsi = await getCorsi({ attivo: true, sede_id: sedeId })

import { apiGet } from './client'

/**
 * Lista corsi con filtri opzionali.
 * @param {{ sede_id?: number, attivo?: boolean }} params
 * @returns {Promise<Array<{ id, codice, titolo, sede_id, stato_del_corso, tipo_finanziamento, data_inizio_corso, data_fine_presunta, attivo }>>}
 */
export async function getCorsi(params = {}) {
  const qs = new URLSearchParams()
  if (params.sede_id !== undefined) qs.set('sede_id', params.sede_id)
  if (params.attivo  !== undefined) qs.set('attivo',  params.attivo)
  const query = qs.toString() ? `?${qs}` : ''
  return apiGet(`/corsi/${query}`)
}

/**
 * Dettaglio completo di un corso.
 * @param {number} id
 */
export async function getCorso(id) {
  return apiGet(`/corsi/${id}`)
}