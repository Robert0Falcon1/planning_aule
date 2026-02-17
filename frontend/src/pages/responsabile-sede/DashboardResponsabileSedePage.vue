<template>
  <div>
    <h2 class="h4 fw-bold mb-4">👋 Dashboard — Responsabile di Sede</h2>

    <div class="row g-3 mb-5">
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Totali"       :valore="stats.totali"     colore="primary" icon="it-list" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Oggi"         :valore="stats.oggi"       colore="info"    icon="it-calendar" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="In Attesa"    :valore="stats.inAttesa"   colore="warning" icon="it-clock" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Conflitti"    :valore="stats.conflitti"  colore="danger"  icon="it-warning-circle" />
      </div>
    </div>

    <!-- Azioni rapide -->
    <div class="d-flex flex-wrap gap-2 mb-5">
      <router-link :to="{ name: 'PrenotazioniSede' }" class="btn btn-primary">
        📋 Prenotazioni Sede
      </router-link>
      <router-link :to="{ name: 'SaturazioneSpazi' }" class="btn btn-outline-primary">
        📊 Saturazione Spazi
      </router-link>
    </div>

    <!-- Tabella prenotazioni recenti -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Prenotazioni recenti della sede</div>
      <LoadingSpinner v-if="loading" />
      <div v-else class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>#</th><th>Tipo</th><th>Aula</th><th>Corso</th><th>Stato</th><th>Slot</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in prenotazioni.slice(0, 10)" :key="p.id">
              <td>{{ p.id }}</td>
              <td>{{ p.tipo }}</td>
              <td>{{ p.aula_id }}</td>
              <td>{{ p.corso_id }}</td>
              <td><BadgeStato :stato="p.stato" /></td>
              <td>{{ p.slots?.length ?? 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getPrenotazioni }   from '@/api/prenotazioni'
import { oggi }              from '@/utils/formatters'
import StatCard              from '@/components/ui/StatCard.vue'
import LoadingSpinner        from '@/components/ui/LoadingSpinner.vue'
import BadgeStato            from '@/components/ui/BadgeStato.vue'

const loading      = ref(false)
const prenotazioni = ref([])
const stats        = reactive({ totali: 0, oggi: 0, inAttesa: 0, conflitti: 0 })
const dataOggi     = oggi()

onMounted(async () => {
  loading.value = true
  try {
    prenotazioni.value = await getPrenotazioni()
    stats.totali    = prenotazioni.value.length
    stats.inAttesa  = prenotazioni.value.filter(p => p.stato === 'in_attesa').length
    stats.conflitti = prenotazioni.value.filter(p => p.stato === 'conflitto').length
    // Prenotazioni con almeno uno slot oggi
    stats.oggi = prenotazioni.value.filter(p =>
      p.stato === 'confermata' &&
      p.slots?.some(s => s.data === dataOggi),
    ).length
  } finally {
    loading.value = false
  }
})
</script>
