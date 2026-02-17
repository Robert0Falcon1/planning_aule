<template>
  <div>
    <h2 class="h4 fw-bold mb-4">📊 Saturazione Spazi</h2>

    <div class="alert alert-info mb-4">
      Analisi dell'occupazione delle aule nel mese corrente.
      Per report avanzati usa la sezione <strong>Coordinamento → Report Saturazione</strong>.
    </div>

    <!-- Metriche aggregate -->
    <div class="row g-3 mb-5">
      <div class="col-sm-4">
        <StatCard titolo="Slot Occupati"  :valore="stats.slotTotali"   colore="primary" icon="it-calendar" />
      </div>
      <div class="col-sm-4">
        <StatCard titolo="Ore Totali"     :valore="stats.oreTotali"    colore="info"    icon="it-clock" />
      </div>
      <div class="col-sm-4">
        <StatCard titolo="Aule Analizzate" :valore="stats.auleAnalizzate" colore="success" icon="it-list" />
      </div>
    </div>

    <LoadingSpinner v-if="loading" />

    <!-- Tabella per aula -->
    <div v-else class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Dettaglio per aula — mese corrente</div>
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Aula ID</th>
              <th>Slot confermati</th>
              <th>Ore totali</th>
              <th>Saturazione</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="riga in datiAule" :key="riga.aula_id">
              <td class="fw-semibold">{{ riga.aula_id }}</td>
              <td>{{ riga.slot }}</td>
              <td>{{ riga.ore }}h</td>
              <td>
                <div class="progress" style="height: 8px; min-width: 80px;">
                  <div
                    class="progress-bar"
                    :class="riga.percentuale > 70 ? 'bg-danger' : riga.percentuale > 40 ? 'bg-warning' : 'bg-success'"
                    :style="{ width: `${riga.percentuale}%` }"
                  />
                </div>
                <small class="text-muted">{{ riga.percentuale }}%</small>
              </td>
            </tr>
            <tr v-if="datiAule.length === 0">
              <td colspan="4" class="text-center text-muted py-3">Nessun dato disponibile</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getPrenotazioni }   from '@/api/prenotazioni'
import { oggi }              from '@/utils/formatters'
import StatCard              from '@/components/ui/StatCard.vue'
import LoadingSpinner        from '@/components/ui/LoadingSpinner.vue'

const loading = ref(false)
const stats   = reactive({ slotTotali: 0, oreTotali: 0, auleAnalizzate: 0 })
const datiAule = ref([])

onMounted(async () => {
  loading.value = true
  try {
    // Filtra per il mese corrente
    const ora       = new Date()
    const primoMese = `${ora.getFullYear()}-${String(ora.getMonth() + 1).padStart(2, '0')}-01`
    const ultimoMese = new Date(ora.getFullYear(), ora.getMonth() + 1, 0)
      .toISOString().split('T')[0]

    const confermante = await getPrenotazioni({
      stato:    'confermata',
      data_dal: primoMese,
      data_al:  ultimoMese,
    })

    // Aggrega per aula
    const perAula = {}
    for (const p of confermante) {
      if (!perAula[p.aula_id]) perAula[p.aula_id] = { slot: 0, minuti: 0 }
      for (const s of (p.slots ?? [])) {
        perAula[p.aula_id].slot++
        // Calcola durata in minuti
        const [hi, mi] = s.ora_inizio.split(':').map(Number)
        const [hf, mf] = s.ora_fine.split(':').map(Number)
        perAula[p.aula_id].minuti += (hf * 60 + mf) - (hi * 60 + mi)
      }
    }

    const maxSlot = Math.max(...Object.values(perAula).map(a => a.slot), 1)
    datiAule.value = Object.entries(perAula).map(([aula_id, d]) => ({
      aula_id:     Number(aula_id),
      slot:        d.slot,
      ore:         (d.minuti / 60).toFixed(1),
      percentuale: Math.round((d.slot / maxSlot) * 100),
    }))

    stats.auleAnalizzate = datiAule.value.length
    stats.slotTotali     = datiAule.value.reduce((s, a) => s + a.slot, 0)
    stats.oreTotali      = (datiAule.value.reduce((s, a) => s + parseFloat(a.ore), 0)).toFixed(1)
  } finally {
    loading.value = false
  }
})
</script>
