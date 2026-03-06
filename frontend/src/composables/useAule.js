// composables/useAule.js
// ─────────────────────────────────────────────────────────────────────────────
// Carica aule e sedi una volta sola (cached) e fornisce funzioni di lookup.
// Usabile in qualsiasi componente: const { nomeAula, nomeSede } = useAule()
// ─────────────────────────────────────────────────────────────────────────────

import { ref, computed } from 'vue'
import { getAule } from '@/api/aule'
import { getSedi } from '@/api/sedi'

// Cache modulo-level (condivisa tra tutti i componenti che usano il composable)
const aule        = ref([])
const sedi        = ref([])
const caricato    = ref(false)
const caricamento = ref(null)   // Promise in corso, evita doppie fetch

export function useAule() {
  async function carica() {
    if (caricato.value) return
    if (caricamento.value) return caricamento.value

    caricamento.value = Promise.all([getAule(), getSedi()])
      .then(([a, s]) => {
        aule.value     = Array.isArray(a) ? a : []
        sedi.value     = Array.isArray(s) ? s : []
        caricato.value = true
      })
      .catch(e => console.warn('useAule:', e.message))
      .finally(() => { caricamento.value = null })

    return caricamento.value
  }

  // Lookup mappe
  const mappaAule = computed(() =>
    Object.fromEntries(aule.value.map(a => [a.id, a]))
  )
  const mappaSedi = computed(() =>
    Object.fromEntries(sedi.value.map(s => [s.id, s]))
  )

  function nomeAula(aulaId) {
    return mappaAule.value[aulaId]?.nome || `Aula ${aulaId}`
  }

  function nomeSede(sedeId) {
    return mappaSedi.value[sedeId]?.nome || `Sede ${sedeId}`
  }

  function sedeDiAula(aulaId) {
    const sedeId = mappaAule.value[aulaId]?.sede_id
    return sedeId ? nomeSede(sedeId) : '—'
  }

  function labelAula(aulaId) {
    const a = mappaAule.value[aulaId]
    if (!a) return `Aula ${aulaId}`
    return `${a.nome} — ${sedeDiAula(aulaId)}`
  }

  return { aule, sedi, carica, nomeAula, nomeSede, sedeDiAula, labelAula }
}