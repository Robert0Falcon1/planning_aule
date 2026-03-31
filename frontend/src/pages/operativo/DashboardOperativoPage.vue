<template>
  <div class="page-operativo">
    <div class="page-header mb-4">
      <div class="row g-3">
        <!-- Colonna sinistra: Saluto e info -->
        <div class="col-12 col-lg-7">
          <h2 class="page-title">Ciao, {{ auth.nomeUtenteInformale }} 👋</h2>
          <!-- Citazione del giorno -->
          <p class="mb-2">
            <span class="text-primary fw-600"><i>"{{ citazione.quote }}"</i></span>
            <span class="text-muted">({{ citazione.author }})</span>
          </p>
          <p class="text-muted mb-0">Riepilogo di oggi — <span class="fw-600 text-primary">{{ oggiLabel }}</span>:</p>
        </div>
        <!-- Colonna destra: Filtro sede impattante -->
        <div class="col-12 col-lg-5">
          <div class="filtro-sede-card">
            <div class="d-flex align-items-center gap-2 mb-2">
              <span class="text-muted">Visualizzazione dati</span>
            </div>
            <select v-model="filtroSede" class="form-select form-select-lg sede-select custom-select">
              <option value="">Tutte le sedi</option>
              <option v-for="s in sediDisponibili" :key="s.id" :value="s.id">
                {{ s.nome }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <!-- KPI -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.totali)" color="primary" icon="it-calendar">
          <template #label>
            Prenotazioni totali
            <span class="info-popover">
              <i class="bi bi-info-circle"></i>
              <span class="popover-content">Tutte le mie prenotazioni</span>
            </span>
          </template>
        </StatCard>
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.oggi)" color="success" icon="it-check-circle">
          <template #label>
            Prenotazioni oggi
            <span class="info-popover">
              <i class="bi bi-info-circle"></i>
              <span class="popover-content">Mie prenotazioni del giorno</span>
            </span>
          </template>
        </StatCard>
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.conflitti)" color="danger" icon="it-warning-circle">
          <template #label>
            Conflitti
            <span class="info-popover">
              <i class="bi bi-info-circle"></i>
              <span class="popover-content">Prenotazioni sovrapposte</span>
            </span>
          </template>
        </StatCard>
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.prossimi7)" color="info" icon="it-user">
          <template #label>
            Prenotazioni prossimi 7 gg
            <span class="info-popover">
              <i class="bi bi-info-circle"></i>
              <span class="popover-content">Mie prenotazioni<br>prossima settimana</span>
            </span>
          </template>
        </StatCard>
      </div>
    </div>
    <!-- Azioni rapide -->
    <div class="row g-3 mb-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h5 class="card-title mb-3">Azioni rapide</h5>
            <div class="d-flex flex-wrap gap-2">
              <RouterLink :to="{ name: 'NuovaPrenotazione' }" class="btn btn-primary">
                <svg class="icon icon-white icon-sm me-1">
                  <use :href="sprites + '#it-plus-circle'"></use>
                </svg>
                Nuova prenotazione
              </RouterLink>
              <RouterLink :to="{ name: 'Calendario' }" class="btn btn-outline-secondary">
                <svg class="icon icon-sm me-1">
                  <use :href="sprites + '#it-calendar'"></use>
                </svg>
                Calendario
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Ultimi slot + prossimi -->
    <div class="row g-3">
      <div class="col-12 col-xl-8">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 pb-0 d-flex justify-content-between align-items-center mb-3">
            <h5 class="card-title mb-0">Prenotazioni passate</h5>
            <RouterLink :to="{ name: 'MiePrenotazioni' }" class="btn btn-sm btn-outline-primary">
              Vedi tutte
            </RouterLink>
          </div>
          <div class="card-body pt-2">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
            <div v-else-if="!ultimi.length" class="text-muted text-center py-4">
              Nessuna tua prenotazione trovata.
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover table-sm align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Data</th>
                    <th>Orario</th>
                    <th>Aula</th>
                    <th>Corso</th>
                    <th>Conflitto</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="s in ultimi" :key="s.key" :class="{ 'table-danger': s.haConflitti }">
                    <td class="fw-semibold">
                      <svg class="icon icon-xs me-1">
                        <use :href="sprites + '#it-calendar'"></use>
                      </svg>
                      {{ formatData(s.data) }}
                    </td>
                    <td class="text-nowrap">
                      <svg class="icon icon-xs me-1">
                        <use :href="sprites + '#it-clock'"></use>
                      </svg>
                      {{ s.oraInizio }} – {{ s.oraFine }}
                    </td>
                    <td>
                      <span class="aula-dot" :style="getAulaBadgeStyle(nomeAulaFn(s.aulaId))"></span>
                      <span class="small fw-semibold">{{ nomeAulaFn(s.aulaId) }}</span><br>
                      <small class="text-muted">{{ sedeDiAulaFn(s.aulaId) }}</small>
                    </td>
                    <td>
                      <svg class="icon icon-xs me-1">
                        <use :href="sprites + '#it-bookmark'"></use>
                      </svg>
                      <span class="small">{{ getTitoloCorso(s.corsoId) }}</span>
                    </td>
                    <td>
                      <span v-if="s.haConflitti" class="badge bg-danger">Sì</span>
                      <span v-else class="text-muted small">—</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-xl-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 pb-0">
            <h5 class="card-title mb-0">Prossimi 7 giorni</h5>
          </div>
          <div class="card-body pt-2">
            <div v-if="loading" class="text-center py-3">
              <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
            </div>
            <div v-else-if="!prossimi.length" class="text-muted small text-center py-3">
              Nessuna tua prenotazione nei prossimi 7 giorni.
            </div>
            <ul v-else class="list-unstyled mb-0">
              <li v-for="s in prossimi" :key="s.key" class="d-flex align-items-start gap-2 px-3 py-3 border-bottom"
                :class="{ 'bg-danger bg-opacity-10': s.haConflitti }">
                <div class="d-flex flex-column justify-content-center">
                  <div class="d-flex justify-content-center">
                    <div class="cal-badge text-center flex-shrink-0 mb-2"
                      :style="s.haConflitti ? 'background:#dc3545' : ''">
                      <span class="cal-badge-day pt-2">{{ new Date(s.data + 'T00:00:00').getDate() }}</span>
                      <span class="cal-badge-month">{{ meseBreve(s.data) }}</span>
                    </div>
                  </div>
                  <span v-if="s.haConflitti"
                    class="badge bg-danger align-self-center flex-shrink-0 d-flex justify-content-center align-items-center">
                    <svg class="icon icon-xs icon-white mx-1">
                      <use :href="sprites + '#it-error'"></use>
                    </svg>
                  </span>
                </div>
                <div class="small overflow-hidden flex-grow-1">
                  <div class="fw-semibold text-truncate">
                    <span class="aula-dot" :style="getAulaBadgeStyle(nomeAulaFn(s.aulaId))"></span>
                    {{ nomeAulaFn(s.aulaId) }}<br>
                    <span class="text-muted">{{ sedeDiAulaFn(s.aulaId) }}</span>
                  </div>
                  <div class="text-muted">{{ s.oraInizio }} – {{ s.oraFine }}</div>
                  <div class="text-muted">{{ getTitoloCorso(s.corsoId) }}</div>
                </div>
              </li>
            </ul>
            <RouterLink :to="{ name: 'Calendario' }" class="btn btn-outline-primary btn-sm mt-3 w-100">
              <svg class="icon icon-sm me-1">
                <use :href="sprites + '#it-calendar'"></use>
              </svg>
              Apri Calendario
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import StatCard from '@/components/ui/StatCard.vue'
import { getMiePrenotazioni, getConflitti } from '@/api/prenotazioni'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { useAule } from '@/composables/useAule'
import { useCorsi } from '@/composables/useCorsi'
import { useCitazioneDelGiorno } from '@/composables/useCitazioneDelGiorno'
import { useSedePerFiltro } from '@/composables/useSedePerFiltro'
import { formatData, oggi, aggiungiGiorni } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import { useAulaColor } from '@/composables/useAulaColor'

const auth = useAuthStore()
const { sedeDefaultFiltro } = useSedePerFiltro()
const loading = ref(false)
const prenotazioni = ref([])
const conflittiAttivi = ref([])
const sediDisponibili = ref([])
const filtroSede = ref('')
const tuttiIDatiCaricati = ref({})

const { getAulaBadgeStyle } = useAulaColor()
const { nomeAula: nomeAulaFn, sedeDiAula: sedeDiAulaFn, carica: caricaAule } = useAule()
const { caricaCorsi, getTitoloCorso } = useCorsi()

const API_CITAZIONI_URL = null
const { citazione, loading: citazioneLoading, errore: citazioneErrore } = useCitazioneDelGiorno(
  API_CITAZIONI_URL,
  auth.utente?.id
)

const oggiISO = oggi()
const fra7 = aggiungiGiorni(oggiISO, 7)
const oggiLabel = new Date().toLocaleDateString('it-IT', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
}).replace(/\b\w/g, c => c.toUpperCase())

function meseBreve(isoDate) {
  return new Date(isoDate + 'T00:00:00').toLocaleDateString('it-IT', { month: 'short' }).toUpperCase()
}

const slotIdConConflitti = computed(() => {
  const s = new Set()
  for (const cf of conflittiAttivi.value) {
    if (cf.slot_id_1) s.add(cf.slot_id_1)
    if (cf.slot_id_2) s.add(cf.slot_id_2)
  }
  return s
})

const miePrenotazioneIds = computed(() => new Set(prenotazioni.value.map(p => p.id)))

const conteggioConflitti = computed(() =>
  conflittiAttivi.value.filter(cf =>
    miePrenotazioneIds.value.has(cf.prenotazione_id_1) ||
    miePrenotazioneIds.value.has(cf.prenotazione_id_2)
  ).length
)

const tuttiSlot = ref([])

const ultimi = computed(() =>
  tuttiSlot.value.filter(s => s.data <= oggiISO).slice(0, 8)
)

const prossimi = computed(() =>
  tuttiSlot.value
    .filter(s => s.data > oggiISO && s.data <= fra7)
    .sort((a, b) => a.data.localeCompare(b.data))
    .slice(0, 10)
)

const kpi = computed(() => ({
  totali: tuttiSlot.value.length,
  oggi: tuttiSlot.value.filter(s => s.data === oggiISO).length,
  conflitti: conteggioConflitti.value,
  prossimi7: prossimi.value.length,
}))

async function caricaDati() {
  loading.value = true
  try {
    const [rSedi, rAule, rPren, rConflitti] = await Promise.allSettled([
      getSedi(),
      getAule(),
      getMiePrenotazioni(),
      getConflitti({ solo_attivi: true }),
    ])

    function val(r) {
      if (r.status !== 'fulfilled') return []
      const v = r.value
      if (Array.isArray(v)) return v
      if (v?.items) return v.items
      return []
    }

    const sediList = val(rSedi)
    const auleList = val(rAule)
    const prenList = val(rPren)
    const conflList = val(rConflitti)

    tuttiIDatiCaricati.value = {
      sediList,
      auleList,
      prenList,
      conflList
    }

    sediDisponibili.value = sediList
    prenotazioni.value = prenList
    conflittiAttivi.value = conflList

    applicaFiltroSede()
  } catch (e) {
    console.warn('DashboardOperativo:', e.message)
  } finally {
    loading.value = false
  }
}

function applicaFiltroSede() {
  const { auleList, prenList } = tuttiIDatiCaricati.value
  if (!auleList) return

  const auleFiltrate = filtroSede.value
    ? auleList.filter(a => a.sede_id === Number(filtroSede.value))
    : auleList

  const aulaIdsFiltrate = new Set(auleFiltrate.map(a => a.id))

  const ids = slotIdConConflitti.value
  const list = []
  for (const p of prenList) {
    if (!auth.isCoordinamento && auth.utente?.id && p.richiedente_id !== auth.utente.id) continue
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]
      if (!slot?.data || slot.annullato) continue
      if (!aulaIdsFiltrate.has(slot.aula_id)) continue
      list.push({
        key: `${p.id}-${si}`,
        prenId: p.id,
        slotId: slot.id,
        aulaId: slot.aula_id,
        corsoId: slot.corso_id,
        haConflitti: ids.has(slot.id),
        data: slot.data,
        oraInizio: slot.ora_inizio?.slice(0, 5) || '—',
        oraFine: slot.ora_fine?.slice(0, 5) || '—',
      })
    }
  }
  tuttiSlot.value = list.sort((a, b) => b.data.localeCompare(a.data))
}

watch(filtroSede, () => {
  applicaFiltroSede()
})

onMounted(async () => {
  await Promise.all([caricaAule(), caricaCorsi()])
  filtroSede.value = sedeDefaultFiltro.value
  await caricaDati()
})
</script>

<style scoped>
.page-title {
  font-size: 1.5rem;
  font-weight: 700;
}

/* Citazione del giorno */
.citazione-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #e8f0fe 100%);
  border-left: 4px solid #0066cc;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-top: 1rem;
}

.citazione-text {
  color: #0073e6;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.citazione-author {
  color: #5a6772;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0;
  text-align: right;
}

.cal-badge {
  background: #0066cc;
  color: #fff;
  border-radius: 6px;
  padding: 4px 8px;
  min-width: 38px;
}

.cal-badge-day {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  line-height: 1;
}

.cal-badge-month {
  display: block;
  font-size: .6rem;
  font-weight: 600;
  opacity: .85;
}

.kpi-card {
  border-radius: 12px;
}

.kpi-value {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1;
}

.kpi-label {
  font-size: .8rem;
  color: #666;
  margin-top: .25rem;
}
</style>