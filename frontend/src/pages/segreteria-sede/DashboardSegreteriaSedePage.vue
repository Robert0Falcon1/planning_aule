<template>
  <div>
    <h2 class="h4 fw-bold mb-4">👋 Dashboard — Segreteria di Sede</h2>

    <div class="row g-3 mb-5">
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Da Validare"  :valore="stats.inAttesa"   colore="warning" icon="it-clock" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Conflitti"    :valore="stats.conflitti"  colore="danger"  icon="it-warning-circle" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Confermate"   :valore="stats.confermate" colore="success" icon="it-check-circle" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Totali"       :valore="stats.totali"     colore="primary" icon="it-list" />
      </div>
    </div>

    <!-- Prime 3 richieste pendenti con accesso rapido -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-header bg-white d-flex justify-content-between align-items-center">
        <span class="fw-semibold">📬 Ultime Richieste Pendenti</span>
        <router-link :to="{ name: 'RichiestePendenti' }" class="btn btn-sm btn-outline-primary">
          Vedi tutte →
        </router-link>
      </div>
      <LoadingSpinner v-if="loading" />
      <ul v-else class="list-group list-group-flush">
        <li
          v-for="p in primaRichieste"
          :key="p.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          <div>
            <BadgeStato :stato="p.stato" />
            <span class="ms-2 fw-semibold">Prenotazione #{{ p.id }}</span>
            <small class="text-muted ms-2">Aula {{ p.aula_id }}</small>
          </div>
          <router-link :to="{ name: 'RichiestePendenti' }" class="btn btn-sm btn-outline-secondary">
            Gestisci →
          </router-link>
        </li>
        <li v-if="primaRichieste.length === 0" class="list-group-item text-muted text-center py-3">
          Nessuna richiesta pendente ✅
        </li>
      </ul>
    </div>

    <!-- Azioni rapide -->
    <div class="d-flex flex-wrap gap-2">
      <router-link :to="{ name: 'RichiestePendenti' }" class="btn btn-primary">
        📬 Gestisci Richieste
      </router-link>
      <router-link :to="{ name: 'GestioneConflitti' }" class="btn btn-outline-danger">
        ⚠️ Conflitti
      </router-link>
      <router-link :to="{ name: 'CalendarioSede' }" class="btn btn-outline-secondary">
        📅 Calendario Sede
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getPrenotazioni }   from '@/api/prenotazioni'
import StatCard              from '@/components/ui/StatCard.vue'
import LoadingSpinner        from '@/components/ui/LoadingSpinner.vue'
import BadgeStato            from '@/components/ui/BadgeStato.vue'

const loading      = ref(false)
const prenotazioni = ref([])
const stats        = reactive({ inAttesa: 0, conflitti: 0, confermate: 0, totali: 0 })

const primaRichieste = computed(() =>
  prenotazioni.value
    .filter(p => p.stato === 'in_attesa' || p.stato === 'conflitto')
    .slice(0, 3),
)

onMounted(async () => {
  loading.value = true
  try {
    prenotazioni.value = await getPrenotazioni()
    stats.totali    = prenotazioni.value.length
    stats.inAttesa  = prenotazioni.value.filter(p => p.stato === 'in_attesa').length
    stats.conflitti = prenotazioni.value.filter(p => p.stato === 'conflitto').length
    stats.confermate = prenotazioni.value.filter(p => p.stato === 'confermata').length
  } finally {
    loading.value = false
  }
})
</script>
