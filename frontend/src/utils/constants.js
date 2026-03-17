// ─────────────────────────────────────────────────────────────────────────────
// Costanti applicazione — specchio degli enum del backend Python
// Architettura 2 ruoli: OPERATIVO, COORDINAMENTO
// ─────────────────────────────────────────────────────────────────────────────

// ── Ruoli ─────────────────────────────────────────────────────────────────────

/** Ruoli utente (nuova architettura a 2 gruppi) */
export const RUOLI = {
  OPERATIVO:     'OPERATIVO',
  COORDINAMENTO: 'COORDINAMENTO',
}

/** Etichette leggibili per i ruoli */
export const RUOLI_LABEL = {
  OPERATIVO:     'Operativo',
  COORDINAMENTO: 'Coordinamento',
}

/**
 * Alias deprecati — mantenuti per non rompere le page in _archivio.
 * Da rimuovere quando si smonta definitivamente la vecchia struttura a 5 ruoli.
 * @deprecated
 */
export const RUOLI_LEGACY = {
  RESPONSABILE_CORSO:   'responsabile_corso',
  RESPONSABILE_SEDE:    'responsabile_sede',
  SEGRETERIA_SEDE:      'segreteria_sede',
  SEGRETERIA_DIDATTICA: 'segreteria_didattica',
  COORDINAMENTO:        'coordinamento',
}

// ── Prenotazioni ──────────────────────────────────────────────────────────────

/** Stati possibili di una prenotazione */
export const STATI_PRENOTAZIONE = {
  CONFERMATA: 'confermata',
  ANNULLATA:  'annullata',
  CONFLITTO:  'conflitto',
  // Legacy — rimossi dal workflow ma presenti in dati storici
  IN_ATTESA: 'in_attesa',
  RIFIUTATA: 'rifiutata',
}

/**
 * Configurazione badge Bootstrap Italia per ogni stato.
 * Compatibile BS5/Bootstrap Italia.
 */
export const STATI_BADGE = {
  confermata: { class: 'bg-success',           label: 'Confermata', icon: '✅' },
  annullata:  { class: 'bg-secondary',         label: 'Annullata',  icon: '🚫' },
  conflitto:  { class: 'bg-danger',            label: 'Conflitto',  icon: '⚠️' },
  // Legacy
  in_attesa:  { class: 'bg-warning text-dark', label: 'In Attesa',  icon: '⏳' },
  rifiutata:  { class: 'bg-danger',            label: 'Rifiutata',  icon: '❌' },
}

// ── Prenotazioni massive ──────────────────────────────────────────────────────

/** Giorni della settimana selezionabili (isoWeekday: 1=Lun … 7=Dom) */
export const GIORNI_SETTIMANA = [
  { value: 1, label: 'Lunedì' },
  { value: 2, label: 'Martedì' },
  { value: 3, label: 'Mercoledì' },
  { value: 4, label: 'Giovedì' },
  { value: 5, label: 'Venerdì' },
  { value: 6, label: 'Sabato' },
  { value: 7, label: 'Domenica' },
]

// ── Corsi ─────────────────────────────────────────────────────────────────────

/** Tipi di finanziamento corso */
export const TIPI_FINANZIAMENTO = {
  finanziato_pubblico: 'Finanziato pubblico',
  a_pagamento:         'A pagamento',
  misto:               'Misto',
}

// ── Calendario ────────────────────────────────────────────────────────────────

/** Ore disponibili per slot orari (HH:MM, passo 30 min) */
export const ORE_SLOT = Array.from({ length: 28 }, (_, i) => {
  const totalMin = 7 * 60 + i * 30   // dalle 07:00 alle 20:30
  const h = String(Math.floor(totalMin / 60)).padStart(2, '0')
  const m = String(totalMin % 60).padStart(2, '0')
  return `${h}:${m}`
})

/** Colori per aula nel calendario (riutilizzati ciclicamente) */
export const COLORI_AULA = [
  '#0066CC',
  '#008D62',
  '#A04000',
  '#6C3483',
  '#B7950B',
  '#C0392B',
  '#117A65',
  '#1A5276',
  '#6E2C00',
  '#4A235A',
  '#1E8449',
  '#784212',
  '#1B2631',
  '#922B21',
  '#0E6655',
]