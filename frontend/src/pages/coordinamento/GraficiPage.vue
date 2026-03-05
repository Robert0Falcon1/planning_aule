<template>
  <div class="page-grafici">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Grafici &amp; Report</h2>
      <div class="ms-auto d-flex gap-2 flex-wrap align-items-center">
        <div class="btn-group btn-group-sm" role="group">
          <button v-for="g in granularita" :key="g.val" class="btn"
            :class="granularity === g.val ? 'btn-primary' : 'btn-outline-primary'"
            @click="granularity = g.val; carica()">{{ g.label }}</button>
        </div>
        <select v-model="range" class="form-select form-select-sm" style="width:auto" @change="carica">
          <option value="3">Ultimi 3 mesi</option>
          <option value="6">Ultimi 6 mesi</option>
          <option value="12">Ultimi 12 mesi</option>
        </select>
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="carica">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>
        <button class="btn btn-sm btn-success" @click="esporta">
          <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-download'"></use></svg>
          CSV
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else class="row g-4">
      <!-- Grafico 1: Prenotazioni per periodo -->
      <div class="col-12 col-xl-8">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">Prenotazioni per {{ granularity === 'settimana' ? 'settimana' : 'mese' }}</h5>
          </div>
          <div class="card-body">
            <div v-if="!datiPeriodo.length" class="text-muted text-center py-4 small">Nessun dato</div>
            <svg v-else :viewBox="`0 0 ${datiPeriodo.length * 60 + 20} 260`" style="width:100%;height:260px" preserveAspectRatio="none">
              <template v-for="(item, i) in datiPeriodo" :key="i">
                <rect :x="30 + i * 60 + 8" :y="40 + 190 - (item.valore / maxPeriodo) * 190"
                  width="44" :height="(item.valore / maxPeriodo) * 190" rx="3" fill="#0066cc" opacity="0.85" />
                <text :x="30 + i * 60 + 30" :y="40 + 190 - (item.valore / maxPeriodo) * 190 - 4"
                  text-anchor="middle" font-size="9" fill="#333" font-weight="600">{{ item.valore }}</text>
                <text :x="30 + i * 60 + 30" y="254"
                  text-anchor="middle" font-size="8" fill="#888">{{ item.label }}</text>
              </template>
            </svg>
          </div>
        </div>
      </div>

      <!-- Grafico 2: Distribuzione per sede -->
      <div class="col-12 col-xl-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">Distribuzione per sede</h5>
          </div>
          <div class="card-body">
            <div v-if="!datiSede.length" class="text-muted text-center py-4 small">Nessun dato</div>
            <div v-else>
              <div v-for="(item, i) in datiSede" :key="i" class="mb-2">
                <div class="d-flex justify-content-between mb-1">
                  <small class="fw-semibold">{{ item.label }}</small>
                  <small>{{ item.pct }}%</small>
                </div>
                <div class="progress" style="height:8px">
                  <div class="progress-bar" :style="{ width: item.pct + '%', background: coloriSede[i % coloriSede.length] }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Grafico 3: Top corsi -->
      <div class="col-12 col-xl-7">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Top corsi per prenotazioni</h5>
            <select v-model="topN" class="form-select form-select-sm" style="width:auto">
              <option :value="5">Top 5</option>
              <option :value="10">Top 10</option>
              <option :value="20">Top 20</option>
            </select>
          </div>
          <div class="card-body">
            <div v-if="!datiCorsi.length" class="text-muted text-center py-4 small">Nessun dato</div>
            <div v-else>
              <div v-for="(item, i) in datiCorsi.slice(0, topN)" :key="i" class="mb-2 d-flex align-items-center gap-2">
                <small class="text-truncate" style="width:180px">{{ item.label }}</small>
                <div class="progress flex-grow-1" style="height:10px">
                  <div class="progress-bar bg-primary" :style="{ width: (item.valore / datiCorsi[0].valore * 100) + '%' }"></div>
                </div>
                <small class="fw-semibold" style="width:28px">{{ item.valore }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Grafico 4: Saturazione per aula -->
      <div class="col-12 col-xl-5">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">Saturazione per aula</h5>
          </div>
          <div class="card-body">
            <div v-for="a in datiAule" :key="a.nome" class="mb-3">
              <div class="d-flex justify-content-between mb-1">
                <small class="fw-semibold">{{ a.nome }} <span class="text-muted fw-normal">({{ a.sede }})</span></small>
                <small class="fw-bold">{{ a.pct }}%</small>
              </div>
              <div class="progress" style="height:10px">
                <div class="progress-bar"
                  :class="a.pct >= 80 ? 'bg-danger' : a.pct >= 50 ? 'bg-warning' : 'bg-success'"
                  :style="{ width: a.pct + '%' }"></div>
              </div>
            </div>
            <div v-if="!datiAule.length" class="text-muted small text-center">Nessun dato</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { getPrenotazioni, esportaCsv } from '@/api/prenotazioni'
import { oggi, aggiungiGiorni, percentuale } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading     = ref(false)
const sedi        = ref([])
const aule        = ref([])
const prenotazioni = ref([])
const granularity = ref('mese')
const range       = ref('6')
const filtroSede  = ref('')
const topN        = ref(10)

const granularita = [
  { val: 'settimana', label: 'Settimana' },
  { val: 'mese',      label: 'Mese' },
]

const coloriSede = ['#0066cc','#198754','#ffc107','#dc3545','#6f42c1','#fd7e14']

const datiPeriodo = computed(() => {
  const buckets = {}
  for (const p of prenotazioni.value.filter(p => p.stato === 'confermata' || p.stato === 'CONFERMATA')) {
    const d = new Date(p.data)
    let key
    if (granularity.value === 'settimana') {
      const lun = new Date(d); const day = lun.getDay() || 7
      lun.setDate(lun.getDate() - day + 1)
      key = lun.toISOString().slice(0, 10)
    } else {
      key = p.data?.slice(0, 7)
    }
    if (key) buckets[key] = (buckets[key] || 0) + 1
  }
  return Object.entries(buckets).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => ({
    label: granularity.value === 'mese'
      ? new Date(k + '-01').toLocaleDateString('it-IT', { month: 'short', year: '2-digit' })
      : k.slice(5),
    valore: v,
  }))
})

const maxPeriodo = computed(() => Math.max(...datiPeriodo.value.map(x => x.valore), 1))

const datiSede = computed(() => {
  const map = {}
  for (const p of prenotazioni.value.filter(p => p.stato === 'confermata' || p.stato === 'CONFERMATA')) {
    const nome = p.aula?.sede?.nome || '—'
    map[nome] = (map[nome] || 0) + 1
  }
  const tot = Object.values(map).reduce((s, v) => s + v, 0) || 1
  return Object.entries(map).map(([label, valore]) => ({ label, valore, pct: Math.round(valore / tot * 100) }))
})

const datiCorsi = computed(() => {
  const map = {}
  for (const p of prenotazioni.value.filter(p => p.stato === 'confermata' || p.stato === 'CONFERMATA')) {
    const titolo = p.titolo_corso || p.corso?.titolo || 'Sconosciuto'
    map[titolo] = (map[titolo] || 0) + 1
  }
  return Object.entries(map).sort(([, a], [, b]) => b - a).map(([label, valore]) => ({ label, valore }))
})

const datiAule = computed(() => {
  const totPerAula = {}
  for (const p of prenotazioni.value) {
    const id = p.aula_id || p.aula?.id
    if (!totPerAula[id]) totPerAula[id] = { nome: p.aula?.nome || '?', sede: p.aula?.sede?.nome || '?', tot: 0, conf: 0 }
    totPerAula[id].tot++
    if (p.stato === 'confermata' || p.stato === 'CONFERMATA') totPerAula[id].conf++
  }
  return Object.values(totPerAula).map(a => ({ nome: a.nome, sede: a.sede, pct: percentuale(a.conf, a.tot) })).sort((a, b) => b.pct - a.pct)
})

async function carica() {
  loading.value = true
  try {
    const fine   = oggi()
    const inizio = aggiungiGiorni(fine, -parseInt(range.value) * 30)
    const data   = await getPrenotazioni({ data_dal: inizio, data_al: fine, sede_id: filtroSede.value || undefined })
    prenotazioni.value = data?.items || data || []
  } catch (e) {
    console.warn('Grafici:', e.message)
    prenotazioni.value = []
  } finally {
    loading.value = false
  }
}

async function esporta() {
  try {
    const fine   = oggi()
    const inizio = aggiungiGiorni(fine, -parseInt(range.value) * 30)
    await esportaCsv({ data_dal: inizio, data_al: fine, sede_id: filtroSede.value || undefined })
  } catch (e) {
    alert(`Errore export: ${e.message}`)
  }
}

onMounted(async () => {
  const [dataSedi, dataAule] = await Promise.allSettled([getSedi(), getAule()])
  sedi.value  = dataSedi.value?.items  || dataSedi.value  || []
  aule.value  = dataAule.value?.items  || dataAule.value  || []
  carica()
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
</style>