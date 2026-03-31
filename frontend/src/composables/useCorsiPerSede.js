// composables/useCorsiPerSede.js
// ─────────────────────────────────────────────────────────────────────────────
// Composable per filtrare corsi in base alla sede (estratta dal codice corso)
// Formato codice: [TITOLO][SIGLA_CITTA][ANNO][EDIZIONE]
// Es: DIGAITO202602 → DIGAI + TO + 2026 + 02
// ─────────────────────────────────────────────────────────────────────────────
import { computed, watch } from 'vue'

// Sigle città valide
const SIGLE_CITTA = ['TO', 'CN', 'AT', 'NO', 'BI']

// Mappa sigla → pattern per match nome sede
// Le sedi "Livorno" sono a Torino (via Livorno 49 e 53)
const SIGLA_TO_SEDE = {
  TO: ['torino', 'livorno'],  // "Sede Livorno 49", "Sede Livorno 53" = Torino
  CN: ['cuneo'],
  AT: ['asti'],
  NO: ['novara'],
  BI: ['biella'],
}

/**
 * Estrae la sigla città (2 lettere) dal codice corso.
 * Il codice ha formato: [TITOLO][SIGLA][ANNO:4][EDIZIONE:2]
 * Quindi la sigla è in posizione: length-8 fino a length-6
 * @param {string} codice - Codice corso (es. "DIGAITO202602")
 * @returns {string|null} - Sigla città (es. "TO") o null se non trovata
 */
export function estraiSiglaDaCodice(codice) {
  if (!codice || typeof codice !== 'string') return null
  
  // Rimuovi eventuali suffissi come "rev", "bis", ecc.
  const codiceClean = codice.replace(/(rev|bis|ter)$/i, '')
  
  if (codiceClean.length < 8) return null
  
  // Estrai le 2 lettere prima delle ultime 6 cifre (anno + edizione)
  const sigla = codiceClean.slice(-8, -6).toUpperCase()
  
  return SIGLE_CITTA.includes(sigla) ? sigla : null
}

/**
 * Trova la sigla città corrispondente a una sede.
 * @param {Object} sede - Oggetto sede con proprietà 'citta' (o 'nome')
 * @returns {string|null} - Sigla città o null
 */
export function getSiglaDaSede(sede) {
  if (!sede) return null
  
  // Usa il campo 'citta' se esiste, altrimenti 'nome'
  const cittaRaw = sede.citta || sede.nome || ''
  const cittaLower = cittaRaw.toLowerCase()
  
  for (const [sigla, patterns] of Object.entries(SIGLA_TO_SEDE)) {
    if (patterns.some(p => cittaLower.includes(p))) {
      return sigla
    }
  }
  
  return null
}

/**
 * Composable per filtrare corsi attivi in base alla sede selezionata.
 * @param {Ref<Array>} corsiAttivi - Ref con lista corsi attivi
 * @param {Ref<Array>} sedi - Ref con lista sedi
 * @param {Ref<string|number>} filtroSede - Ref con ID sede selezionata
 * @returns {Object} - { corsiFiltrati, siglaSede, resetCorso }
 */
export function useCorsiPerSede(corsiAttivi, sedi, filtroSede) {
  
  // DEBUG: Log quando cambiano i dati
  watch([filtroSede, sedi], ([newFiltro, newSedi]) => {
    console.log('🔍 [useCorsiPerSede] filtroSede:', newFiltro)
    console.log('🔍 [useCorsiPerSede] sedi disponibili:', newSedi?.map(s => ({ id: s.id, nome: s.nome })))
    if (newFiltro && newSedi?.length) {
      const sede = newSedi.find(s => String(s.id) === String(newFiltro))
      console.log('🔍 [useCorsiPerSede] sede trovata:', sede)
      console.log('🔍 [useCorsiPerSede] sigla estratta:', getSiglaDaSede(sede))
    }
  }, { immediate: true })
  
  // Sigla della sede attualmente selezionata
  const siglaSede = computed(() => {
    if (!filtroSede.value) return null
    
    const sede = sedi.value.find(s => String(s.id) === String(filtroSede.value))
    const sigla = getSiglaDaSede(sede)
    
    // DEBUG
    console.log('🏷️ [siglaSede] sede:', sede?.nome, '→ sigla:', sigla)
    
    return sigla
  })
  
  // Corsi filtrati per sede
  const corsiFiltrati = computed(() => {
    // Se nessuna sede selezionata, ritorna array vuoto
    if (!filtroSede.value || !siglaSede.value) {
      console.log('📋 [corsiFiltrati] Nessuna sede/sigla, ritorno []')
      return []
    }
    
    const risultato = corsiAttivi.value.filter(corso => {
      const siglaCodice = estraiSiglaDaCodice(corso.codice)
      return siglaCodice === siglaSede.value
    })
    
    // DEBUG
    console.log(`📋 [corsiFiltrati] Sigla ${siglaSede.value}: ${risultato.length} corsi trovati`)
    if (risultato.length > 0) {
      console.log('📋 [corsiFiltrati] Primi 3:', risultato.slice(0, 3).map(c => c.codice))
    }
    
    return risultato
  })
  
  // Verifica se un corso appartiene alla sede selezionata
  function corsoAppartieneASede(corsoId) {
    if (!filtroSede.value || !siglaSede.value) return true
    
    const corso = corsiAttivi.value.find(c => c.id === Number(corsoId))
    if (!corso) return false
    
    const siglaCodice = estraiSiglaDaCodice(corso.codice)
    return siglaCodice === siglaSede.value
  }
  
  return {
    corsiFiltrati,
    siglaSede,
    corsoAppartieneASede,
    estraiSiglaDaCodice,
  }
}