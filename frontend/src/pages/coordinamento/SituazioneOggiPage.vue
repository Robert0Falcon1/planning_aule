<template>
  <div class="page-situazione">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Situazione Oggi</h2>
      <div class="ms-auto d-flex gap-2 flex-wrap align-items-center">
        <button class="btn" @click="spostaGiorno(-1)">
          <svg class="icon icon-sm">
            <use :href="sprites + '#it-chevron-left'"></use>
          </svg>
        </button>
        <input v-model="dataSelezionata" type="date" class="form-control form-control-sm" style="width:auto"
          @change="carica" />
        <button class="btn" @click="spostaGiorno(1)">
          <svg class="icon icon-sm">
            <use :href="sprites + '#it-chevron-right'"></use>
          </svg>
        </button>
        <button class="btn btn-sm btn-outline-primary" @click="dataSelezionata = oggiISO; carica()">Oggi</button>
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="carica">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>
      </div>
    </div>

    <!-- KPI -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-md-4">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-primary">{{ slotDelGiorno.length }}</div>
          <div class="small text-muted">Prenotazioni totali</div>
        </div>
      </div>
      <div class="col-6 col-md-4">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-success">{{ confermate }}</div>
          <div class="small text-muted">Confermate</div>
        </div>
      </div>
      <div class="col-6 col-md-4">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-info">{{ auleOccupate }}</div>
          <div class="small text-muted">Aule occupate</div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>
    <div v-else>
      <!-- Raggruppa per sede tramite useAule -->
      <div v-for="gruppo in sediConSlot" :key="gruppo.sedeId" class="mb-4">
        <h5 class="fw-bold text-primary mb-2">
          <svg class="icon icon-primary icon-sm me-1">
            <use :href="sprites + '#it-map-marker'"></use>
          </svg>
          {{ gruppo.sedeNome }}
          <span class="badge bg-primary-subtle text-primary ms-2 fw-normal">{{ gruppo.slots.length }}
            Prenotazioni</span>
        </h5>
        <div class="card border-0 shadow-sm">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 table-sm">
              <thead class="table-light">
                <tr>
                  <th>Aula</th>
                  <th>Corso&nbsp;ID</th>
                  <th>Orario</th>
                  <th>Stato</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="slot in gruppo.slots" :key="slot.prenId + '-' + slot.slotIdx">
                  <td class="fw-semibold">
                    <div class="d-flex align-items-center gap-1">
                      <span :style="getAulaBadgeStyle(nomeAulaFn(slot.aulaId))"></span>
                      {{ nomeAulaFn(slot.aulaId) }}
                    </div>
                  </td>
                  <td><code class="small">{{ slot.corsoId }}</code></td>
                  <td class="text-nowrap">{{ slot.oraInizio }} – {{ slot.oraFine }}</td>
                  <td>
                    <span class="badge" :class="badgeStato(slot)">{{ statoLabel(slot) }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-if="!sediConSlot.length" class="card border-0 shadow-sm">
        <div class="card-body text-center text-muted py-5">
          Nessuna prenotazione per {{ dataSelezionata }}{{ filtroSede ? ' in questa sede' : '' }}.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSedi } from '@/api/sedi'
import { getPrenotazioni, getConflitti } from '@/api/prenotazioni'
import { useAule } from '@/composables/useAule'
import { useAulaColor } from '@/composables/useAulaColor'
import { oggi, aggiungiGiorni } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading = ref(false)
const sedi = ref([])
const prenotazioni = ref([])
const conflittiAttivi = ref([])
const oggiISO = oggi()
const dataSelezionata = ref(oggiISO)
const filtroSede = ref('')

const { nomeAula: nomeAulaFn, sedeDiAula, carica: caricaAule } = useAule()
const { getAulaBadgeStyle } = useAulaColor()

// Set di slot_id con conflitti NON_RISOLTO
const slotIdConConflitti = computed(() => {
  const s = new Set()
  for (const cf of conflittiAttivi.value) {
    if (cf.slot_id_1) s.add(cf.slot_id_1)
    if (cf.slot_id_2) s.add(cf.slot_id_2)
  }
  return s
})

// ── Espande prenotazioni in slot per la data selezionata ──────────────────────
const slotDelGiorno = computed(() => {
  const ids = slotIdConConflitti.value
  const list = []
  for (const p of prenotazioni.value) {
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]
      if (slot?.data !== dataSelezionata.value) continue
      list.push({
        prenId: p.id,
        slotIdx: si,
        slotId: slot.id,
        aulaId: slot.aula_id,
        corsoId: slot.corso_id,
        tipo: p.tipo,
        stato: p.stato,
        haConflitti: ids.has(slot.id),
        oraInizio: slot.ora_inizio?.slice(0, 5) || '—',
        oraFine: slot.ora_fine?.slice(0, 5) || '—',
      })
    }
  }
  return list.sort((a, b) => a.oraInizio.localeCompare(b.oraInizio))
})

// KPI
const confermate = computed(() => slotDelGiorno.value.filter(s => !s.haConflitti && s.stato === 'confermata').length)
const auleOccupate = computed(() => new Set(slotDelGiorno.value.filter(s => s.stato === 'confermata').map(s => s.aulaId)).size)

// Raggruppa per sede usando sedeDiAula dal composable
const sediConSlot = computed(() => {
  const map = {}
  for (const slot of slotDelGiorno.value) {
    const sedeNome = sedeDiAula(slot.aulaId)
    const sedeKey = sedeNome
    if (!map[sedeKey]) map[sedeKey] = { sedeId: sedeKey, sedeNome, slots: [] }
    map[sedeKey].slots.push(slot)
  }
  return Object.values(map).sort((a, b) => a.sedeNome.localeCompare(b.sedeNome))
})

function badgeStato(slot) {
  if (slot.haConflitti) return 'bg-danger'
  
  return {
    confermata: 'bg-success',
    in_attesa: 'bg-warning text-dark',
    rifiutata: 'bg-danger',
    annullata: 'bg-secondary',
  }[slot.stato] || 'bg-secondary'
}

function statoLabel(slot) {
  return slot.haConflitti ? 'conflitto' : slot.stato
}

function spostaGiorno(n) {
  dataSelezionata.value = aggiungiGiorni(dataSelezionata.value, n)
  carica()
}

async function carica() {
  loading.value = true
  try {
    const [dataPren, dataConflitti] = await Promise.all([
      getPrenotazioni({
        data_dal: dataSelezionata.value,
        data_al: dataSelezionata.value,
        ...(filtroSede.value ? { sede_id: filtroSede.value } : {}),
      }),
      getConflitti({ solo_attivi: true })
    ])
    prenotazioni.value = Array.isArray(dataPren) ? dataPren : (dataPren?.items || [])
    conflittiAttivi.value = Array.isArray(dataConflitti) ? dataConflitti : (dataConflitti?.items || [])
  } catch (e) {
    console.warn('SituazioneOggi:', e.message)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await caricaAule()
  const data = await getSedi()
  sedi.value = Array.isArray(data) ? data : []
  carica()
})
</script>

<style scoped>
.page-title {
  font-size: 1.4rem;
  font-weight: 700;
}
</style>