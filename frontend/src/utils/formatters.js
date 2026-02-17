// ─────────────────────────────────────────────────────────────────────────────
// Funzioni di utilità — formattazione date, ore e valori da mostrare in UI
// ─────────────────────────────────────────────────────────────────────────────

import { STATI_BADGE, RUOLI_LABEL, TIPI_FINANZIAMENTO } from './constants'

/**
 * Formatta una data ISO (YYYY-MM-DD) nel formato italiano (DD/MM/YYYY).
 * @param {string|null} isoDate
 * @returns {string}
 */
export function formatData(isoDate) {
  if (!isoDate) return '—'
  const [y, m, d] = isoDate.split('T')[0].split('-')
  return `${d}/${m}/${y}`
}

/**
 * Formatta una data ISO con ora (es. "2024-03-15T09:00:00") in modo leggibile.
 * @param {string|null} isoDateTime
 * @returns {string}
 */
export function formatDataOra(isoDateTime) {
  if (!isoDateTime) return '—'
  const dt = new Date(isoDateTime)
  return dt.toLocaleString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

/**
 * Formatta un orario HH:MM:SS in HH:MM.
 * @param {string|null} timeStr
 * @returns {string}
 */
export function formatOra(timeStr) {
  if (!timeStr) return '—'
  return timeStr.slice(0, 5)
}

/**
 * Restituisce la configurazione del badge Bootstrap per uno stato prenotazione.
 * @param {string} stato
 * @returns {{ class: string, label: string, icon: string }}
 */
export function badgeStato(stato) {
  return STATI_BADGE[stato] ?? { class: 'bg-secondary', label: stato, icon: '' }
}

/**
 * Etichetta leggibile per un ruolo utente.
 * @param {string} ruolo
 * @returns {string}
 */
export function labelRuolo(ruolo) {
  return RUOLI_LABEL[ruolo] ?? ruolo
}

/**
 * Etichetta leggibile per un tipo di finanziamento.
 * @param {string} tipo
 * @returns {string}
 */
export function labelFinanziamento(tipo) {
  return TIPI_FINANZIAMENTO[tipo] ?? tipo
}

/**
 * Tronca una stringa aggiungendo "…" se supera maxLen caratteri.
 * @param {string} str
 * @param {number} maxLen
 * @returns {string}
 */
export function tronca(str, maxLen = 60) {
  if (!str) return ''
  return str.length > maxLen ? str.slice(0, maxLen) + '…' : str
}

/**
 * Restituisce la data odierna in formato YYYY-MM-DD (compatibile con <input type="date">).
 * @returns {string}
 */
export function oggi() {
  return new Date().toISOString().split('T')[0]
}
