<template>
  <div>
    <h2 class="h4 fw-bold mb-4">📊 Saturazione Spazi</h2>

    <!-- Filtro periodo -->
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
              📊 Aggiorna
            </button>
          </div>
        </div>
        <div class="mt-2">
          <span class="small text-muted me-3">Scorciatoie:</span>
          <button class="btn btn-outline-secondary btn-sm me-2" @click="setMese(0)">Mese corrente</button>
          <button class="btn btn-outline-secondary btn-sm me-2" @click="setMesi(3)">Prossimi 3 mesi</button>
          <button class="btn btn-outline-secondary btn-sm me-2" @click="setMesi(6)">Prossimi 6 mesi</button>
          <button class="btn btn-outline-secondary btn-sm" @click="setAnno">Anno corrente</button>
        </div>
      </div>
    </div>

    <LoadingSpinner v-if="loading" />

    <div v-else-if="stats">
      <!-- KPI -->
      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <StatCard titolo="Slot Occupati" :valore="stats.totaleSlot" colore="primary" icona="🗓️" />
        </div>
        <div class="col-md-4">
          <StatCard titolo="Ore Totali" :valore="stats.oreText" colore="success" icona="⏱️" />
        </div>
        <div class="col-md-4">
          <StatCard titolo="Aule Analizzate" :valore="stats.aule.length" colore="info" icona="🏫" />
        </div>
      </div>

      <!-- Tabella per aula -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white fw-semibold">
          Dettaglio per aula — {{ labelPeriodo }}
        </div>
        <div class="card-body p-0">
          <div v-if="stats.aule.length === 0" class="p-4 text-center text-muted">
            Nessuno slot confermato nel periodo selezionato.
          </div>
          <table v-else class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Aula ID</th>
                <th class="text-center">Slot confermati</th>
                <th class="text-center">Ore totali</th>
                <th>Saturazione</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="aula in stats.aule" :key="aula.aulaId">
                <td class="fw-semibold">{{ aula.aulaId }}</td>
                <td class="text-center">{{ aula.slot }}</td>
                <td class="text-center">{{ aula.ore.toFixed(1) }}h</td>
                <td style="min-width: 180px;">
                  <div class="d-flex align-items-center gap-2">
                    <div class="progress flex-grow-1" style="height: 8px;">
                      <div
                        class="progress-bar"
                        :class="coloreSaturazione(aula.saturazione)"
                        :style="{ width: `${Math.min(aula.saturazione, 100)}%` }"
                        role="progressbar"
                      />
                    </div>
                    <span class="small text-muted" style="min-width: 38px;">
                      {{ aula.saturazione }}%
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getPrenotazioni } from '@/api/prenotazioni'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import StatCard       from '@/components/ui/StatCard.vue'

const loading = ref(false)
const stats   = ref(null)

// ── Helpers data ──────────────────────────────────────────────────────────────
function isoDate(d) {
  return d.toISOString().split('T')[0]
}
function primoDelMese(offset = 0) {
  const d = new Date()
  d.setDate(1)
  d.setMonth(d.getMonth() + offset)
  return isoDate(d)
}
function ultimoDelMese(offset = 0) {
  const d = new Date()
  d.setMonth(d.getMonth() + offset + 1)
  d.setDate(0)
  return isoDate(d)
}

// Default: dall'inizio del mese corrente ai prossimi 3 mesi
const filtri = reactive({
  dal: primoDelMese(0),
  al:  ultimoDelMese(3),
})

// Scorciatoie periodo
function setMese()       { filtri.dal = primoDelMese(0); filtri.al = ultimoDelMese(0);  carica() }
function setMesi(n)      { filtri.dal = primoDelMese(0); filtri.al = ultimoDelMese(n-1); carica() }
function setAnno()       {
  const y = new Date().getFullYear()
  filtri.dal = `${y}-01-01`
  filtri.al  = `${y}-12-31`
  carica()
}

const labelPeriodo = computed(() => `${filtri.dal} → ${filtri.al}`)

// ── Calcolo saturazione ───────────────────────────────────────────────────────
const ORE_DISPONIBILI_MESE = 160  // base di riferimento per %

async function carica() {
  loading.value = true
  stats.value   = null
  try {
    const prenotazioni = await getPrenotazioni({
      stato:    'confermata',
      data_dal: filtri.dal,
      data_al:  filtri.al,
    })

    // Aggrega per aula
    const perAula = {}
    let totaleSlot = 0
    let totaleOre  = 0

    for (const p of prenotazioni) {
      for (const s of (p.slots ?? [])) {
        const [hI, mI] = s.ora_inizio.split(':').map(Number)
        const [hF, mF] = s.ora_fine.split(':').map(Number)
        const ore = (hF * 60 + mF - hI * 60 - mI) / 60

        if (!perAula[p.aula_id]) perAula[p.aula_id] = { slot: 0, ore: 0 }
        perAula[p.aula_id].slot++
        perAula[p.aula_id].ore += ore
        totaleSlot++
        totaleOre += ore
      }
    }

    // Calcola mesi nel periodo per normalizzare la saturazione
    const dalDate = new Date(filtri.dal)
    const alDate  = new Date(filtri.al)
    const mesiPeriodo = Math.max(1,
      (alDate.getFullYear() - dalDate.getFullYear()) * 12 +
      (alDate.getMonth() - dalDate.getMonth()) + 1
    )
    const baseOre = ORE_DISPONIBILI_MESE * mesiPeriodo

    const auleStats = Object.entries(perAula).map(([id, v]) => ({
      aulaId:      Number(id),
      slot:        v.slot,
      ore:         v.ore,
      saturazione: Math.round((v.ore / baseOre) * 100),
    })).sort((a, b) => b.saturazione - a.saturazione)

    stats.value = {
      totaleSlot,
      oreText: `${totaleOre.toFixed(1)}h`,
      aule:    auleStats,
    }
  } finally {
    loading.value = false
  }
}

function coloreSaturazione(pct) {
  if (pct < 40) return 'bg-success'
  if (pct < 70) return 'bg-warning'
  return 'bg-danger'
}

onMounted(carica)
</script>
