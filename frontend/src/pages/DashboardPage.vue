<template>
  <!--
    Dashboard di smistamento.
    Renderizza la dashboard specifica in base al gruppo funzionale:
      - OPERATIVO    → RC / Segreteria Didattica / Segreteria di Sede
      - SUPERVISIONE → Responsabile Sede
      - COORDINAMENTO → Coordinamento (admin)
  -->
  <component :is="dashboardComponent" v-if="dashboardComponent" />

  <div v-else class="alert alert-warning">
    Dashboard non disponibile per il ruolo: <strong>{{ authStore.ruolo }}</strong>
  </div>
</template>

<script setup>
import { computed, defineAsyncComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { RUOLI }        from '@/utils/constants'

const authStore = useAuthStore()

// ── Gruppi funzionali (specchio di backend/core/permissions.py) ──────────────
const OPERATIVO = [
  RUOLI.RESPONSABILE_CORSO,
  RUOLI.SEGRETERIA_DIDATTICA,
  RUOLI.SEGRETERIA_SEDE,
]

/**
 * Seleziona la dashboard in base al gruppo funzionale del ruolo.
 * Lazy-loaded per non caricare tutti i bundle in anticipo.
 */
const dashboardComponent = computed(() => {
  if (OPERATIVO.includes(authStore.ruolo)) {
    return defineAsyncComponent(() => import('./operativo/DashboardOperativoPage.vue'))
  }
  if (authStore.ruolo === RUOLI.COORDINAMENTO) {
    return defineAsyncComponent(() => import('./coordinamento/DashboardCoordinamentoPage.vue'))
  }
  if (authStore.ruolo === RUOLI.RESPONSABILE_SEDE) {
    return defineAsyncComponent(() => import('./supervisione/DashboardSupervisionePage.vue'))
  }
  return null
})
</script>