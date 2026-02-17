<template>
  <!--
    Dashboard di smistamento.
    Renderizza la dashboard specifica in base al ruolo dell'utente autenticato.
    Se il ruolo non è riconosciuto, mostra un messaggio di errore.
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

/**
 * Mappa ruolo → componente dashboard.
 * Lazy-loaded per non caricare tutti i bundle in anticipo.
 */
const dashboardComponent = computed(() => {
  const map = {
    [RUOLI.RESPONSABILE_CORSO]:   defineAsyncComponent(() => import('./responsabile-corso/DashboardResponsabilePage.vue')),
    [RUOLI.SEGRETERIA_SEDE]:      defineAsyncComponent(() => import('./segreteria-sede/DashboardSegreteriaSedePage.vue')),
    [RUOLI.RESPONSABILE_SEDE]:    defineAsyncComponent(() => import('./responsabile-sede/DashboardResponsabileSedePage.vue')),
    [RUOLI.SEGRETERIA_DIDATTICA]: defineAsyncComponent(() => import('./segreteria-didattica/DashboardSegreteriaDidatticaPage.vue')),
    [RUOLI.COORDINAMENTO]:        defineAsyncComponent(() => import('./coordinamento/DashboardCoordinamentoPage.vue')),
  }
  return map[authStore.ruolo] ?? null
})
</script>
