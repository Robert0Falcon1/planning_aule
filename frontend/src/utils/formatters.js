// ─────────────────────────────────────────────────────────────────────────────
// Funzioni di utilità — formattazione valori per la UI
// ─────────────────────────────────────────────────────────────────────────────

import { STATI_BADGE, RUOLI_LABEL, TIPI_FINANZIAMENTO } from './constants'

// ── Date e ore ────────────────────────────────────────────────────────────────

/**
 * Restituisce la data odierna in formato YYYY-MM-DD.
 * @returns {string}
 */
export function oggi() {
  return new Date().toISOString().split('T')[0]
}

/**
 * Formatta una data ISO (YYYY-MM-DD o ISO full) nel formato italiano DD/MM/YYYY.
 * @param {string|null} isoDate
 * @returns {string}
 */
export function formatData(isoDate) {
  if (!isoDate) return '—'
  const [y, m, d] = isoDate.split('T')[0].split('-')
  return `${d}/${m}/${y}`
}

/**
 * Formatta una data ISO con ora in formato italiano leggibile.
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
 * Formatta un range orario in "09:00–11:30".
 * @param {string} oraInizio
 * @param {string} oraFine
 * @returns {string}
 */
export function formatRangeOra(oraInizio, oraFine) {
  return `${formatOra(oraInizio)}–${formatOra(oraFine)}`
}

/**
 * Aggiunge (o sottrae) N giorni a una data ISO YYYY-MM-DD.
 */
export function aggiungiGiorni(isoDate, giorni) {
  const [y, m, d] = isoDate.split('-').map(Number)
  const data = new Date(y, m - 1, d)
  data.setDate(data.getDate() + giorni)
  return [
    data.getFullYear(),
    String(data.getMonth() + 1).padStart(2, '0'),
    String(data.getDate()).padStart(2, '0'),
  ].join('-')
}

export function inizioSettimana(isoDate) {
  const [y, m, d] = isoDate.split('-').map(Number)
  const data = new Date(y, m - 1, d)
  const giorno = data.getDay() || 7        // domenica = 7
  data.setDate(data.getDate() - giorno + 1) // lunedì
  return [
    data.getFullYear(),
    String(data.getMonth() + 1).padStart(2, '0'),
    String(data.getDate()).padStart(2, '0'),
  ].join('-')
}

export function fineSettimana(isoDate) {
  return aggiungiGiorni(inizioSettimana(isoDate), 6)
}

/**
 * Restituisce il nome del giorno della settimana in italiano.
 * @param {string} isoDate  YYYY-MM-DD
 * @returns {string}  es. "Lunedì"
 */
export function nomeGiorno(isoDate) {
  if (!isoDate) return '—'
  const dt = new Date(isoDate + 'T00:00:00')
  return dt.toLocaleDateString('it-IT', { weekday: 'long' })
    .replace(/^\w/, c => c.toUpperCase())
}

// ── Stato e ruolo ─────────────────────────────────────────────────────────────

/**
 * Configurazione badge Bootstrap per uno stato prenotazione.
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
  return RUOLI_LABEL[ruolo] ?? RUOLI_LABEL[ruolo?.toUpperCase()] ?? ruolo
}

// ── Testo ─────────────────────────────────────────────────────────────────────

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
 * @param {string|null} str
 * @param {number} maxLen
 * @returns {string}
 */
export function tronca(str, maxLen = 60) {
  if (!str) return ''
  return str.length > maxLen ? str.slice(0, maxLen) + '…' : str
}

/**
 * Capitalizza la prima lettera di una stringa.
 * @param {string|null} str
 * @returns {string}
 */
export function capitalizza(str) {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

/**
 * Calcola la percentuale di val su tot (arrotondato intero).
 * @param {number} val
 * @param {number} tot
 * @returns {number}
 */
export function percentuale(val, tot) {
  if (!tot) return 0
  return Math.round((val / tot) * 100)
}