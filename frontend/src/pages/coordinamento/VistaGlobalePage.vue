<template>
  <div>
    <h2 class="h4 fw-bold mb-4">🌐 Vista Globale Prenotazioni</h2>

    <!-- Filtri avanzati -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-sm-3">
            <label class="form-label small fw-semibold">Sede</label>
            <select v-model.number="filtri.sede_id" class="form-select form-select-sm">
              <option :value="null">Tutte le sedi</option>
              <option v-for="s in sedi" :key="s.id" :value="s.id">
                {{ s.nome }} ({{ s.citta }})
              </option>
            </select>
          </div>
          <div class="col-sm-2">
            <label class="form-label small fw-semibold">Stato</label>
            <select v-model="filtri.stato" class="form-select form-select-sm">
              <option value="">Tutti</option>
              <option v-for="(cfg, val) in STATI_BADGE" :key="val" :value="val">
                {{ cfg.icon }} {{ cfg.label }}
              </option>
            </select>
          </div>
          <div class="col-sm-2">
            <label class="form-label small fw-semibold">Dal</label>
            <input v-model="filtri.data_dal" type="date" class="form-control form-control-sm" />
          </div>
          <div class="col-sm-2">
            <label class="form-label small fw-semibold">Al</label>
            <input v-model="filtri.data_al" type="date" class="form-control form-control-sm" />
          </div>
          <div class="col-sm-3">
            <button class="btn btn-primary btn-sm w-100" @click="carica">
              🔍 Filtra
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Risultati -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white d-flex justify-content-between align-items-center">
        <span class="fw-semibold">{{ prenotazioni.length }} risultati</span>
        <button class="btn btn-sm btn-outline-secondary" @click="esportaCsv">
          📥 Esporta CSV
        </button>
      </div>

      <LoadingSpinner v-if="loading" />

      <div v-else class="table-responsive">
        <table class="table table-hover table-sm mb-0">
          <thead class="table-light">
            <tr>
              <th>ID</th><th>Tipo</th><th>Aula</th><th>Corso</th>
              <th>Richiedente</th><th>Stato</th><th>Slot</th><th>Dal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="prenotazioni.length === 0">
              <td colspan="8" class="text-center text-muted py-4">Nessun risultato</td>
            </tr>
            <tr v-for="p in prenotazioni" :key="p.id">
              <td>#{{ p.id }}</td>
              <td>{{ p.tipo }}</td>
              <td>{{ p.aula_id }}</td>
              <td>{{ p.corso_id }}</td>
              <td>{{ p.richiedente_id }}</td>
              <td><BadgeStato :stato="p.stato" /></td>
              <td>{{ p.slots?.length ?? 0 }}</td>
              <td class="text-muted small">
                {{ p.slots?.[0] ? formatData(p.slots[0].data) : '—' }}
              </td>
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
import { getSedi }           from '@/api/sedi'
import { formatData }        from '@/utils/formatters'
import { STATI_BADGE }       from '@/utils/constants'
import LoadingSpinner        from '@/components/ui/LoadingSpinner.vue'
import BadgeStato            from '@/components/ui/BadgeStato.vue'

const loading      = ref(false)
const prenotazioni = ref([])
const sedi         = ref([])
const filtri       = reactive({ sede_id: null, stato: '', data_dal: '', data_al: '' })

onMounted(async () => {
  sedi.value = await getSedi()
  await carica()
})

async function carica() {
  loading.value = true
  try {
    prenotazioni.value = await getPrenotazioni({
      sede_id:  filtri.sede_id  || undefined,
      stato:    filtri.stato    || undefined,
      data_dal: filtri.data_dal || undefined,
      data_al:  filtri.data_al  || undefined,
    })
  } finally {
    loading.value = false
  }
}

/** Esporta i dati in CSV scaricabile */
function esportaCsv() {
  const righe = [
    ['ID', 'Tipo', 'Aula', 'Corso', 'Richiedente', 'Stato', 'Slot', 'Data primo slot'],
    ...prenotazioni.value.map(p => [
      p.id, p.tipo, p.aula_id, p.corso_id, p.richiedente_id, p.stato,
      p.slots?.length ?? 0,
      p.slots?.[0]?.data ?? '',
    ]),
  ]
  const csv  = righe.map(r => r.join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href = url; a.download = 'prenotazioni_export.csv'; a.click()
  URL.revokeObjectURL(url)
}
</script>
