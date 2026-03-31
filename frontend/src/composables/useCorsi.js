// composables/useCorsi.js
// ─────────────────────────────────────────────────────────────────────────────
// Composable per gestione corsi: caricamento centralizzato + helper ID→titolo
// ─────────────────────────────────────────────────────────────────────────────

import { ref, computed } from 'vue'
import { getCorsi } from '@/api/corsi'

// ── Stato singleton (condiviso tra tutti i componenti) ──────────────────────
const corsi = ref([])
const caricando = ref(false)
const caricato = ref(false)
const errore = ref(null)

// ── Funzione di caricamento (chiamata una sola volta) ────────────────────────
async function caricaCorsi(force = false) {
  if (caricato.value && !force) return corsi.value
  if (caricando.value) return corsi.value

  caricando.value = true
  errore.value = null

  try {
    corsi.value = await getCorsi()
    caricato.value = true
  } catch (e) {
    errore.value = e.message
    console.error('Errore caricamento corsi:', e)
  } finally {
    caricando.value = false
  }

  return corsi.value
}

// ── Composable ───────────────────────────────────────────────────────────────
export function useCorsi() {
  // Computed: solo corsi attivi (per i form)
  const corsiAttivi = computed(() => corsi.value.filter(c => c.attivo))

  // Mappa ID → corso (per lookup veloci)
  const corsiMap = computed(() => {
    const map = new Map()
    for (const c of corsi.value) {
      map.set(c.id, c)
    }
    return map
  })

  /**
   * Restituisce l'oggetto corso dato l'ID.
   * @param {number|string} id
   * @returns {Object|null}
   */
  function getCorsoById(id) {
    if (!id) return null
    return corsiMap.value.get(Number(id)) || null
  }

  /**
   * Formatta ID corso come "CODICE — Titolo" per visualizzazione.
   * @param {number|string} id
   * @returns {string}
   */
  function formatCorso(id) {
    const corso = getCorsoById(id)
    if (!corso) return `Corso #${id}`
    return `${corso.codice} — ${corso.titolo}`
  }

  /**
   * Restituisce solo il titolo del corso.
   * @param {number|string} id
   * @returns {string}
   */
  function getTitoloCorso(id) {
    const corso = getCorsoById(id)
    return corso?.titolo || `Corso #${id}`
  }

  /**
   * Restituisce solo il codice del corso.
   * @param {number|string} id
   * @returns {string}
   */
  function getCodiceCorso(id) {
    const corso = getCorsoById(id)
    return corso?.codice || `#${id}`
  }

  return {
    // Stato
    corsi,
    corsiAttivi,
    caricandoCorsi: caricando,
    corsiCaricati: caricato,
    erroreCorsi: errore,

    // Metodi
    caricaCorsi,
    getCorsoById,
    formatCorso,
    getTitoloCorso,
    getCodiceCorso,
  }
}