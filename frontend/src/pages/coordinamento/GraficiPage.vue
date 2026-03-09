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
        <button class="btn btn-sm btn-success" @click="esportaCsv">
          <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-download'"></use></svg>
          CSV
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else class="row g-4">
      <!-- Riepilogo KPI -->
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-body py-3">
            <div class="row text-center g-3">
              <div class="col-4">
                <div class="fs-2 fw-bold text-primary">{{ totPrenotazioni }}</div>
                <div class="small text-muted">Prenotazioni totali</div>
              </div>
              <div class="col-4">
                <div class="fs-2 fw-bold text-success">{{ totConfermate }}</div>
                <div class="small text-muted">Confermate</div>
              </div>
              <div class="col-4">
                <div class="fs-2 fw-bold text-danger">{{ totConflitti }}</div>
                <div class="small text-muted">Con conflitti</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Grafico 1: Prenotazioni per periodo -->
      <div class="col-12 col-xl-8">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">Prenotazioni per {{ granularity === 'settimana' ? 'settimana' : 'mese' }}</h5>
          </div>
          <div class="card-body">
            <div v-if="!datiPeriodo.length" class="text-muted text-center py-4 small">Nessun dato</div>
            <div v-else style="overflow-x:auto">
            <svg :viewBox="`0 0 ${Math.max(datiPeriodo.length * 60 + 60, 400)} 260`"
              :style="`width:${Math.max(datiPeriodo.length * 60 + 60, 400)}px;height:260px;max-width:100%`"
              preserveAspectRatio="xMinYMin meet">
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
      </div>

      <!-- Grafico 2: Distribuzione per aula (accordion per sede) -->
      <div class="col-12 col-xl-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">Distribuzione per aula</h5>
          </div>
          <div class="card-body p-0">
            <div v-if="!datiPerSede.length" class="text-muted text-center py-4 small">Nessun dato</div>
            <div v-else class="accordion accordion-flush" id="accordionSedi">
              <div v-for="(sede, si) in datiPerSede" :key="sede.nome" class="accordion-item border-0 border-bottom">
                <h2 class="accordion-header">
                  <button class="accordion-button py-2 px-3 small fw-semibold"
                    :class="{ collapsed: !(accordionAperto === sede.nome || (si === 0 && accordionAperto === null)) }"
                    type="button"
                    @click="toggleAccordion(sede.nome)">
                    {{ sede.nome }}
                    <span class="badge bg-secondary ms-3 me-2">{{ sede.totSlot }} slot</span>
                  </button>
                </h2>
                <div :class="{ show: accordionAperto === sede.nome || (si === 0 && accordionAperto === null) }"
                  class="accordion-collapse collapse">
                  <div class="accordion-body py-2 px-3">
                    <div v-for="(aula, ai) in sede.aule" :key="aula.aulaId" class="mb-2">
                      <div class="d-flex justify-content-between mb-1">
                        <small class="fw-semibold text-truncate" style="max-width:150px">{{ aula.nome }}</small>
                        <small class="text-nowrap ms-1">{{ aula.slot }}&nbsp;<span class="text-muted">slot&nbsp;({{ aula.pct }}%)</span></small>
                      </div>
                      <div class="progress" style="height:6px">
                        <div class="progress-bar"
                          :style="{ width: aula.pct + '%', background: coloriSede[si % coloriSede.length] }">
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Grafico 3: Top corsi (per corso_id) -->
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
            <h5 class="card-title mb-0">Slot per aula</h5>
          </div>
          <div class="card-body">
            <div v-for="(a, i) in datiAule" :key="i" class="mb-3">
              <div class="d-flex justify-content-between mb-1">
                <small class="fw-semibold">{{ a.nome }} <span class="text-muted fw-normal">({{ a.sede }})</span></small>
                <small class="fw-bold">{{ a.slot }} slot</small>
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
import { useAule } from '@/composables/useAule'
import { getPrenotazioni, getConflitti } from '@/api/prenotazioni'
import { oggi, aggiungiGiorni } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const { nomeAula, sedeDiAula, carica: caricaAule } = useAule()
const loading         = ref(false)
const sedi            = ref([])
const prenotazioni    = ref([])
const conflittiAttivi = ref([])
const granularity     = ref('mese')
const range           = ref('6')
const filtroSede      = ref('')
const topN            = ref(10)
const accordionAperto = ref(null)   // null = primo aperto di default

function toggleAccordion(nome) {
  accordionAperto.value = accordionAperto.value === nome ? '__chiudi__' : nome
}

const granularita = [
  { val: 'settimana', label: 'Settimana' },
  { val: 'mese',      label: 'Mese' },
]
const coloriSede = ['#0066cc','#198754','#ffc107','#dc3545','#6f42c1','#fd7e14']

// ── Helper: estrae la data del primo slot ─────────────────────────────────────
function dataSlot(p) { return p.slots?.[0]?.data || '' }

// ── Computed ──────────────────────────────────────────────────────────────────

// Espande ogni prenotazione per numero di slot (1 prenotazione massiva = N slot)
const slotEspansi = computed(() => {
  const list = []
  for (const p of prenotazioni.value) {
    for (const slot of (p.slots || [])) {
      list.push({ ...p, _slotData: slot.data })
    }
  }
  return list
})

const confermate = computed(() => prenotazioni.value.filter(p => p.stato === 'confermata'))

// Dati per grafico a barre per periodo (conta slot confermati)
const datiPeriodo = computed(() => {
  const buckets = {}
  for (const s of slotEspansi.value.filter(s => s.stato === 'confermata')) {
    const d = s._slotData; if (!d) continue
    let key
    if (granularity.value === 'settimana') {
      const dt = new Date(d + 'T00:00:00')
      const day = dt.getDay() || 7
      dt.setDate(dt.getDate() - day + 1)
      key = dt.toISOString().slice(0, 10)
    } else {
      key = d.slice(0, 7)
    }
    buckets[key] = (buckets[key] || 0) + 1
  }
  return Object.entries(buckets).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => ({
    label: granularity.value === 'mese'
      ? new Date(k + '-01').toLocaleDateString('it-IT', { month: 'short', year: '2-digit' })
      : k.slice(5),
    valore: v,
  }))
})

const maxPeriodo = computed(() => Math.max(...datiPeriodo.value.map(x => x.valore), 1))

// Distribuzione per aula_id
const datiSede = computed(() => {
  const map = {}
  for (const p of confermate.value) {
    const k = nomeAula(p.aula_id)
    map[k] = (map[k] || 0) + (p.slots?.length || 1)
  }
  const tot = Object.values(map).reduce((s, v) => s + v, 0) || 1
  return Object.entries(map).sort(([,a],[,b]) => b - a).slice(0, 8)
    .map(([label, valore]) => ({ label, valore, pct: Math.round(valore / tot * 100) }))
})

// Distribuzione per aula raggruppata per sede (accordion)
const datiPerSede = computed(() => {
  const map = {}
  for (const s of slotEspansi.value.filter(s => s.stato === 'confermata')) {
    const k = s.aula_id
    map[k] = (map[k] || 0) + 1
  }
  const sediMap = {}
  for (const [aulaId, slot] of Object.entries(map)) {
    const id = Number(aulaId)
    const nomeSede = sedeDiAula(id) || 'Altra sede'
    if (!sediMap[nomeSede]) sediMap[nomeSede] = { nome: nomeSede, aule: [], totSlot: 0 }
    sediMap[nomeSede].aule.push({ aulaId: id, nome: nomeAula(id), slot })
    sediMap[nomeSede].totSlot += slot
  }
  return Object.values(sediMap)
    .sort((a, b) => b.totSlot - a.totSlot)
    .map(sede => {
      const maxSlot = Math.max(...sede.aule.map(a => a.slot), 1)
      sede.aule = sede.aule
        .sort((a, b) => b.slot - a.slot)
        .map(a => ({ ...a, pct: Math.round(a.slot / maxSlot * 100) }))
      return sede
    })
})

// Top corsi per corso_id
const datiCorsi = computed(() => {
  const map = {}
  for (const p of confermate.value) {
    const k = `Corso ${p.corso_id}`
    map[k] = (map[k] || 0) + 1
  }
  return Object.entries(map).sort(([,a],[,b]) => b - a).map(([label, valore]) => ({ label, valore }))
})

// Slot per aula (conta slot totali confermati)
const datiAule = computed(() => {
  const map = {}
  for (const s of slotEspansi.value.filter(s => s.stato === 'confermata')) {
    const k = s.aula_id
    map[k] = (map[k] || 0) + 1
  }
  const max = Math.max(...Object.values(map), 1)
  return Object.entries(map).sort(([,a],[,b]) => b - a).slice(0, 10)
    .map(([aulaId, slot]) => ({ aulaId, nome: nomeAula(aulaId), sede: sedeDiAula(aulaId), slot, pct: Math.round(slot / max * 100) }))
})

// KPI riepilogo
const totPrenotazioni = computed(() => prenotazioni.value.length)
const totConfermate   = computed(() => prenotazioni.value.filter(p => p.stato === 'confermata').length)
// FIX: conta conflitti NON_RISOLTO distinti da API (non il flag ha_conflitti inaffidabile)
const totConflitti    = computed(() => conflittiAttivi.value.length)

// ── Caricamento ───────────────────────────────────────────────────────────────

async function carica() {
  loading.value = true
  try {
    const fine   = oggi()
    const inizio = aggiungiGiorni(fine, -parseInt(range.value) * 30)
    const data   = await getPrenotazioni({
      data_dal: inizio,
      data_al:  fine,
      ...(filtroSede.value ? { sede_id: filtroSede.value } : {}),
    })
    prenotazioni.value = Array.isArray(data) ? data : (data?.items || [])
  } catch (e) {
    console.warn('Grafici:', e.message)
    prenotazioni.value = []
  } finally {
    loading.value = false
  }
}

function esportaCsv() {
  if (!prenotazioni.value.length) { alert('Nessun dato da esportare.'); return }
  const righe = [['ID', 'Tipo', 'Aula ID', 'Corso ID', 'Stato', 'Ha conflitti', 'Data', 'Ora inizio', 'Ora fine', 'Creata il']]
  for (const p of prenotazioni.value) {
    for (const slot of (p.slots || [])) {
      righe.push([
        p.id, p.tipo, p.aula_id, p.corso_id, p.stato,
        p.richiesta?.ha_conflitti ? 'si' : 'no',
        slot.data || '', slot.ora_inizio || '', slot.ora_fine || '',
        p.data_creazione?.slice(0, 10) || '',
      ])
    }
  }
  const csv  = righe.map(r => r.join(';')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href     = url
  a.download = `prenotazioni_${oggi()}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

onMounted(async () => {
  await caricaAule()
  const data = await getSedi()
  sedi.value = Array.isArray(data) ? data : []
  carica()
  // FIX: conflitti distinti da API — separato per non bloccare su 403 OPERATIVO
  try {
    const cf = await getConflitti({ solo_attivi: true })
    conflittiAttivi.value = Array.isArray(cf) ? cf : (cf?.items || [])
  } catch (e) {
    conflittiAttivi.value = []
  }
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
.bar-chart {
  display: flex; align-items: flex-end; gap: 6px; height: 220px;
  padding: 24px 8px 32px; overflow-x: auto;
}
.bar-col {
  display: flex; flex-direction: column; align-items: center;
  justify-content: flex-end; flex: 1; min-width: 32px; max-width: 64px;
}
.bar-val  { font-size: .7rem; font-weight: 700; color: #333; margin-bottom: 2px; }
.bar-fill { width: 100%; background: #0066cc; opacity: .85; border-radius: 3px 3px 0 0; transition: height .3s; }
.bar-label { font-size: .65rem; color: #888; margin-top: 4px; text-align: center; white-space: nowrap; }
</style>