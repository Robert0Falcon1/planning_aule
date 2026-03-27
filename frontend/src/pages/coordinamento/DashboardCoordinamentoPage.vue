<template>
  <div class="page-dashboard-coord">
    <div class="page-header mb-4">
      <div class="row g-3 align-items-center">
        <!-- Colonna sinistra: Saluto e info -->
        <div class="col-12 col-xl-9">
          <h2 class="page-title">Ciao, {{ auth.nomeUtenteInformale }} 👋</h2>

          <!-- Citazione del giorno -->
          <p class="mb-2">
            <span class="text-primary fw-600"><i>"{{ citazione.quote }}"</i></span>
            <span class="text-muted">({{ citazione.author }})</span>
          </p>

          <p class="text-muted mb-0">Panoramica generale · {{ oggiLabel }}</p>
        </div>

        <!-- Colonna destra: Filtro sede impattante -->
        <div class="col-12 col-xl-3 pt-4 pt-xl-0">
          <div class="filtro-sede-card">
            <div class="">
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
    <!-- KPI row -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.prenotazioniOggi)" color="primary" icon="it-calendar">
          <template #label>
            Prenotazioni oggi
            <span class="info-popover">
              <i class="bi bi-info-circle"></i>
              <span class="popover-content">Prenotazioni del giorno</span>
            </span>
          </template>
        </StatCard>
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.auleOccupateOggi)" color="success" icon="it-check-circle">
          <template #label>
            Aule occupate oggi
            <span class="info-popover">
              <i class="bi bi-info-circle"></i>
              <span class="popover-content">Aule con almeno una prenotazione oggi</span>
            </span>
          </template>
        </StatCard>
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.conflittiAperti)" color="danger" icon="it-warning-circle">
          <template #label>
            Conflitti aperti
            <span class="info-popover">
              <i class="bi bi-info-circle"></i>
              <span class="popover-content">Prenotazioni sovrapposte</span>
            </span>
          </template>
        </StatCard>
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.utentiAttivi)" color="info" icon="it-user">
          <template #label>
            Utenti attivi
            <span class="info-popover">
              <i class="bi bi-info-circle"></i>
              <span class="popover-content">Utenti abilitati ad accedere al sistema</span>
            </span>
          </template>
        </StatCard>
      </div>
    </div>

    <!-- Quick nav -->
    <div class="row g-3 mb-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h5 class="card-title mb-3">Azioni rapide</h5>

            <div class="d-flex flex-wrap gap-2">
              <RouterLink :to="{ name: 'SituazioneOggi' }" class="btn btn-primary">
                <svg class="icon icon-sm me-1">
                  <use :href="sprites + '#it-calendar'"></use>
                </svg>
                Situazione Oggi
              </RouterLink>
              <RouterLink :to="{ name: 'Calendario' }" class="btn btn-outline-secondary">
                <svg class="icon icon-sm me-1">
                  <use :href="sprites + '#it-calendar'"></use>
                </svg>
                Calendario
              </RouterLink>
              <RouterLink :to="{ name: 'Conflitti' }" class="btn btn-outline-danger">
                <svg class="icon icon-sm me-1">
                  <use :href="sprites + '#it-error'"></use>
                </svg>
                Conflitti
              </RouterLink>
              <RouterLink :to="{ name: 'Grafici' }" class="btn btn-outline-primary">
                <svg class="icon icon-sm me-1">
                  <use :href="sprites + '#it-presentation'"></use>
                </svg>
                Grafici & Report
              </RouterLink>
              <RouterLink :to="{ name: 'GestioneSediAule' }" class="btn btn-outline-secondary">
                <svg class="icon icon-sm me-1">
                  <use :href="sprites + '#it-settings'"></use>
                </svg>
                Sedi/Aule
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabella sedi -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center px-0">
        <h5 class="card-title mb-0">Saturazione sedi — oggi</h5>
        <RouterLink :to="{ name: 'SituazioneOggi' }" class="btn btn-sm btn-outline-primary">Dettaglio →</RouterLink>
      </div>
      <div class="card-body p-0">
        <div v-if="loadingSedi" class="text-center py-4">
          <div class="spinner-border spinner-border-sm text-primary"></div>
        </div>
        <div v-else class="table-responsive">
          <table class="table align-middle mb-0 table-hover">
            <thead class="table-light">
              <tr>
                <th>Sede</th>
                <th>Aule totali</th>
                <th>Occupate oggi</th>
                <th>Saturazione</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in saturazioneSedi" :key="s.id">
                <td class="fw-semibold">
                  <svg class="icon icon-primary small">
                    <use :href="sprites + '#it-map-marker'"></use>
                  </svg>
                  {{ s.nome }}
                </td>
                <td>
                  {{ s.totale }}
                </td>
                <td>{{ s.occupate }}</td>
                <td style="min-width:160px">
                  <div class="d-flex align-items-center gap-2">
                    <div class="progress flex-grow-1" style="height:8px">
                      <div class="progress-bar"
                        :class="s.pct >= 80 ? 'bg-danger' : s.pct >= 50 ? 'bg-warning' : 'bg-success'"
                        :style="{ width: s.pct + '%' }"></div>
                    </div>
                    <small class="fw-semibold text-nowrap" style="min-width:40px">{{ s.pct }}%</small>
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
import StatCard from '@/components/ui/StatCard.vue'
import { ref, onMounted, onBeforeUnmount, nextTick, watch, computed } from 'vue'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { getPrenotazioni, getConflitti } from '@/api/prenotazioni'
import { getUtenti } from '@/api/utenti'
import { oggi as isoOggi } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import { useAuthStore } from '@/stores/auth'
import { useCitazioneDelGiorno } from '@/composables/useCitazioneDelGiorno'
import { useSedePerFiltro } from '@/composables/useSedePerFiltro'

const API_CITAZIONI_URL = null
const auth = useAuthStore()
const { sedeDefaultFiltro } = useSedePerFiltro()  // ← ESTRAI DAL COMPOSABLE
const { citazione, loading: loadingCitazione, errore: erroreCitazione } = useCitazioneDelGiorno(
  API_CITAZIONI_URL,
  auth.utente?.id
)

function percentuale(val, tot) {
  if (!tot) return 0
  return Math.round((val / tot) * 100)
}

const oggiLabel = new Date().toLocaleDateString('it-IT', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
}).replace(/\b\w/g, c => c.toUpperCase())

const loadingSedi = ref(false)
const kpi = ref({ prenotazioniOggi: '—', auleOccupateOggi: '—', conflittiAperti: '—', utentiAttivi: '—' })
const saturazioneSedi = ref([])
const sediDisponibili = ref([])
const filtroSede = ref('')
const tuttiIDatiCaricati = ref({})  // Cache dati per evitare ricaricamenti

async function caricaDati() {
  loadingSedi.value = true
  try {
    const dataOggi = isoOggi()

    const [rSedi, rAule, rPren, rUtenti, rConflitti] = await Promise.allSettled([
      getSedi(),
      getAule(),
      getPrenotazioni({ data_dal: dataOggi, data_al: dataOggi }),
      getUtenti(),
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
    const utentiList = val(rUtenti)
    const conflList = val(rConflitti)

    // Salva dati in cache
    tuttiIDatiCaricati.value = {
      sediList,
      auleList,
      prenList,
      utentiList,
      conflList,
      dataOggi
    }

    sediDisponibili.value = sediList

    const slotOggi = []
    for (const p of prenList) {
      for (const s of (p.slots || [])) {
        if (s.data === dataOggi && !s.annullato) slotOggi.push({ ...s })
      }
    }

    kpi.value = {
      prenotazioniOggi: slotOggi.length,
      auleOccupateOggi: new Set(slotOggi.map(s => s.aula_id)).size,
      conflittiAperti: conflList.length,
      utentiAttivi: utentiList.filter(u => u.attivo).length,
    }

    applicaFiltroSede()
  } catch (e) {
    console.warn('DashboardCoord:', e.message)
  } finally {
    loadingSedi.value = false
  }
}

function applicaFiltroSede() {
  const { sediList, auleList, prenList, utentiList, conflList, dataOggi } = tuttiIDatiCaricati.value
  if (!sediList) return

  // Filtra aule in base alla sede selezionata
  const auleFiltrate = filtroSede.value
    ? auleList.filter(a => a.sede_id === Number(filtroSede.value))
    : auleList

  const aulaIdsFiltrate = new Set(auleFiltrate.map(a => a.id))

  // Filtra slot per aule della sede selezionata
  const slotOggi = []
  const slotIdsFiltratiSet = new Set()

  for (const p of prenList) {
    for (const s of (p.slots || [])) {
      if (s.data === dataOggi && !s.annullato && aulaIdsFiltrate.has(s.aula_id)) {
        slotOggi.push({ ...s })
        slotIdsFiltratiSet.add(s.id)
      }
    }
  }

  // Filtra conflitti per slot della sede selezionata
  const conflittiFiltrati = conflList.filter(cf =>
    slotIdsFiltratiSet.has(cf.slot_id_1) || slotIdsFiltratiSet.has(cf.slot_id_2)
  )

  // ← AGGIORNA KPI FILTRATI
  kpi.value = {
    prenotazioniOggi: slotOggi.length,
    auleOccupateOggi: new Set(slotOggi.map(s => s.aula_id)).size,
    conflittiAperti: conflittiFiltrati.length,
    utentiAttivi: utentiList.filter(u => u.attivo).length,  // Rimane globale
  }

  // Tabella saturazione sedi
  const sediDaMostrare = filtroSede.value
    ? sediList.filter(s => s.id === Number(filtroSede.value))
    : sediList

  saturazioneSedi.value = sediDaMostrare.map(sede => {
    const auleS = auleList.filter(a => a.sede_id === sede.id)
    const aulaIds = new Set(auleS.map(a => a.id))
    const occupate = new Set(slotOggi.filter(s => aulaIds.has(s.aula_id)).map(s => s.aula_id)).size
    return {
      id: sede.id,
      nome: sede.nome,
      totale: auleS.length,
      occupate,
      pct: percentuale(occupate, auleS.length),
    }
  })
}

watch(filtroSede, () => {
  applicaFiltroSede()
})

onMounted(async () => {
  // Inizializza filtro con sede utente
  filtroSede.value = sedeDefaultFiltro.value

  await caricaDati()

  await nextTick()
  const popoverElements = document.querySelectorAll('[data-bs-toggle="popover"]')
  if (popoverElements.length > 0) {
    if (window.bootstrap?.Popover) {
      popoverElements.forEach(el => {
        new window.bootstrap.Popover(el)
      })
    } else {
      import('bootstrap-italia/dist/js/bootstrap-italia.bundle.min.js').then(() => {
        setTimeout(() => {
          if (window.bootstrap?.Popover) {
            popoverElements.forEach(el => {
              new window.bootstrap.Popover(el)
            })
          }
        }, 100)
      })
    }
  }
})

onBeforeUnmount(() => {
  const popoverElements = document.querySelectorAll('[data-bs-toggle="popover"]')
  popoverElements.forEach(el => {
    const instance = window.bootstrap?.Popover?.getInstance(el)
    if (instance) instance.dispose()
  })
})
</script>


<style scoped>
.page-title {
  font-size: 1.5rem;
  font-weight: 700;
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