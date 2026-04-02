/**
 * API per la gestione dei docenti
 */
import { apiGet } from './client'

/**
 * Recupera la lista dei docenti
 * @param {Object} filtri - Filtri opzionali
 * @param {number} filtri.sede_id - Filtra per sede
 * @param {boolean} filtri.attivi - Mostra solo docenti attivi (default: true)
 * @returns {Promise<Array>} Lista docenti
 */
export async function getDocenti(filtri = {}) {
  const params = {}
  
  if (filtri.sede_id) params.sede_id = filtri.sede_id
  if (filtri.attivi !== undefined) params.attivi = filtri.attivi
  
  return await apiGet('/docenti', params)
}

/**
 * Recupera un singolo docente per ID
 * @param {number} id - ID del docente
 * @returns {Promise<Object>} Docente
 */
export async function getDocente(id) {
  return await apiGet(`/docenti/${id}`)
}