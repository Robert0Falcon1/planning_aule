<template>
  <div class="page-dashboard-coord">
    <div class="page-header mb-4">
      <h2 class="page-title">Dashboard Coordinamento</h2>
      <p class="text-muted mb-0">Panoramica generale · {{ oggi }}</p>
    </div>

    <!-- KPI row -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3">
        <div class="card border-0 shadow-sm kpi-card">
          <div class="card-body">
            <div class="kpi-value text-primary">{{ kpi.prenotazioniOggi }}</div>
            <div class="kpi-label">Prenotazioni oggi</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card border-0 shadow-sm kpi-card">
          <div class="card-body">
            <div class="kpi-value text-success">{{ kpi.auleOccupateOggi }}</div>
            <div class="kpi-label">Aule occupate oggi</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card border-0 shadow-sm kpi-card">
          <div class="card-body">
            <div class="kpi-value text-warning">{{ kpi.conflittiAperti }}</div>
            <div class="kpi-label">Conflitti aperti</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card border-0 shadow-sm kpi-card">
          <div class="card-body">
            <div class="kpi-value text-info">{{ kpi.utentiAttivi }}</div>
            <div class="kpi-label">Utenti attivi</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick nav -->
    <div class="row g-3 mb-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h5 class="card-title mb-3">Accesso rapido</h5>
            <div class="d-flex flex-wrap gap-2">
              <RouterLink :to="{ name: 'SituazioneOggi' }" class="btn btn-outline-primary">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-calendar'"></use></svg>
                Situazione Oggi
              </RouterLink>
              <RouterLink :to="{ name: 'Grafici' }" class="btn btn-outline-primary">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-presentation'"></use></svg>
                Grafici & Report
              </RouterLink>
              <RouterLink :to="{ name: 'GestioneUtenti' }" class="btn btn-outline-secondary">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-user'"></use></svg>
                Gestione Utenti
              </RouterLink>
              <RouterLink :to="{ name: 'GestioneSediAule' }" class="btn btn-outline-secondary">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-settings'"></use></svg>
                Gestione Sedi/Aule
              </RouterLink>
              <RouterLink :to="{ name: 'Conflitti' }" class="btn btn-outline-danger">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-error'"></use></svg>
                Conflitti
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabella sedi -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
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
                <td class="fw-semibold">{{ s.nome }}</td>
                <td>{{ s.totale }}</td>
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
import { ref, onMounted } from 'vue'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { getPrenotazioni, getConflitti } from '@/api/prenotazioni'
import { getUtenti } from '@/api/utenti'
import { oggi as isoOggi } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

function percentuale(val, tot) {
  if (!tot) return 0
  return Math.round((val / tot) * 100)
}

const oggi        = new Date().toLocaleDateString('it-IT', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
const loadingSedi = ref(false)
const kpi         = ref({ prenotazioniOggi: '—', auleOccupateOggi: '—', conflittiAperti: '—', utentiAttivi: '—' })
const saturazioneSedi = ref([])

onMounted(async () => {
  loadingSedi.value = true
  try {
    const dataOggi = isoOggi()

    // Promise.allSettled: ogni risultato è { status, value } oppure { status, reason }
    const [rSedi, rAule, rPren, rUtenti, rConflitti] = await Promise.allSettled([
      getSedi(),
      getAule(),
      getPrenotazioni({ data_dal: dataOggi, data_al: dataOggi }),
      getUtenti(),
      getConflitti({ solo_attivi: true }),
    ])

    // Estrai .value solo se fulfilled, altrimenti array vuoto
    function val(r) {
      if (r.status !== 'fulfilled') return []
      const v = r.value
      if (Array.isArray(v)) return v
      if (v?.items) return v.items
      return []
    }

    const sediList   = val(rSedi)
    const auleList   = val(rAule)
    const prenList   = val(rPren)
    const utentiList = val(rUtenti)
    const conflList  = val(rConflitti)

    // Slot di oggi (ogni prenotazione può avere più slot — filtra per data)
    const slotOggi = []
    for (const p of prenList) {
      for (const s of (p.slots || [])) {
        if (s.data === dataOggi && !s.annullato) slotOggi.push({ ...s })
      }
    }

    kpi.value = {
      prenotazioniOggi: slotOggi.length,
      auleOccupateOggi: new Set(slotOggi.map(s => s.aula_id)).size,
      conflittiAperti:  conflList.length,
      utentiAttivi: utentiList.filter(u => u.attivo).length,
    }

    saturazioneSedi.value = sediList.map(sede => {
      const auleS    = auleList.filter(a => a.sede_id === sede.id)
      const aulaIds  = new Set(auleS.map(a => a.id))
      const occupate = new Set(slotOggi.filter(s => aulaIds.has(s.aula_id)).map(s => s.aula_id)).size
      return {
        id: sede.id,
        nome: sede.nome,
        totale: auleS.length,
        occupate,
        pct: percentuale(occupate, auleS.length),
      }
    })
  } catch (e) {
    console.warn('DashboardCoord:', e.message)
  } finally {
    loadingSedi.value = false
  }
})
</script>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; }
.kpi-card   { border-radius: 12px; }
.kpi-value  { font-size: 2rem; font-weight: 800; line-height: 1; }
.kpi-label  { font-size: .8rem; color: #666; margin-top: .25rem; }
</style>