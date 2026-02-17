<template>
  <div>
    <h2 class="h4 fw-bold mb-4">👋 Benvenuto, {{ authStore.nomeCompleto }}</h2>

    <!-- Metriche -->
    <div class="row g-3 mb-5">
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Totali"    :valore="stats.totali"    colore="primary"   icon="it-list" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="In Attesa" :valore="stats.inAttesa"  colore="warning"   icon="it-clock" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Confermate" :valore="stats.confermate" colore="success"  icon="it-check-circle" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Conflitti" :valore="stats.conflitti"  colore="danger"   icon="it-warning-circle" />
      </div>
    </div>

    <!-- Prossime prenotazioni confermate -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">
        📅 Prossime Prenotazioni Confermate
      </div>
      <div class="card-body p-0">
        <LoadingSpinner v-if="loading" />

        <div v-else-if="prossime.length === 0" class="p-4 text-muted text-center">
          Nessuna prenotazione confermata prossima.
        </div>

        <ul v-else class="list-group list-group-flush">
          <li
            v-for="p in prossime"
            :key="p.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <div>
              <div class="fw-semibold">Prenotazione #{{ p.id }}</div>
              <small class="text-muted">
                Aula {{ p.aula_id }} —
                {{ p.slots[0] ? formatData(p.slots[0].data) : '—' }}
                {{ p.slots[0] ? formatOra(p.slots[0].ora_inizio) + ' – ' + formatOra(p.slots[0].ora_fine) : '' }}
              </small>
            </div>
            <BadgeStato :stato="p.stato" />
          </li>
        </ul>
      </div>
    </div>

    <!-- Azioni rapide -->
    <div class="row g-3 mt-4">
      <div class="col-auto">
        <router-link :to="{ name: 'NuovaPrenotazione' }" class="btn btn-primary">
          📅 Nuova Prenotazione
        </router-link>
      </div>
      <div class="col-auto">
        <router-link :to="{ name: 'PrenotazioneMassiva' }" class="btn btn-outline-primary">
          🔄 Prenotazione Massiva
        </router-link>
      </div>
      <div class="col-auto">
        <router-link :to="{ name: 'SlotLiberi' }" class="btn btn-outline-secondary">
          🔍 Verifica Disponibilità
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore }     from '@/stores/auth'
import { getPrenotazioni }  from '@/api/prenotazioni'
import { formatData, formatOra } from '@/utils/formatters'
import StatCard      from '@/components/ui/StatCard.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import BadgeStato    from '@/components/ui/BadgeStato.vue'

const authStore = useAuthStore()
const loading   = ref(false)
const prossime  = ref([])

const stats = reactive({ totali: 0, inAttesa: 0, confermate: 0, conflitti: 0 })

onMounted(async () => {
  loading.value = true
  try {
    const tutte = await getPrenotazioni()
    stats.totali    = tutte.length
    stats.inAttesa  = tutte.filter(p => p.stato === 'in_attesa').length
    stats.confermate = tutte.filter(p => p.stato === 'confermata').length
    stats.conflitti = tutte.filter(p => p.stato === 'conflitto').length
    // Mostra solo le 5 più recenti confermate
    prossime.value  = tutte.filter(p => p.stato === 'confermata').slice(0, 5)
  } finally {
    loading.value = false
  }
})
</script>
