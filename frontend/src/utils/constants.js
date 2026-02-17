// ─────────────────────────────────────────────────────────────────────────────
// Costanti applicazione — specchio degli enum del backend Python
// ─────────────────────────────────────────────────────────────────────────────

/** Ruoli utente disponibili */
export const RUOLI = {
  RESPONSABILE_CORSO:   'responsabile_corso',
  RESPONSABILE_SEDE:    'responsabile_sede',
  SEGRETERIA_SEDE:      'segreteria_sede',
  SEGRETERIA_DIDATTICA: 'segreteria_didattica',
  COORDINAMENTO:        'coordinamento',
}

/** Etichette leggibili per i ruoli */
export const RUOLI_LABEL = {
  responsabile_corso:   'Responsabile Corso',
  responsabile_sede:    'Responsabile di Sede',
  segreteria_sede:      'Segreteria di Sede',
  segreteria_didattica: 'Segreteria Didattica',
  coordinamento:        'Coordinamento',
}

/** Stati possibili di una prenotazione */
export const STATI_PRENOTAZIONE = {
  IN_ATTESA:  'in_attesa',
  CONFERMATA: 'confermata',
  RIFIUTATA:  'rifiutata',
  ANNULLATA:  'annullata',
  CONFLITTO:  'conflitto',
}

/**
 * Configurazione badge Bootstrap per ogni stato.
 * Usa le classi Bootstrap Italia (compatibili BS5).
 */
export const STATI_BADGE = {
  in_attesa:  { class: 'bg-warning text-dark', label: 'In Attesa', icon: '⏳' },
  confermata: { class: 'bg-success',           label: 'Confermata', icon: '✅' },
  rifiutata:  { class: 'bg-danger',            label: 'Rifiutata', icon: '❌' },
  annullata:  { class: 'bg-secondary',         label: 'Annullata', icon: '🚫' },
  conflitto:  { class: 'bg-danger',            label: 'Conflitto', icon: '⚠️' },
}

/** Tipi di ricorrenza per prenotazioni massive */
export const TIPI_RICORRENZA = [
  { value: 'settimanale',   label: 'Settimanale (ogni settimana)' },
  { value: 'bisettimanale', label: 'Bisettimanale (ogni 2 settimane)' },
  { value: 'giornaliera',   label: 'Giornaliera (ogni giorno lavorativo)' },
  { value: 'mensile',       label: 'Mensile (una volta al mese)' },
]

/** Giorni della settimana (isoWeekday: 1=Lun … 7=Dom) */
export const GIORNI_SETTIMANA = [
  { value: 1, label: 'Lunedì' },
  { value: 2, label: 'Martedì' },
  { value: 3, label: 'Mercoledì' },
  { value: 4, label: 'Giovedì' },
  { value: 5, label: 'Venerdì' },
  { value: 6, label: 'Sabato' },
  { value: 7, label: 'Domenica' },
]

/** Tipi di finanziamento corso */
export const TIPI_FINANZIAMENTO = {
  finanziato_pubblico: 'Finanziato pubblico',
  a_pagamento:         'A pagamento',
  misto:               'Misto',
}
