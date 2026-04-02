<template>
  <div class="page-calendario">
    <!-- Header -->
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">
        Calendario
        <span class="info-popover">
          <i class="bi bi-info-circle" style="font-size: .8rem;"></i>
          <span class="popover-content">
            Il calendario globale delle prenotazioni nelle varie sedi con vista: 4 giorni - settimanale - mensile
          </span>
        </span>
      </h2>
      <div class="ms-auto d-flex gap-2 align-items-center flex-wrap">
        <div class="btn-group btn-group-sm">
          <button class="btn simplebtn"
            :class="vista === 'giorno' ? 'btn-primary' : 'btn-outline-primary btn-no-border-e'"
            @click="vista = 'giorno'"><svg class="icon icon-sm me-1">
              <use :href="sprites + '#it-note'"></use>
            </svg>Giorno</button>
          <button class="btn simplebtn" :class="vista === '4giorni' ? 'btn-primary' : 'btn-outline-primary'"
            @click="vista = '4giorni'">
            <svg class="icon icon-sm me-1">
              <use :href="sprites + '#it-calendar'"></use>
            </svg>4 giorni</button>
          <button class="btn simplebtn"
            :class="vista === 'settimana' ? 'btn-primary' : 'btn-no-border-x btn-outline-primary'"
            @click="vista = 'settimana'">
            <svg class="icon icon-sm me-1">
              <use :href="sprites + '#it-calendar'"></use>
            </svg>Settimana
          </button>
          <button class="btn simplebtn" :class="vista === 'mese' ? 'btn-primary' : 'btn-outline-primary'"
            @click="vista = 'mese'">
            <svg class="icon icon-sm me-1">
              <use :href="sprites + '#it-files'"></use>
            </svg>Mese
          </button>
        </div>
        <button class="btn" @click="sposta(-1)">
          <svg class="icon icon-sm">
            <use :href="sprites + '#it-chevron-left'"></use>
          </svg>
        </button>
        <span class="fw-semibold px-1" style="min-width:200px;text-align:center">{{ labelPeriodo }}</span>
        <button class="btn" @click="sposta(1)">
          <svg class="icon icon-sm">
            <use :href="sprites + '#it-chevron-right'"></use>
          </svg>
        </button>
        <button class="btn btn-outline-primary btn-sm" @click="vaiOggi">Oggi</button>
        <!-- Filtro sede -->
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="onSedeChange">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>
        <!-- Filtro aula -->
        <select v-model="filtroAula" class="form-select form-select-sm" style="width:auto" :disabled="!filtroSede">
          <option value="">Tutte le aule</option>
          <option v-for="a in auleFiltrate" :key="a.id" :value="a.id">{{ a.nome }}</option>
        </select>
        <RouterLink :to="{ name: 'NuovaPrenotazione' }" class="btn btn-primary btn-sm">
          <svg class="icon icon-white icon-sm me-1">
            <use :href="sprites + '#it-plus-circle'"></use>
          </svg>Nuova
        </RouterLink>
      </div>
    </div>
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>
    <!-- ── VISTA GRIGLIA (4 giorni + settimana) ── -->
    <div v-else-if="vista !== 'mese'" class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div class="cal-week">
          <div class="cal-week-header pe-3" :style="headerGridStyle">
            <div class="cal-gutter-head"></div>
            <div v-for="(g, i) in giorniVista" :key="i" class="cal-day-head" :class="{ 'is-today': isToday(g) }">
              <span class="cal-dow">{{ nomGiorno(g) }}</span>
              <span class="cal-dnum" :class="isToday(g) ? 'badge bg-primary rounded-circle' : ''">
                {{ g.getDate() }}
              </span>
            </div>
          </div>
          <div class="cal-week-body" :style="bodyGridStyle">
            <div class="cal-gutter">
              <div v-for="ora in oreGiornata" :key="ora" class="cal-gutter-slot">
                <span class="cal-ora-label">{{ String(ora).padStart(2, '0') }}:00</span>
              </div>
            </div>
            <div v-for="(g, gi) in giorniVista" :key="gi" 
                 class="cal-day-col cal-day-col--clickable" 
                 :class="{ 'is-today': isToday(g) }"
                 :style="{ height: altezzaTotale + 'px' }"
                 @click="vaiNuovaPrenotazione(g)">
              <div v-for="ora in oreGiornata" :key="ora" class="cal-bg-line"
                :style="{ top: (ora - ORA_INIZIO) * SLOT_H + 'px' }"></div>
              <div class="cal-bg-line cal-bg-line--end" :style="{ top: oreGiornata.length * SLOT_H + 'px' }"></div>
              <div v-if="isToday(g) && nowTop >= 0" class="cal-now-line" :style="{ top: nowTop + 'px' }">
                <span class="cal-now-dot"></span>
              </div>
              <div v-for="ev in eventiLayoutGiorno(g)" :key="ev.prenId + '-' + ev.slotIdx" class="cal-ev"
                :class="coloreEvento(ev)" :style="evStyle(ev)" 
                @click.stop
                @mouseenter="e => mostraPopover(e, ev)"
                @mouseleave="chiudiPopover">
                <span class="cal-ev-time">{{ ev.oraInizio }}–{{ ev.oraFine }}</span>
                <span class="cal-ev-title d-flex align-items-center">
                  <span :style="getAulaBadgeStyle(nomeAulaFn(ev.aulaId))"></span>
                  {{ nomeAulaFn(ev.aulaId) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- ── VISTA MENSILE ── -->
    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div class="mes-grid">
          <div class="mes-header">
            <div v-for="n in nomiGiorni" :key="n" class="mes-dow">{{ n }}</div>
          </div>
          <div class="mes-body">
            <div v-for="(cella, ci) in celleMese" :key="ci" 
                 class="mes-cell mes-cell--clickable" 
                 :class="{
                   'mes-cell--other': !cella.corrente,
                   'mes-cell--today': cella.oggi,
                   'mes-cell--weekend': cella.weekend,
                 }"
                 @click="vaiNuovaPrenotazione(cella.d)">
              <span class="mes-cell-num" :class="cella.oggi ? 'badge bg-primary rounded-circle' : ''">
                {{ cella.d.getDate() }}
              </span>
              <div class="mes-events" @click.stop>
                <div v-for="(ev, ei) in eventiGiornoMese(cella.d).slice(0, 3)" :key="ei" class="mes-event"
                  :class="coloreEvento(ev)" @mouseenter="e => mostraPopover(e, ev)" @mouseleave="chiudiPopover">
                  <span class="text-truncate d-flex align-items-center">
                    <span :style="getAulaBadgeStyle(nomeAulaFn(ev.aulaId))"></span>
                    {{ ev.oraInizio }} {{ nomeAulaFn(ev.aulaId) }}
                  </span>
                </div>
                <div v-if="eventiGiornoMese(cella.d).length > 3" class="mes-event-more">
                  +{{ eventiGiornoMese(cella.d).length - 3 }} altri
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
        <span
          :style="`width:12px;height:12px;background:${l.bg};border-left:3px solid ${l.border};display:inline-block;border-radius:2px`"></span>
        {{ l.label }}
      </span>
    </div>
    <!-- ── POPOVER EVENTO ── -->
    <Teleport to="body">
      <div v-if="popover.visible" class="cal-popover" :style="{ top: popover.y + 'px', left: popover.x + 'px' }"
        @mouseenter="cancellaChiudiPopover" @mouseleave="chiudiPopover">
        <div class="cal-popover-header" :class="coloreEvento(popover.ev)">
          <span class="fw-bold">{{ popover.ev?.oraInizio }} – {{ popover.ev?.oraFine }}</span>
          <span v-if="popover.ev?.haConflitti" class="badge bg-danger ms-2">Conflitto</span>
        </div>
        <div class="cal-popover-body">
          <div class="mb-1">
            <svg class="icon icon-sm me-1 text-primary">
              <use :href="sprites + '#it-map-marker'"></use>
            </svg>
            <strong>{{ nomeAulaFn(popover.ev?.aulaId) }}</strong>
          </div>
          <div class="mb-1 text-muted small">{{ sedeDiAulaFn(popover.ev?.aulaId) }}</div>
          <div class="mb-1">
            <svg class="icon icon-sm me-1 text-secondary">
              <use :href="sprites + '#it-list'"></use>
            </svg>
            {{ formatCorso(popover.ev?.corsoId) }}
          </div>
          <div class="mb-1">
            <svg class="icon icon-sm me-1 text-secondary">
              <use :href="sprites + '#it-user'"></use>
            </svg>
            {{ getNomeDocente(popover.ev?.docenteId) }}
          </div>
          <div v-if="popover.ev?.note" class="mt-1 fst-italic text-muted small">
            <svg class="icon icon-sm me-1">
              <use :href="sprites + '#it-comment'"></use>
            </svg>
            {{ popover.ev.note }}
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { getCalendario, getConflitti } from '@/api/prenotazioni'
import { useAule } from '@/composables/useAule'
import { useAulaColor } from '@/composables/useAulaColor'
import { useCorsi } from '@/composables/useCorsi'
import { useDocenti } from '@/composables/useDocenti'  // ← AGGIUNTO
import { oggi, aggiungiGiorni, inizioSettimana } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import { useSedePerFiltro } from '@/composables/useSedePerFiltro'

const ORA_INIZIO = 7
const ORA_FINE = 21
const SLOT_H = 56
const GAP = 2
const altezzaTotale = (ORA_FINE - ORA_INIZIO) * SLOT_H

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const filtroSede = ref('')
const filtroAula = ref('')
const vista = ref('settimana')
const sedi = ref([])
const aule = ref([])
const prenotazioni = ref([])
const conflittiAttivi = ref([])
const dataRef = ref(oggi())
const nowTop = ref(-1)
const { sedeDefaultFiltro } = useSedePerFiltro()
const { nomeAula: nomeAulaFn, sedeDiAula: sedeDiAulaFn, carica: caricaAule } = useAule()
const { getAulaBadgeStyle } = useAulaColor()
const { caricaCorsi, getTitoloCorso, formatCorso } = useCorsi()
const { getNomeDocente, caricaDocenti } = useDocenti()  // ← AGGIUNTO

// ── FIX TIMEZONE ─────────────────────────────────────────────────────────────
function dateToISO(d) {
  return [
    d.getFullYear(),
    String(d.getMonth() + 1).padStart(2, '0'),
    String(d.getDate()).padStart(2, '0'),
  ].join('-')
}

function vaiNuovaPrenotazione(data) {
  const dataISO = dateToISO(data)
  router.push({ 
    name: 'NuovaPrenotazione', 
    query: { data: dataISO } 
  })
}

const slotIdConConflitti = computed(() => {
  const s = new Set()
  for (const cf of conflittiAttivi.value) {
    if (cf.slot_id_1) s.add(cf.slot_id_1)
    if (cf.slot_id_2) s.add(cf.slot_id_2)
  }
  return s
})

const nomiGiorni = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
const oreGiornata = Array.from({ length: ORA_FINE - ORA_INIZIO }, (_, i) => i + ORA_INIZIO)

// ── Popover ───────────────────────────────────────────────────────────────────
const popover = reactive({ visible: false, ev: null, x: 0, y: 0 })
let popoverTimer = null

function mostraPopover(e, ev) {
  cancellaChiudiPopover()
  const rect = e.currentTarget.getBoundingClientRect()
  let x = rect.right + window.scrollX + 8
  if (x + 260 > window.innerWidth) x = rect.left + window.scrollX - 268
  const y = Math.min(rect.top + window.scrollY, window.innerHeight + window.scrollY - 180)
  popover.ev = ev; popover.x = x; popover.y = y; popover.visible = true
}

function chiudiPopover() {
  popoverTimer = setTimeout(() => { popover.visible = false }, 120)
}

function cancellaChiudiPopover() {
  if (popoverTimer) { clearTimeout(popoverTimer); popoverTimer = null }
}

// ── Ora corrente ──────────────────────────────────────────────────────────────
function aggiornaNow() {
  const now = new Date()
  nowTop.value = (now.getHours() + now.getMinutes() / 60 - ORA_INIZIO) * SLOT_H
}
setInterval(aggiornaNow, 60000)

// ── Filtri ────────────────────────────────────────────────────────────────────
const auleFiltrate = computed(() =>
  filtroSede.value ? aule.value.filter(a => a.sede_id == filtroSede.value) : aule.value
)

function onSedeChange() { filtroAula.value = '' }

// ── Giorni visibili per vista ─────────────────────────────────────────────────
const nGiorni = computed(() => {
  if (vista.value === 'giorno') return 1
  if (vista.value === '4giorni') return 4
  return 7
})

const giorniVista = computed(() => {
  const start = vista.value === 'settimana'
    ? new Date(inizioSettimana(dataRef.value) + 'T00:00:00')
    : new Date(dataRef.value + 'T00:00:00')
  return Array.from({ length: nGiorni.value }, (_, i) => {
    const d = new Date(start); d.setDate(start.getDate() + i); return d
  })
})

const headerGridStyle = computed(() => ({
  gridTemplateColumns: `52px repeat(${nGiorni.value}, 1fr)`
}))

const bodyGridStyle = computed(() => ({
  gridTemplateColumns: `52px repeat(${nGiorni.value}, 1fr)`
}))

// ── Periodo mensile ───────────────────────────────────────────────────────────
function inizioMese() { const d = new Date(dataRef.value + 'T00:00:00'); d.setDate(1); return d }
function fineMese() { const d = inizioMese(); d.setMonth(d.getMonth() + 1); d.setDate(0); return d }

const celleMese = computed(() => {
  const ini = inizioMese(), fin = fineMese(), oggiStr = oggi()
  const cells = [], primoGiorno = ini.getDay() === 0 ? 6 : ini.getDay() - 1
  for (let i = primoGiorno; i > 0; i--) {
    const d = new Date(ini); d.setDate(d.getDate() - i)
    cells.push({ d, corrente: false, oggi: false, weekend: d.getDay() === 0 || d.getDay() === 6 })
  }
  for (let g = 1; g <= fin.getDate(); g++) {
    const d = new Date(ini); d.setDate(g)
    cells.push({ d, corrente: true, oggi: dateToISO(d) === oggiStr, weekend: d.getDay() === 0 || d.getDay() === 6 })
  }
  while (cells.length % 7 !== 0) {
    const d = new Date(fin); d.setDate(fin.getDate() + (cells.length - fin.getDate() - primoGiorno + 1))
    cells.push({ d, corrente: false, oggi: false, weekend: d.getDay() === 0 || d.getDay() === 6 })
  }
  return cells
})

const labelPeriodo = computed(() => {
  if (vista.value === 'mese')
    return new Date(dataRef.value + 'T00:00:00').toLocaleDateString('it-IT', { month: 'long', year: 'numeric' })
  const ini = giorniVista.value[0], fin = giorniVista.value[giorniVista.value.length - 1]
  const opt = { day: 'numeric', month: 'short' }
  return `${ini.toLocaleDateString('it-IT', opt)} – ${fin.toLocaleDateString('it-IT', opt)} ${fin.getFullYear()}`
})

function isToday(d) { return dateToISO(d) === oggi() }
function nomGiorno(d) { return d.toLocaleDateString('it-IT', { weekday: 'short' }).toUpperCase() }

function sposta(n) {
  if (vista.value === 'mese') {
    const d = new Date(dataRef.value + 'T00:00:00'); d.setMonth(d.getMonth() + n)
    dataRef.value = dateToISO(d)
  } else {
    dataRef.value = aggiungiGiorni(dataRef.value, n * nGiorni.value)
  }
}

function vaiOggi() {
  dataRef.value = oggi()
  vista.value = 'giorno'
}

// ── Orari decimali ────────────────────────────────────────────────────────────
function oraDec(hhmm) {
  if (!hhmm) return ORA_INIZIO
  const [h, m] = hhmm.split(':').map(Number)
  return h + (m || 0) / 60
}

// ── Lista eventi filtrati ─────────────────────────────────────────────────────
const eventiFiltrati = computed(() => {
  const list = []
  const ids = slotIdConConflitti.value
  for (const p of prenotazioni.value) {
    if (filtroAula.value && !p.slots?.some(s => !s.annullato && Number(s.aula_id) === Number(filtroAula.value))) continue
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]; if (!slot?.data || slot.annullato) continue
      const oraInizio = slot.ora_inizio?.slice(0, 5) || ''
      const oraFine = slot.ora_fine?.slice(0, 5) || ''
      list.push({
        prenId: p.id, slotIdx: si, aulaId: slot.aula_id, corsoId: slot.corso_id,
        docenteId: slot.docente_id,  // ← AGGIUNTO
        stato: p.stato,
        haConflitti: ids.has(slot.id),
        note: slot.note || '',
        data: slot.data, oraInizio, oraFine,
        _ini: oraDec(oraInizio), _fin: oraDec(oraFine),
      })
    }
  }
  return list
})

const eventiPerData = computed(() => {
  const map = {}
  for (const ev of eventiFiltrati.value) {
    if (!map[ev.data]) map[ev.data] = []
    map[ev.data].push(ev)
  }
  return map
})

// ── Algoritmo anti-overlap ────────────────────────────────────────────────────
function calcolaLayout(eventi) {
  if (!eventi.length) return []
  const sorted = [...eventi].sort((a, b) =>
    a._ini !== b._ini ? a._ini - b._ini : (b._fin - b._ini) - (a._fin - a._ini)
  )
  const columns = []
  const result = sorted.map(ev => {
    let col = columns.findIndex(endTime => endTime <= ev._ini)
    if (col === -1) { col = columns.length; columns.push(0) }
    columns[col] = ev._fin
    return { ...ev, _col: col }
  })
  result.forEach(ev => {
    let maxCol = ev._col
    result.forEach(other => {
      if (other._ini < ev._fin && other._fin > ev._ini) maxCol = Math.max(maxCol, other._col)
    })
    ev._cols = maxCol + 1
  })
  return result
}

const layoutPerData = computed(() => {
  const map = {}
  for (const [data, evs] of Object.entries(eventiPerData.value)) map[data] = calcolaLayout(evs)
  return map
})

function eventiLayoutGiorno(g) { return layoutPerData.value[dateToISO(g)] || [] }
function eventiGiornoMese(g) { return eventiPerData.value[dateToISO(g)] || [] }

function evStyle(ev) {
  const ini = Math.max(ev._ini, ORA_INIZIO)
  const fin = Math.min(ev._fin, ORA_FINE)
  const top = (ini - ORA_INIZIO) * SLOT_H
  const height = Math.max((fin - ini) * SLOT_H - 1, 18)
  const cols = ev._cols || 1, col = ev._col || 0
  const W = 100 / cols
  return {
    position: 'absolute',
    top: `${top}px`,
    height: `${height}px`,
    left: `calc(${col * W}% + ${col > 0 ? GAP : 1}px)`,
    width: `calc(${W}% - ${col > 0 ? GAP : 1}px)`,
    zIndex: col + 1,
    boxSizing: 'border-box',
  }
}

function coloreEvento(ev) {
  if (!ev) return 'cal-ev--confirmed'
  const s = (ev.stato || '').toLowerCase().trim()
  if (s === 'annullata' || s === 'rifiutata' || ev.haConflitti || s === 'conflitto')
    return 'cal-ev--cancelled'
  return 'cal-ev--confirmed'
}

const legenda = [
  { label: 'Confermata', bg: '#d4edda', border: '#198754' },
  { label: 'Conflitto', bg: '#f8d7da', border: '#dc3545' },
]

// ── Caricamento ───────────────────────────────────────────────────────────────
async function caricaDati() {
  loading.value = true
  try {
    let ini, fin
    if (vista.value === 'mese') {
      ini = dateToISO(inizioMese())
      fin = dateToISO(fineMese())
    } else {
      ini = dateToISO(giorniVista.value[0])
      fin = dateToISO(giorniVista.value[giorniVista.value.length - 1])
    }
    const [data, cf] = await Promise.all([
      getCalendario(ini, fin, filtroSede.value || null),
      getConflitti({ solo_attivi: true })
    ])
    prenotazioni.value = Array.isArray(data) ? data : (data?.items || [])
    conflittiAttivi.value = Array.isArray(cf) ? cf : (cf?.items || [])
  } catch (e) {
    console.warn('Calendario:', e.message)
    prenotazioni.value = []
    conflittiAttivi.value = []
  } finally {
    loading.value = false
  }
}

watch([dataRef, filtroSede, vista], caricaDati)

onMounted(async () => {
  if (!route.query.data) {
    filtroSede.value = sedeDefaultFiltro.value
  }
  if (route.query.data) {
    dataRef.value = route.query.data
  }
  aggiornaNow()
  await Promise.all([caricaAule(), caricaCorsi(), caricaDocenti()])  // ← AGGIUNTO caricaDocenti
  const [dataSedi, dataAule] = await Promise.all([getSedi(), getAule()])
  sedi.value = Array.isArray(dataSedi) ? dataSedi : []
  const tutteLeAule = Array.isArray(dataAule) ? dataAule : []
  aule.value = tutteLeAule.filter(a => a.attiva !== false)
  caricaDati()
})
</script>
<style scoped>
.page-title {
  font-size: 1.4rem;
  font-weight: 700;
}

.cal-week {
  overflow-x: auto;
  min-width: 420px;
  display: flex;
  flex-direction: column;
}

.cal-week-header {
  display: grid;
  border-bottom: 2px solid #dee2e6;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
}

.cal-gutter-head {
  border-right: 1px solid #dee2e6;
}

.cal-day-head {
  text-align: center;
  padding: .4rem .2rem;
  border-left: 1px solid #eee;
}

.cal-day-head.is-today {
  background: #eef4ff;
}

.cal-dow {
  display: block;
  font-size: .62rem;
  color: #999;
  font-weight: 700;
  letter-spacing: .04em;
}

.cal-dnum {
  font-size: .9rem;
  font-weight: 700;
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.cal-week-body {
  display: grid;
  overflow-y: auto;
  max-height: 70vh;
}

.cal-gutter {
  border-right: 1px solid #dee2e6;
}

.cal-gutter-slot {
  height: v-bind('SLOT_H + "px"');
  display: flex;
  align-items: flex-start;
  padding-top: 2px;
}

.cal-ora-label {
  font-size: .6rem;
  color: #aaa;
  padding-left: 4px;
  white-space: nowrap;
}

.cal-day-col {
  position: relative;
  border-left: 1px solid #eee;
}

.cal-day-col.is-today {
  background: #f8fbff;
}

.cal-day-col--clickable {
  cursor: pointer;
  transition: background-color 0.2s;
}

.cal-day-col--clickable:hover {
  background-color: #f0f7ff !important;
}

.cal-day-col--clickable.is-today:hover {
  background-color: #e6f2ff !important;
}

.cal-bg-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 0;
  border-top: 1px solid #f0f0f0;
  pointer-events: none;
}

.cal-bg-line--end {
  border-top: 1px solid #dee2e6;
}

.cal-now-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 0;
  border-top: 2px solid #dc3545;
  z-index: 5;
  pointer-events: none;
}

.cal-now-dot {
  position: absolute;
  left: -4px;
  top: -4px;
  width: 8px;
  height: 8px;
  background: #dc3545;
  border-radius: 50%;
}

.cal-ev {
  position: absolute;
  border-radius: 4px;
  padding: 2px 5px;
  font-size: .68rem;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  cursor: default;
  transition: filter .12s, box-shadow .12s;
}

.cal-ev:hover {
  filter: brightness(.9);
  box-shadow: 0 3px 10px rgba(0, 0, 0, .18);
  z-index: 20 !important;
}

.cal-ev-time {
  font-weight: 700;
  font-size: .6rem;
  line-height: 1.3;
  white-space: nowrap;
}

.cal-ev-title {
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cal-ev--confirmed {
  background: #d4edda;
  border-left: 3px solid #198754;
  color: #0d4f2b;
}

.cal-ev--cancelled {
  background: #f8d7da;
  border-left: 3px solid #dc3545;
  color: #5c1a1e;
}

.cal-popover {
  position: absolute;
  width: 260px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, .18);
  z-index: 9999;
  overflow: hidden;
  pointer-events: auto;
  animation: popoverIn .12s ease;
}

@keyframes popoverIn {
  from {
    opacity: 0;
    transform: translateY(4px) scale(.97);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

.cal-popover-header {
  padding: 8px 12px;
  font-size: .82rem;
  display: flex;
  align-items: center;
}

.cal-popover-header.cal-ev--confirmed {
  background: #d4edda;
  color: #0d4f2b;
}

.cal-popover-header.cal-ev--cancelled {
  background: #f8d7da;
  color: #5c1a1e;
}

.cal-popover-body {
  padding: 10px 12px;
  font-size: .82rem;
  line-height: 1.6;
}

.mes-grid {
  overflow-x: auto;
  min-width: 600px;
}

.mes-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.mes-dow {
  padding: .4rem;
  text-align: center;
  font-size: .7rem;
  font-weight: 700;
  color: #888;
  border-bottom: 2px solid #eee;
}

.mes-body {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.mes-cell {
  min-height: 90px;
  border: 1px solid #eee;
  padding: 4px;
  background: #fff;
  overflow: hidden;
}

.mes-cell--clickable {
  cursor: pointer;
  transition: background-color 0.2s;
}

.mes-cell--clickable:hover {
  background-color: #f0f7ff !important;
}

.mes-cell--other {
  background: #f8f9fa;
}

.mes-cell--other .mes-cell-num {
  color: #bbb;
}

.mes-cell--today {
  background: #f0f5ff;
}

.mes-cell--today.mes-cell--clickable:hover {
  background-color: #e6f2ff !important;
}

.mes-cell--weekend {
  background: #fafafa;
}

.mes-cell-num {
  font-size: .78rem;
  font-weight: 700;
  width: 22px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2px;
}

.mes-events {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mes-event {
  border-radius: 3px;
  padding: 1px 4px;
  font-size: .65rem;
  display: flex;
  overflow: hidden;
  cursor: default;
}

.mes-event.cal-ev--confirmed {
  background: #d4edda;
  border-left: 3px solid #198754;
  color: #0d4f2b;
}

.mes-event.cal-ev--cancelled {
  background: #f8d7da;
  border-left: 3px solid #dc3545;
  color: #5c1a1e;
}

.mes-event:hover {
  filter: brightness(.9);
}

.mes-event-more {
  font-size: .6rem;
  color: #888;
  padding-left: 4px;
}
</style>