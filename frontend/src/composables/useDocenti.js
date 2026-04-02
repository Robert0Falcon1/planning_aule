/**
 * Composable per la gestione dei docenti
 */
import { ref, computed } from 'vue'
import { getDocenti } from '@/api/docenti'

const docenti = ref([])
const caricandoDocenti = ref(false)
const erroreDocenti = ref(null)

export function useDocenti() {
  /**
   * Carica tutti i docenti dal backend
   * @param {Object} filtri - Filtri opzionali
   */
  async function caricaDocenti(filtri = {}) {
    caricandoDocenti.value = true
    erroreDocenti.value = null
    
    try {
      docenti.value = await getDocenti(filtri)
    } catch (e) {
      erroreDocenti.value = e.message
      console.error('Errore caricamento docenti:', e)
    } finally {
      caricandoDocenti.value = false
    }
  }
  
  /**
   * Trova un docente per ID
   * @param {number} id - ID del docente
   * @returns {Object|undefined} Docente trovato
   */
  function getDocenteById(id) {
    return docenti.value.find(d => d.id === Number(id))
  }
  
  /**
   * Formatta il nome completo del docente
   * @param {number} id - ID del docente
   * @returns {string} Nome formattato "Cognome Nome"
   */
  function getNomeDocente(id) {
    const docente = getDocenteById(id)
    return docente ? `${docente.cognome} ${docente.nome}` : '—'
  }
  
  /**
   * Docenti ordinati per cognome
   */
  const docentiOrdinati = computed(() => 
    [...docenti.value].sort((a, b) => 
      a.cognome.localeCompare(b.cognome) || a.nome.localeCompare(b.nome)
    )
  )
  
  return {
    docenti,
    docentiOrdinati,
    caricandoDocenti,
    erroreDocenti,
    caricaDocenti,
    getDocenteById,
    getNomeDocente,
  }
}