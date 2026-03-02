<template>
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

const dashboardComponent = computed(() => {
  const map = {
    [RUOLI.RESPONSABILE_CORSO]:   defineAsyncComponent(() => import('./_archivio/DashboardResponsabilePage.vue')),
    [RUOLI.SEGRETERIA_SEDE]:      defineAsyncComponent(() => import('./_archivio/DashboardSegreteriaSedePage.vue')),
    [RUOLI.RESPONSABILE_SEDE]:    defineAsyncComponent(() => import('./_archivio/DashboardResponsabileSedePage.vue')),
    [RUOLI.SEGRETERIA_DIDATTICA]: defineAsyncComponent(() => import('./_archivio/DashboardSegreteriaDidatticaPage.vue')),
    [RUOLI.COORDINAMENTO]:        defineAsyncComponent(() => import('./_archivio/DashboardCoordinamentoPage.vue')),
  }
  return map[authStore.ruolo] ?? null
})
</script>