<template>
  <div class="page-operativo">
    <div class="page-header mb-4">
      <h2 class="page-title">Ciao, {{ auth.nomeUtente }} 👋</h2>
      <p class="text-muted mb-0">{{ oggiLabel }} — qui trovi un riepilogo rapido della tua attività.</p>
    </div>

    <!-- KPI -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.attive)"     label="Prenotazioni attive"  icon="it-calendar"     color="primary" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.oggi)"       label="Slot oggi"            icon="it-check-circle" color="success" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.conflitti)"  label="Con conflitti"        icon="it-error"        color="danger" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard :value="String(kpi.prossimi7)"  label="Slot prossimi 7 gg"   icon="it-calendar"     color="info" />
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
                <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
                Nuova prenotazione
              </RouterLink>
              <!-- <RouterLink :to="{ name: 'NuovaPrenotazione', query: { tipo: 'massiva' } }" class="btn btn-outline-primary">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-files'"></use></svg>
                Prenotazione massiva
              </RouterLink> -->
              <RouterLink :to="{ name: 'Calendario' }" class="btn btn-outline-secondary">
                <svg class="icon icon-sm me-1"><use :href="sprites + '#it-calendar'"></use></svg>
                Calendario
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

    <!-- Ultimi slot + prossimi -->
    <div class="row g-3">
      <div class="col-12 col-xl-8">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 pb-0 d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Ultimi slot prenotati</h5>
            <RouterLink :to="{ name: 'MiePrenotazioni' }" class="btn btn-sm btn-outline-primary">
              Vedi tutte
            </RouterLink>
          </div>
          <div class="card-body pt-2">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
            <div v-else-if="!ultimi.length" class="text-muted text-center py-4">
              Nessuna prenotazione trovata.
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover table-sm align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Data</th>
                    <th>Orario</th>
                    <th>Aula</th>
                    <th>Corso ID</th>
                    <th>Conflitto</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="s in ultimi" :key="s.key"
                    :class="{ 'table-danger': s.haConflitti }">
                    <td class="fw-semibold">{{ formatData(s.data) }}</td>
                    <td class="text-nowrap">{{ s.oraInizio }} – {{ s.oraFine }}</td>
                    <td>
                      <span class="fw-semibold">{{ nomeAulaFn(s.aulaId) }}</span>
                      <small class="text-muted d-block">{{ sedeDiAulaFn(s.aulaId) }}</small>
                    </td>
                    <td><code class="small">{{ s.corsoId }}</code></td>
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
              Nessuno slot nei prossimi 7 giorni.
            </div>
            <ul v-else class="list-unstyled mb-0">
              <li v-for="s in prossimi" :key="s.key"
                class="d-flex align-items-start gap-2 py-2 border-bottom">
                <div class="cal-badge text-center flex-shrink-0">
                  <span class="cal-badge-day">{{ new Date(s.data + 'T00:00:00').getDate() }}</span>
                  <span class="cal-badge-month">{{ meseBreve(s.data) }}</span>
                </div>
                <div class="small overflow-hidden">
                  <div class="fw-semibold text-truncate">{{ nomeAulaFn(s.aulaId) }}</div>
                  <div class="text-muted">{{ s.oraInizio }} – {{ s.oraFine }}</div>
                  <div class="text-muted">Corso {{ s.corsoId }}</div>
                </div>
              </li>
            </ul>
            <RouterLink :to="{ name: 'Calendario' }" class="btn btn-outline-primary btn-sm mt-3 w-100">
              <svg class="icon icon-sm me-1"><use :href="sprites + '#it-calendar'"></use></svg>
              Apri Calendario
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import StatCard from '@/components/ui/StatCard.vue'
import { getMiePrenotazioni } from '@/api/prenotazioni'
import { useAule } from '@/composables/useAule'
import { formatData, oggi, aggiungiGiorni } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const auth    = useAuthStore()
const loading = ref(false)
const prenotazioni = ref([])

const { nomeAula: nomeAulaFn, sedeDiAula: sedeDiAulaFn, carica: caricaAule } = useAule()

const oggiISO = oggi()
const fra7    = aggiungiGiorni(oggiISO, 7)

const oggiLabel = new Date().toLocaleDateString('it-IT', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
})

function meseBreve(isoDate) {
  return new Date(isoDate + 'T00:00:00').toLocaleDateString('it-IT', { month: 'short' }).toUpperCase()
}

// ── Espande le prenotazioni in slot, filtrando per utente corrente ─────────────
const tuttiSlot = computed(() => {
  const list = []
  for (const p of prenotazioni.value) {
    // OPERATIVO vede solo i propri
    if (!auth.isCoordinamento && auth.utente?.id && p.richiedente_id !== auth.utente.id) continue
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]
      if (!slot?.data) continue
      list.push({
        key:         `${p.id}-${si}`,
        prenId:      p.id,
        aulaId:      p.aula_id,
        corsoId:     p.corso_id,
        haConflitti: p.richiesta?.ha_conflitti || false,
        data:        slot.data,
        oraInizio:   slot.ora_inizio?.slice(0, 5) || '—',
        oraFine:     slot.ora_fine?.slice(0, 5)   || '—',
      })
    }
  }
  return list.sort((a, b) => b.data.localeCompare(a.data))
})

// Ultimi 8 slot (passati + oggi)
const ultimi = computed(() =>
  tuttiSlot.value.filter(s => s.data <= oggiISO).slice(0, 8)
)

// Prossimi 7 giorni
const prossimi = computed(() =>
  tuttiSlot.value
    .filter(s => s.data > oggiISO && s.data <= fra7)
    .sort((a, b) => a.data.localeCompare(b.data))
    .slice(0, 10)
)

// KPI
const kpi = computed(() => ({
  attive:    tuttiSlot.value.filter(s => s.data >= oggiISO).length,
  oggi:      tuttiSlot.value.filter(s => s.data === oggiISO).length,
  conflitti: tuttiSlot.value.filter(s => s.haConflitti).length,
  prossimi7: prossimi.value.length,
}))

onMounted(async () => {
  await caricaAule()
  loading.value = true
  try {
    const data = await getMiePrenotazioni()
    prenotazioni.value = Array.isArray(data) ? data : (data?.items || [])
  } catch (e) {
    console.warn('DashboardOperativo:', e.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; }
.cal-badge {
  background: #0066cc; color: #fff; border-radius: 6px;
  padding: 4px 8px; min-width: 38px;
}
.cal-badge-day   { display: block; font-size: 1.1rem; font-weight: 700; line-height: 1; }
.cal-badge-month { display: block; font-size: .6rem; font-weight: 600; opacity: .85; }
</style>