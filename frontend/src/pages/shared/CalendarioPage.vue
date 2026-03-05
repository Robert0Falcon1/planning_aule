<template>
  <div class="page-calendario">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Calendario</h2>
      <div class="ms-auto d-flex gap-2 align-items-center flex-wrap">
        <button class="btn btn-outline-secondary btn-sm" @click="spostaSettimana(-1)">
          <svg class="icon icon-sm"><use :href="sprites + '#it-chevron-left'"></use></svg>
        </button>
        <span class="fw-semibold px-2">{{ labelSettimana }}</span>
        <button class="btn btn-outline-secondary btn-sm" @click="spostaSettimana(1)">
          <svg class="icon icon-sm"><use :href="sprites + '#it-chevron-right'"></use></svg>
        </button>
        <button class="btn btn-outline-primary btn-sm" @click="vaiOggi">Oggi</button>
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>
        <RouterLink :to="{ name: 'NuovaPrenotazione' }" class="btn btn-primary btn-sm">
          <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
          Nuova
        </RouterLink>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div class="cal-grid">
          <!-- Header giorni -->
          <div class="cal-header">
            <div class="cal-time-col"></div>
            <div v-for="(g, i) in giorniSettimana" :key="i"
              class="cal-day-header" :class="{ 'cal-day-today': isToday(g) }">
              <span class="cal-day-name">{{ nomGiorno(g) }}</span>
              <span class="cal-day-num" :class="{ 'badge bg-primary rounded-circle': isToday(g) }">
                {{ g.getDate() }}
              </span>
            </div>
          </div>

          <!-- Righe ore -->
          <div class="cal-body">
            <div v-for="ora in oreGiornata" :key="ora" class="cal-row">
              <div class="cal-time-label">{{ String(ora).padStart(2,'0') }}:00</div>
              <div v-for="(g, gi) in giorniSettimana" :key="gi"
                class="cal-cell" :class="{ 'cal-cell-today': isToday(g) }">
                <div v-for="ev in eventiCella(g, ora)" :key="ev.prenId + '-' + ev.slotIdx"
                  class="cal-event" :class="coloreEvento(ev.stato)"
                  :title="`Prenotazione #${ev.prenId} — Aula ${ev.aulaId} — Corso ${ev.corsoId}`">
                  <span class="cal-event-time">{{ ev.oraInizio }}–{{ ev.oraFine }}</span>
                  <span class="cal-event-title">Aula {{ ev.aulaId }}</span>
                  <span class="cal-event-room">Corso {{ ev.corsoId }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legenda -->
    <div class="d-flex gap-3 mt-3 flex-wrap">
      <span class="d-flex align-items-center gap-1 small">
        <span style="width:12px;height:12px;background:#d4edda;border-left:3px solid #198754;display:inline-block;border-radius:2px"></span>
        Confermata
      </span>
      <span class="d-flex align-items-center gap-1 small">
        <span style="width:12px;height:12px;background:#fff3cd;border-left:3px solid #ffc107;display:inline-block;border-radius:2px"></span>
        In attesa
      </span>
      <span class="d-flex align-items-center gap-1 small">
        <span style="width:12px;height:12px;background:#f8d7da;border-left:3px solid #dc3545;display:inline-block;border-radius:2px"></span>
        Conflitto / Annullata
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getSedi } from '@/api/sedi'
import { getCalendario } from '@/api/prenotazioni'
import { oggi, aggiungiGiorni, inizioSettimana } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading    = ref(false)
const filtroSede = ref('')
const sedi       = ref([])
const prenotazioni = ref([])   // lista grezza dal backend
const dataRef    = ref(oggi())

// ── Griglia settimana ────────────────────────────────────────────────────────

const giorniSettimana = computed(() => {
  const lun = new Date(inizioSettimana(dataRef.value) + 'T00:00:00')
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(lun); d.setDate(lun.getDate() + i); return d
  })
})

const oreGiornata = Array.from({ length: 13 }, (_, i) => i + 7) // 07–19

const labelSettimana = computed(() => {
  const ini = giorniSettimana.value[0]
  const fin = giorniSettimana.value[6]
  const opt = { day: 'numeric', month: 'short' }
  return `${ini.toLocaleDateString('it-IT', opt)} – ${fin.toLocaleDateString('it-IT', opt)} ${fin.getFullYear()}`
})

function isToday(d)   { return d.toISOString().slice(0, 10) === oggi() }
function nomGiorno(d) { return d.toLocaleDateString('it-IT', { weekday: 'short' }).toUpperCase() }
function spostaSettimana(n) { dataRef.value = aggiungiGiorni(dataRef.value, n * 7) }
function vaiOggi() { dataRef.value = oggi() }

// ── Espandi prenotazioni in eventi per cella ─────────────────────────────────
// Ogni prenotazione ha slots: [{ data, ora_inizio, ora_fine }]
// Generiamo un evento per ogni slot, indicizzato per (data, ora)

const eventiPerData = computed(() => {
  const map = {}  // key: "YYYY-MM-DD|HH" → array eventi
  for (const p of prenotazioni.value) {
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]
      if (!slot?.data) continue
      const ora = parseInt(slot.ora_inizio?.slice(0, 2) || '0')
      const key = `${slot.data}|${ora}`
      if (!map[key]) map[key] = []
      map[key].push({
        prenId:    p.id,
        slotIdx:   si,
        aulaId:    p.aula_id,
        corsoId:   p.corso_id,
        stato:     p.stato,
        oraInizio: slot.ora_inizio?.slice(0, 5) || '',
        oraFine:   slot.ora_fine?.slice(0, 5)   || '',
      })
    }
  }
  return map
})

function eventiCella(giorno, ora) {
  const dataStr = giorno.toISOString().slice(0, 10)
  return eventiPerData.value[`${dataStr}|${ora}`] || []
}

function coloreEvento(stato) {
  if (stato === 'confermata') return 'cal-event--confirmed'
  if (stato === 'in_attesa')  return 'cal-event--pending'
  return 'cal-event--cancelled'
}

// ── Caricamento ──────────────────────────────────────────────────────────────

async function caricaDati() {
  loading.value = true
  try {
    const ini  = giorniSettimana.value[0].toISOString().slice(0, 10)
    const fin  = giorniSettimana.value[6].toISOString().slice(0, 10)
    const data = await getCalendario(ini, fin, filtroSede.value || null)
    prenotazioni.value = Array.isArray(data) ? data : (data?.items || [])
  } catch (e) {
    console.warn('Calendario:', e.message)
    prenotazioni.value = []
  } finally {
    loading.value = false
  }
}

watch([dataRef, filtroSede], caricaDati)

onMounted(async () => {
  const data = await getSedi()
  sedi.value = Array.isArray(data) ? data : []
  caricaDati()
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
.cal-grid { overflow-x: auto; min-width: 700px; }
.cal-header, .cal-row {
  display: grid;
  grid-template-columns: 52px repeat(7, 1fr);
  border-bottom: 1px solid #eee;
}
.cal-day-header {
  padding: .5rem .25rem; text-align: center; border-left: 1px solid #eee;
}
.cal-day-header.cal-day-today { background: #eef4ff; }
.cal-day-name { display: block; font-size: .65rem; color: #999; font-weight: 600; }
.cal-day-num  { font-size: .9rem; font-weight: 700; width: 28px; height: 28px;
  display: inline-flex; align-items: center; justify-content: center; }
.cal-time-col { border-right: 1px solid #eee; }
.cal-time-label {
  padding: .25rem .3rem; font-size: .65rem; color: #999;
  border-right: 1px solid #eee; white-space: nowrap; line-height: 1;
}
.cal-cell {
  min-height: 48px; border-left: 1px solid #eee; padding: 2px; vertical-align: top;
}
.cal-cell-today { background: #f7f9ff; }
.cal-event {
  border-radius: 4px; padding: 2px 5px; margin-bottom: 2px;
  font-size: .68rem; display: flex; flex-direction: column; overflow: hidden;
  cursor: default;
}
.cal-event--confirmed { background: #d4edda; border-left: 3px solid #198754; color: #0d4f2b; }
.cal-event--pending   { background: #fff3cd; border-left: 3px solid #ffc107; color: #664d03; }
.cal-event--cancelled { background: #f8d7da; border-left: 3px solid #dc3545; color: #5c1a1e; }
.cal-event-time  { font-weight: 600; }
.cal-event-title { font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cal-event-room  { opacity: .7; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>