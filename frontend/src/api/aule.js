// ─────────────────────────────────────────────────────────────────────────────
// API — Aule e slot orari
// ─────────────────────────────────────────────────────────────────────────────

import apiClient from './client'

/**
 * Restituisce le aule, opzionalmente filtrate per sede.
 * @param {number|null} sedeId
 * @returns {Promise<Aula[]>}
 */
export async function getAule(sedeId = null) {
  const params = sedeId ? { sede_id: sedeId } : {}
  const response = await apiClient.get('/aule/', { params })
  return response.data
}

/**
 * Crea una nuova aula (Segreteria Sede o Coordinamento).
 * @param {{ nome, capienza, sede_id, note }} dati
 * @returns {Promise<Aula>}
 */
export async function creaAula(dati) {
  const response = await apiClient.post('/aule/', dati)
  return response.data
}

/**
 * Restituisce gli slot già occupati per un'aula in un range di date.
 * Utile per mostrare la disponibilità prima di prenotare.
 *
 * @param {number} aulaId
 * @param {string} dataDal  YYYY-MM-DD
 * @param {string} dataAl   YYYY-MM-DD
 * @returns {Promise<SlotOccupato[]>}
 */
export async function getSlotOccupati(aulaId, dataDal, dataAl) {
  const response = await apiClient.get(`/prenotazioni/slot-liberi/${aulaId}`, {
    params: { data_dal: dataDal, data_al: dataAl },
  })
  return response.data
}
