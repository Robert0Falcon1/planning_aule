<template>
  <div>
    <h2 class="h4 fw-bold mb-4">📊 Report Saturazione Spazi</h2>

    <!-- Periodo personalizzabile -->
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
            <button class="btn btn-primary btn-sm w-100" :disabled="loading" @click="genera">
              {{ loading ? 'Calcolo…' : '📊 Genera Report' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Metriche aggregate -->
    <div v-if="generato" class="row g-3 mb-4">
      <div class="col-sm-4">
        <StatCard titolo="Aule Analizzate"  :valore="stats.auleAnalizzate"  colore="primary" icon="it-list" />
      </div>
      <div class="col-sm-4">
        <StatCard titolo="Slot Totali"      :valore="stats.slotTotali"      colore="info"    icon="it-calendar" />
      </div>
      <div class="col-sm-4">
        <StatCard titolo="Ore Totali"       :valore="`${stats.oreTotali}h`" colore="success" icon="it-clock" />
      </div>
    </div>

    <!-- Tabella dettaglio -->
    <div v-if="generato" class="card border-0 shadow-sm">
      <div class="card-header bg-white d-flex justify-content-between align-items-center">
        <span class="fw-semibold">Dettaglio per aula</span>
        <button class="btn btn-sm btn-outline-secondary" @click="esportaCsv">
          📥 Scarica CSV
        </button>
      </div>
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Aula ID</th><th>Slot</th><th>Ore</th><th>Occupazione</th></tr>
          </thead>
          <tbody>
            <tr v-for="r in righe" :key="r.aula_id">
              <td class="fw-semibold">{{ r.aula_id }}</td>
              <td>{{ r.slot }}</td>
              <td>{{ r.ore }}h</td>
              <td style="min-width: 150px;">
                <div class="d-flex align-items-center gap-2">
                  <div class="progress flex-grow-1" style="height: 8px;">
                    <div
                      class="progress-bar"
                      :class="r.percentuale > 70 ? 'bg-danger' : r.percentuale > 40 ? 'bg-warning' : 'bg-success'"
                      :style="{ width: `${r.percentuale}%` }"
                    />
                  </div>
                  <small class="text-muted" style="min-width: 35px;">{{ r.percentuale }}%</small>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { getPrenotazioni }   from '@/api/prenotazioni'
import { oggi }              from '@/utils/formatters'
import StatCard              from '@/components/ui/StatCard.vue'

const loading  = ref(false)
const generato = ref(false)
const righe    = ref([])
const stats    = reactive({ auleAnalizzate: 0, slotTotali: 0, oreTotali: 0 })

// Default: mese corrente
const ora = new Date()
const filtri = reactive({
  dal: `${ora.getFullYear()}-${String(ora.getMonth() + 1).padStart(2, '0')}-01`,
  al:  new Date(ora.getFullYear(), ora.getMonth() + 1, 0).toISOString().split('T')[0],
})

async function genera() {
  loading.value = true
  try {
    const dati = await getPrenotazioni({
      stato:    'confermata',
      data_dal: filtri.dal,
      data_al:  filtri.al,
    })

    // Aggrega per aula
    const perAula = {}
    for (const p of dati) {
      if (!perAula[p.aula_id]) perAula[p.aula_id] = { slot: 0, minuti: 0 }
      for (const s of (p.slots ?? [])) {
        perAula[p.aula_id].slot++
        const [hi, mi] = s.ora_inizio.split(':').map(Number)
        const [hf, mf] = s.ora_fine.split(':').map(Number)
        perAula[p.aula_id].minuti += (hf * 60 + mf) - (hi * 60 + mi)
      }
    }

    const maxSlot = Math.max(...Object.values(perAula).map(a => a.slot), 1)
    righe.value = Object.entries(perAula)
      .map(([aula_id, d]) => ({
        aula_id: Number(aula_id),
        slot:    d.slot,
        ore:     (d.minuti / 60).toFixed(1),
        percentuale: Math.round((d.slot / maxSlot) * 100),
      }))
      .sort((a, b) => b.slot - a.slot)

    stats.auleAnalizzate = righe.value.length
    stats.slotTotali     = righe.value.reduce((s, r) => s + r.slot, 0)
    stats.oreTotali      = righe.value.reduce((s, r) => s + parseFloat(r.ore), 0).toFixed(1)

    generato.value = true
  } finally {
    loading.value = false
  }
}

function esportaCsv() {
  const intestazione = 'Aula ID,Slot,Ore,% Occupazione'
  const corpo = righe.value.map(r => `${r.aula_id},${r.slot},${r.ore},${r.percentuale}%`).join('\n')
  const blob  = new Blob([`${intestazione}\n${corpo}`], { type: 'text/csv;charset=utf-8;' })
  const url   = URL.createObjectURL(blob)
  const a     = document.createElement('a')
  a.href = url
  a.download = `report_saturazione_${filtri.dal}_${filtri.al}.csv`
  a.click()
  URL.revokeObjectURL(url)
}
</script>
