<template>
  <div>
    <h2 class="h4 fw-bold mb-4">🌐 Dashboard — Coordinamento</h2>

    <!-- Metriche aggregate multi-sede -->
    <div class="row g-3 mb-5">
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Prenotazioni"  :valore="stats.totali"     colore="primary" icon="it-list" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Confermate"    :valore="stats.confermate" colore="success" icon="it-check-circle" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="In Attesa"     :valore="stats.inAttesa"   colore="warning" icon="it-clock" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Conflitti"     :valore="stats.conflitti"  colore="danger"  icon="it-warning-circle" />
      </div>
    </div>

    <LoadingSpinner v-if="loading" />

    <div v-else class="row g-4">
      <!-- Tabella per sede -->
      <div class="col-lg-7">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white fw-semibold">Prenotazioni per sede</div>
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr><th>Sede</th><th>Totali</th><th>Confermate</th><th>In Attesa</th></tr>
              </thead>
              <tbody>
                <tr v-for="(d, nome) in perSede" :key="nome">
                  <td class="fw-semibold">{{ nome }}</td>
                  <td>{{ d.totali }}</td>
                  <td><span class="text-success">{{ d.confermate }}</span></td>
                  <td><span class="text-warning">{{ d.inAttesa }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Distribuzione stati -->
      <div class="col-lg-5">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white fw-semibold">Distribuzione stati</div>
          <div class="card-body">
            <div v-for="(cfg, stato) in STATI_BADGE" :key="stato" class="mb-3">
              <div class="d-flex justify-content-between small mb-1">
                <span>{{ cfg.icon }} {{ cfg.label }}</span>
                <span class="fw-semibold">{{ statCounts[stato] ?? 0 }}</span>
              </div>
              <div class="progress" style="height: 6px;">
                <div
                  class="progress-bar"
                  :class="cfg.class"
                  :style="{ width: stats.totali ? `${((statCounts[stato] ?? 0) / stats.totali * 100).toFixed(0)}%` : '0%' }"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Azioni rapide -->
    <div class="d-flex flex-wrap gap-2 mt-4">
      <router-link :to="{ name: 'VistaGlobale' }"  class="btn btn-primary">🌐 Vista Globale</router-link>
      <router-link :to="{ name: 'Report' }"         class="btn btn-outline-primary">📊 Report Saturazione</router-link>
      <router-link :to="{ name: 'GestioneUtenti' }" class="btn btn-outline-secondary">👥 Gestione Utenti</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getPrenotazioni }   from '@/api/prenotazioni'
import { getSedi }           from '@/api/sedi'
import { STATI_BADGE }       from '@/utils/constants'
import StatCard              from '@/components/ui/StatCard.vue'
import LoadingSpinner        from '@/components/ui/LoadingSpinner.vue'

const loading      = ref(false)
const prenotazioni = ref([])
const sedi         = ref([])
const stats        = reactive({ totali: 0, confermate: 0, inAttesa: 0, conflitti: 0 })

// Conteggio per stato
const statCounts = computed(() => {
  const counts = {}
  prenotazioni.value.forEach(p => { counts[p.stato] = (counts[p.stato] ?? 0) + 1 })
  return counts
})

// TODO: da affinare quando il backend esporrà sede_id nella risposta prenotazione
const perSede = computed(() => ({}))

onMounted(async () => {
  loading.value = true
  try {
    [prenotazioni.value, sedi.value] = await Promise.all([getPrenotazioni(), getSedi()])
    stats.totali    = prenotazioni.value.length
    stats.confermate = prenotazioni.value.filter(p => p.stato === 'confermata').length
    stats.inAttesa  = prenotazioni.value.filter(p => p.stato === 'in_attesa').length
    stats.conflitti = prenotazioni.value.filter(p => p.stato === 'conflitto').length
  } finally {
    loading.value = false
  }
})
</script>
