<template>
  <div>
    <h2 class="h4 fw-bold mb-4">📅 Calendario Sede</h2>

    <!-- Filtri periodo -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-sm-4">
            <label class="form-label small fw-semibold">Dal</label>
            <input v-model="filtri.dal" type="date" class="form-control form-control-sm" />
          </div>
          <div class="col-sm-4">
            <label class="form-label small fw-semibold">Al</label>
            <input v-model="filtri.al" type="date" class="form-control form-control-sm" />
          </div>
          <div class="col-sm-4">
            <button class="btn btn-primary btn-sm w-100" @click="carica">
              🔍 Visualizza
            </button>
          </div>
        </div>
      </div>
    </div>

    <LoadingSpinner v-if="loading" />

    <!-- Vista raggruppata per giorno -->
    <div v-else>
      <div v-if="Object.keys(perGiorno).length === 0" class="alert alert-info">
        Nessuna prenotazione nel periodo selezionato.
      </div>

      <div v-for="(slots, data) in perGiorno" :key="data" class="mb-4">
        <!-- Intestazione giorno -->
        <div class="d-flex align-items-center gap-2 mb-2">
          <div class="badge bg-primary rounded-pill px-3 py-2">{{ formatData(data) }}</div>
          <small class="text-muted">{{ slots.length }} prenotazion{{ slots.length === 1 ? 'e' : 'i' }}</small>
        </div>

        <div class="row g-2">
          <div v-for="p in slots" :key="p.id" class="col-md-6 col-lg-4">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body py-2 px-3">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <div class="small fw-semibold">Aula {{ p.aula_id }}</div>
                    <div class="text-muted x-small">Corso {{ p.corso_id }}</div>
                    <div class="small">
                      {{ formatOra(p.ora_inizio) }} – {{ formatOra(p.ora_fine) }}
                    </div>
                  </div>
                  <BadgeStato :stato="p.stato" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getPrenotazioni }   from '@/api/prenotazioni'
import { formatData, formatOra, oggi } from '@/utils/formatters'
import LoadingSpinner        from '@/components/ui/LoadingSpinner.vue'
import BadgeStato            from '@/components/ui/BadgeStato.vue'

const loading = ref(false)
const rawData = ref([])   // Lista piatta di { aula_id, corso_id, stato, data, ora_inizio, ora_fine }

// Periodo di default: settimana corrente
const filtri = reactive({
  dal: oggi(),
  al:  new Date(Date.now() + 7 * 86400000).toISOString().split('T')[0],
})

/**
 * Espande ogni prenotazione nei suoi slot e raggruppa per data.
 * Struttura: { 'YYYY-MM-DD': [ { ...prenotazione, ora_inizio, ora_fine } ] }
 */
const perGiorno = computed(() => {
  const map = {}
  for (const p of rawData.value) {
    for (const slot of (p.slots ?? [])) {
      if (!map[slot.data]) map[slot.data] = []
      map[slot.data].push({ ...p, ora_inizio: slot.ora_inizio, ora_fine: slot.ora_fine })
    }
  }
  // Ordina per data
  return Object.fromEntries(Object.entries(map).sort(([a], [b]) => a.localeCompare(b)))
})

onMounted(carica)

async function carica() {
  loading.value = true
  try {
    rawData.value = await getPrenotazioni({
      data_dal: filtri.dal,
      data_al:  filtri.al,
    })
  } finally {
    loading.value = false
  }
}
</script>
