<template>
  <div class="page-calendario">

    <!-- Header ───────────────────────────────────────────────────────────── -->
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Calendario</h2>
      <div class="ms-auto d-flex gap-2 align-items-center flex-wrap">

        <!-- Vista -->
        <div class="btn-group btn-group-sm">
          <button class="btn simplebtn" :class="vista === 'settimana' ? 'btn-primary' : 'btn-outline-primary'"
            @click="vista = 'settimana'">
            <svg class="icon icon-sm me-1"><use :href="sprites + '#it-calendar'"></use></svg>Settimana
          </button>
          <button class="btn simplebtn" :class="vista === 'mese' ? 'btn-primary' : 'btn-outline-primary'"
            @click="vista = 'mese'">
            <svg class="icon icon-sm me-1"><use :href="sprites + '#it-files'"></use></svg>Mese
          </button>
        </div>

        <!-- Navigazione -->
        <button class="btn" @click="sposta(-1)">
          <svg class="icon icon-sm"><use :href="sprites + '#it-chevron-left'"></use></svg>
        </button>
        <span class="fw-semibold px-1" style="min-width:200px;text-align:center">{{ labelPeriodo }}</span>
        <button class="btn" @click="sposta(1)">
          <svg class="icon icon-sm"><use :href="sprites + '#it-chevron-right'"></use></svg>
        </button>
        <button class="btn btn-outline-primary btn-sm" @click="vaiOggi">Oggi</button>

        <!-- Filtro sede -->
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="onSedeChange">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>

        <!-- Filtro aula -->
        <select v-model="filtroAula" class="form-select form-select-sm" style="width:auto">
          <option value="">Tutte le aule</option>
          <option v-for="a in auleFiltrate" :key="a.id" :value="a.id">{{ a.nome }}</option>
        </select>

        <RouterLink :to="{ name: 'NuovaPrenotazione' }" class="btn btn-primary btn-sm">
          <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>Nuova
        </RouterLink>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <!-- ── VISTA SETTIMANALE ──────────────────────────────────────────────── -->
    <div v-else-if="vista === 'settimana'" class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div class="cal-grid">
          <div class="cal-header">
            <div class="cal-time-col"></div>
            <div v-for="(g, i) in giorniSettimana" :key="i"
              class="cal-day-header" :class="{ 'cal-day-today': isToday(g) }">
              <span class="cal-day-name">{{ nomGiorno(g) }}</span>
              <span class="cal-day-num"
                :class="isToday(g) ? 'badge bg-primary rounded-circle' : ''">{{ g.getDate() }}</span>
            </div>
          </div>
          <div class="cal-body">
            <div v-for="ora in oreGiornata" :key="ora" class="cal-row">
              <div class="cal-time-label">{{ String(ora).padStart(2,'0') }}:00</div>
              <div v-for="(g, gi) in giorniSettimana" :key="gi"
                class="cal-cell" :class="{ 'cal-cell-today': isToday(g) }">
                <div v-for="ev in eventiCella(g, ora)" :key="ev.prenId + '-' + ev.slotIdx"
                  class="cal-event" :class="coloreEvento(ev)"
                  :title="`#${ev.prenId} — ${nomeAulaFn(ev.aulaId)} — Corso ${ev.corsoId}`">
                  <span class="cal-event-time">{{ ev.oraInizio }}–{{ ev.oraFine }}</span>
                  <span class="cal-event-title">{{ nomeAulaFn(ev.aulaId) }}</span>
                  <span class="cal-event-room">Corso {{ ev.corsoId }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── VISTA MENSILE ─────────────────────────────────────────────────── -->
    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div class="mes-grid">
          <!-- Intestazione giorni -->
          <div class="mes-header">
            <div v-for="n in nomiGiorni" :key="n" class="mes-dow">{{ n }}</div>
          </div>
          <!-- Celle -->
          <div class="mes-body">
            <div v-for="(cella, ci) in celleMese" :key="ci"
              class="mes-cell"
              :class="{
                'mes-cell--other':   !cella.corrente,
                'mes-cell--today':    cella.oggi,
                'mes-cell--weekend':  cella.weekend,
              }">
              <span class="mes-cell-num" :class="cella.oggi ? 'badge bg-primary rounded-circle' : ''">
                {{ cella.d.getDate() }}
              </span>
              <div class="mes-events">
                <div v-for="(ev, ei) in eventiGiorno(cella.d).slice(0, 3)" :key="ei"
                  class="mes-event" :class="coloreEvento(ev)"
                  :title="`${nomeAulaFn(ev.aulaId)} — Corso ${ev.corsoId} — ${ev.oraInizio}–${ev.oraFine}`">
                  <span class="text-truncate">{{ nomeAulaFn(ev.aulaId) }}</span>
                </div>
                <div v-if="eventiGiorno(cella.d).length > 3" class="mes-event-more">
                  +{{ eventiGiorno(cella.d).length - 3 }} altri
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legenda -->
    <div class="d-flex gap-3 mt-3 flex-wrap">
      <span v-for="(l, i) in legenda" :key="i" class="d-flex align-items-center gap-1 small">
        <span :style="`width:12px;height:12px;background:${l.bg};border-left:3px solid ${l.border};display:inline-block;border-radius:2px`"></span>
        {{ l.label }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { getCalendario } from '@/api/prenotazioni'
import { useAule } from '@/composables/useAule'
import { oggi, aggiungiGiorni, inizioSettimana } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading    = ref(false)
const filtroSede = ref('')
const filtroAula = ref('')
const vista      = ref('settimana')   // 'settimana' | 'mese'
const sedi       = ref([])
const aule       = ref([])
const prenotazioni = ref([])
const dataRef    = ref(oggi())

const { nomeAula: nomeAulaFn, carica: caricaAule } = useAule()

const nomiGiorni = ['Lun','Mar','Mer','Gio','Ven','Sab','Dom']

// ── Filtro aule per sede ──────────────────────────────────────────────────────
const auleFiltrate = computed(() =>
  filtroSede.value
    ? aule.value.filter(a => a.sede_id == filtroSede.value)
    : aule.value
)

function onSedeChange() {
  filtroAula.value = ''   // reset filtro aula quando cambia sede
}

// ── Periodo ───────────────────────────────────────────────────────────────────
const giorniSettimana = computed(() => {
  const lun = new Date(inizioSettimana(dataRef.value) + 'T00:00:00')
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(lun); d.setDate(lun.getDate() + i); return d
  })
})

const oreGiornata = Array.from({ length: 13 }, (_, i) => i + 7)

function inizioMese() {
  const d = new Date(dataRef.value + 'T00:00:00'); d.setDate(1); return d
}
function fineMese() {
  const d = inizioMese(); d.setMonth(d.getMonth() + 1); d.setDate(0); return d
}

const celleMese = computed(() => {
  const ini  = inizioMese()
  const fin  = fineMese()
  const oggiStr = oggi()
  // Aggiungi celle dei giorni precedenti per allineare al lunedì
  const cells = []
  const primoGiorno = ini.getDay() === 0 ? 6 : ini.getDay() - 1
  for (let i = primoGiorno; i > 0; i--) {
    const d = new Date(ini); d.setDate(d.getDate() - i)
    cells.push({ d, corrente: false, oggi: false, weekend: d.getDay() === 0 || d.getDay() === 6 })
  }
  for (let g = 1; g <= fin.getDate(); g++) {
    const d = new Date(ini); d.setDate(g)
    cells.push({ d, corrente: true, oggi: d.toISOString().slice(0,10) === oggiStr, weekend: d.getDay() === 0 || d.getDay() === 6 })
  }
  // Riempi righe incomplete fino a multiplo di 7
  while (cells.length % 7 !== 0) {
    const d = new Date(fin); d.setDate(fin.getDate() + (cells.length - fin.getDate() - primoGiorno + 1))
    cells.push({ d, corrente: false, oggi: false, weekend: d.getDay() === 0 || d.getDay() === 6 })
  }
  return cells
})

const labelPeriodo = computed(() => {
  if (vista.value === 'settimana') {
    const ini = giorniSettimana.value[0]
    const fin = giorniSettimana.value[6]
    const opt = { day: 'numeric', month: 'short' }
    return `${ini.toLocaleDateString('it-IT', opt)} – ${fin.toLocaleDateString('it-IT', opt)} ${fin.getFullYear()}`
  } else {
    return new Date(dataRef.value + 'T00:00:00')
      .toLocaleDateString('it-IT', { month: 'long', year: 'numeric' })
  }
})

function isToday(d) { return d.toISOString().slice(0,10) === oggi() }
function nomGiorno(d) { return d.toLocaleDateString('it-IT', { weekday: 'short' }).toUpperCase() }

function sposta(n) {
  if (vista.value === 'settimana') {
    dataRef.value = aggiungiGiorni(dataRef.value, n * 7)
  } else {
    const d = new Date(dataRef.value + 'T00:00:00')
    d.setMonth(d.getMonth() + n)
    dataRef.value = d.toISOString().slice(0,10)
  }
}
function vaiOggi() { dataRef.value = oggi() }

// ── Eventi filtrati ────────────────────────────────────────────────────────────
const eventiFiltrati = computed(() => {
  const list = []
  for (const p of prenotazioni.value) {
    if (filtroAula.value && p.aula_id != filtroAula.value) continue
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]; if (!slot?.data) continue
      list.push({
        prenId:      p.id,
        slotIdx:     si,
        aulaId:      p.aula_id,
        corsoId:     p.corso_id,
        stato:       p.stato,
        haConflitti: p.richiesta?.ha_conflitti || false,
        data:        slot.data,
        oraInizio:   slot.ora_inizio?.slice(0,5) || '',
        oraFine:     slot.ora_fine?.slice(0,5)   || '',
        oraH:        parseInt(slot.ora_inizio?.slice(0,2) || '0'),
      })
    }
  }
  return list
})

// Mappa "YYYY-MM-DD|HH" → eventi (per vista settimanale)
const eventiPerCella = computed(() => {
  const map = {}
  for (const ev of eventiFiltrati.value) {
    const key = `${ev.data}|${ev.oraH}`
    if (!map[key]) map[key] = []
    map[key].push(ev)
  }
  return map
})

// Mappa "YYYY-MM-DD" → eventi (per vista mensile)
const eventiPerGiorno = computed(() => {
  const map = {}
  for (const ev of eventiFiltrati.value) {
    if (!map[ev.data]) map[ev.data] = []
    map[ev.data].push(ev)
  }
  return map
})

function eventiCella(giorno, ora) {
  return eventiPerCella.value[`${giorno.toISOString().slice(0,10)}|${ora}`] || []
}
function eventiGiorno(d) {
  return eventiPerGiorno.value[d.toISOString().slice(0,10)] || []
}

function coloreEvento(ev) {
  if (!ev) return 'cal-event--confirmed'
  const s = (ev.stato || '').toLowerCase().trim()
  if (s === 'annullata' || s === 'rifiutata') return 'cal-event--cancelled'
  if (ev.haConflitti || s === 'conflitto')    return 'cal-event--cancelled'
  if (s === 'in_attesa')                      return 'cal-event--pending'
  return 'cal-event--confirmed'
}

const legenda = [
  { label: 'Confermata', bg: '#d4edda', border: '#198754' },
  // { label: 'In attesa',  bg: '#fff3cd', border: '#ffc107' },
  { label: 'Conflitto', bg: '#f8d7da', border: '#dc3545' },
]

// ── Caricamento ───────────────────────────────────────────────────────────────
async function caricaDati() {
  loading.value = true
  try {
    let ini, fin
    if (vista.value === 'settimana') {
      ini = giorniSettimana.value[0].toISOString().slice(0,10)
      fin = giorniSettimana.value[6].toISOString().slice(0,10)
    } else {
      ini = inizioMese().toISOString().slice(0,10)
      fin = fineMese().toISOString().slice(0,10)
    }
    const data = await getCalendario(ini, fin, filtroSede.value || null)
    prenotazioni.value = Array.isArray(data) ? data : (data?.items || [])
  } catch (e) {
    console.warn('Calendario:', e.message)
    prenotazioni.value = []
  } finally {
    loading.value = false
  }
}

watch([dataRef, filtroSede, vista], caricaDati)

onMounted(async () => {
  await caricaAule()
  const [dataSedi, dataAule] = await Promise.all([getSedi(), getAule()])
  sedi.value  = Array.isArray(dataSedi)  ? dataSedi  : []
  aule.value  = Array.isArray(dataAule)  ? dataAule  : []
  caricaDati()
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }

/* ── SETTIMANALE ── */
.cal-grid  { overflow-x: auto; min-width: 700px; }
.cal-header, .cal-row {
  display: grid;
  grid-template-columns: 52px repeat(7, 1fr);
  border-bottom: 1px solid #eee;
}
.cal-day-header { padding: .5rem .25rem; text-align: center; border-left: 1px solid #eee; }
.cal-day-header.cal-day-today { background: #eef4ff; }
.cal-day-name  { display: block; font-size: .65rem; color: #999; font-weight: 600; }
.cal-day-num   { font-size: .9rem; font-weight: 700; width: 28px; height: 28px;
  display: inline-flex; align-items: center; justify-content: center; }
.cal-time-col  { border-right: 1px solid #eee; }
.cal-time-label { padding: .25rem .3rem; font-size: .65rem; color: #999;
  border-right: 1px solid #eee; white-space: nowrap; }
.cal-cell      { min-height: 48px; border-left: 1px solid #eee; padding: 2px; }
.cal-cell-today { background: #f7f9ff; }

/* ── MENSILE ── */
.mes-grid  { overflow-x: auto; min-width: 600px; }
.mes-header { display: grid; grid-template-columns: repeat(7, 1fr); }
.mes-dow   { padding: .4rem; text-align: center; font-size: .7rem; font-weight: 700;
  color: #888; border-bottom: 2px solid #eee; }
.mes-body  { display: grid; grid-template-columns: repeat(7, 1fr); }
.mes-cell  { min-height: 90px; border: 1px solid #eee; padding: 4px;
  background: #fff; overflow: hidden; }
.mes-cell--other   { background: #f8f9fa; }
.mes-cell--other .mes-cell-num { color: #bbb; }
.mes-cell--today   { background: #f0f5ff; }
.mes-cell--weekend { background: #fafafa; }
.mes-cell-num      { font-size: .78rem; font-weight: 700; width: 22px; height: 22px;
  display: inline-flex; align-items: center; justify-content: center; margin-bottom: 2px; }
.mes-events { display: flex; flex-direction: column; gap: 2px; }
.mes-event  { border-radius: 3px; padding: 1px 4px; font-size: .65rem;
  display: flex; overflow: hidden; cursor: default; }
.mes-event-more { font-size: .6rem; color: #888; padding-left: 4px; }

/* ── EVENTI (condivisi) ── */
.cal-event {
  border-radius: 4px; padding: 2px 5px; margin-bottom: 2px;
  font-size: .68rem; display: flex; flex-direction: column; overflow: hidden; cursor: default;
}
.cal-event--confirmed { background: #d4edda !important; border-left: 3px solid #198754 !important; color: #0d4f2b !important; }
.cal-event--pending   { background: #fff3cd !important; border-left: 3px solid #ffc107 !important; color: #664d03 !important; }
.cal-event--cancelled { background: #f8d7da !important; border-left: 3px solid #dc3545 !important; color: #5c1a1e !important; }
.cal-event-time  { font-weight: 600; }
.cal-event-title { font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cal-event-room  { opacity: .7; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>