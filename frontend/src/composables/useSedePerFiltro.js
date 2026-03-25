/**
 * Composable per gestire il filtro sede di default basato sull'utente loggato.
 * Se l'utente ha una sede assegnata, la usa come filtro di default.
 * Se sede_id è null/undefined, ritorna '' (nessun filtro).
 */
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function useSedePerFiltro() {
  const authStore = useAuthStore()
  
  /**
   * Ritorna la sede_id dell'utente come stringa (per select/filtri)
   * o stringa vuota se non ha sede assegnata.
   */
  const sedeDefaultFiltro = computed(() => {
    const sedeId = authStore.utente?.sede_id
    return sedeId ? String(sedeId) : ''
  })
  
  /**
   * Ritorna la sede_id dell'utente come numero
   * o null se non ha sede assegnata.
   */
  const sedeIdUtente = computed(() => {
    return authStore.utente?.sede_id || null
  })
  
  /**
   * Verifica se l'utente ha una sede assegnata
   */
  const haSedeAssegnata = computed(() => {
    return !!authStore.utente?.sede_id
  })
  
  return {
    sedeDefaultFiltro,  // Per select/filtri (string)
    sedeIdUtente,       // Per logica/confronti (number|null)
    haSedeAssegnata,    // Boolean check
  }
}