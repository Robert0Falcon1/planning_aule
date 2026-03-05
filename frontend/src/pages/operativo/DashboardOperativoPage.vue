<template>
  <div class="page-operativo">
    <div class="page-header mb-4">
      <h2 class="page-title">Ciao, {{ auth.nomeUtente }} 👋</h2>
      <p class="text-muted mb-0">{{ oggiLabel }} — qui trovi un riepilogo rapido della tua attività.</p>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3">
        <StatCard value="—" label="Prenotazioni attive" icon="it-calendar" color="primary" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard value="—" label="Prenotazioni oggi" icon="it-check-circle" color="success" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard value="—" label="Conflitti aperti" icon="it-error" color="danger" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard value="—" label="Aule disponibili ora" icon="it-map-marker" color="info" />
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h5 class="card-title mb-3">Azioni rapide</h5>
            <div class="d-flex flex-wrap gap-2">
              <RouterLink :to="{ name: 'NuovaPrenotazione' }" class="btn btn-primary">
                <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
                Nuova prenotazione
              </RouterLink>
              <RouterLink :to="{ name: 'NuovaPrenotazione', query: { tipo: 'massiva' } }" class="btn btn-outline-primary">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-files'"></use></svg>
                Prenotazione massiva
              </RouterLink>
              <RouterLink :to="{ name: 'Calendario' }" class="btn btn-outline-secondary">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-calendar'"></use></svg>
                Vai al calendario
              </RouterLink>
              <RouterLink :to="{ name: 'Conflitti' }" class="btn btn-outline-danger">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-error'"></use></svg>
                Controlla conflitti
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-12 col-xl-8">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 pb-0 d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Ultime prenotazioni</h5>
            <RouterLink :to="{ name: 'MiePrenotazioni' }" class="btn btn-sm btn-outline-primary">Vedi tutte</RouterLink>
          </div>
          <div class="card-body pt-2">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
            <div v-else-if="!prenotazioni.length" class="text-muted text-center py-4">
              Nessuna prenotazione trovata.
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover table-sm align-middle">
                <thead class="table-light">
                  <tr><th>Corso</th><th>Aula</th><th>Data</th><th>Orario</th><th>Stato</th></tr>
                </thead>
                <tbody>
                  <tr v-for="p in prenotazioni" :key="p.id">
                    <td class="fw-semibold">{{ p.titolo_corso || p.corso?.titolo || '—' }}</td>
                    <td>{{ p.aula?.nome }}<small class="text-muted d-block">{{ p.aula?.sede?.nome }}</small></td>
                    <td>{{ formatData(p.data) }}</td>
                    <td>{{ p.ora_inizio }} – {{ p.ora_fine }}</td>
                    <td>
                      <span class="badge" :class="p.stato === 'confermata' || p.stato === 'CONFERMATA' ? 'bg-success' : 'bg-secondary'">
                        {{ p.stato }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-xl-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 pb-0">
            <h5 class="card-title mb-0">Prossimi appuntamenti</h5>
          </div>
          <div class="card-body pt-2">
            <p class="text-muted small">Visualizza il calendario completo per i dettagli.</p>
            <RouterLink :to="{ name: 'Calendario' }" class="btn btn-outline-primary btn-sm">
              <svg class="icon icon-sm me-1"><use :href="sprites + '#it-calendar'"></use></svg>
              Apri Calendario
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import StatCard from '@/components/ui/StatCard.vue'
import { getMiePrenotazioni } from '@/api/prenotazioni'
import { formatData } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const auth        = useAuthStore()
const loading     = ref(false)
const prenotazioni = ref([])

const oggiLabel = new Date().toLocaleDateString('it-IT', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
})

onMounted(async () => {
  loading.value = true
  try {
    const data = await getMiePrenotazioni()
    prenotazioni.value = (data?.items || data || []).slice(0, 5)
  } catch (e) {
    console.warn('Dashboard: impossibile caricare prenotazioni', e.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; }
</style>