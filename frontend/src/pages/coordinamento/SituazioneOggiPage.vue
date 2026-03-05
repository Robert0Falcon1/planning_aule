<template>
  <div class="page-situazione">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Situazione Oggi</h2>
      <div class="ms-auto d-flex gap-2 flex-wrap align-items-center">
        <button class="btn btn-outline-secondary btn-sm" @click="spostaGiorno(-1)">
          <svg class="icon icon-sm"><use :href="sprites + '#it-chevron-left'"></use></svg>
        </button>
        <input v-model="dataSelezionata" type="date" class="form-control form-control-sm" style="width:auto" @change="carica" />
        <button class="btn btn-outline-secondary btn-sm" @click="spostaGiorno(1)">
          <svg class="icon icon-sm"><use :href="sprites + '#it-chevron-right'"></use></svg>
        </button>
        <button class="btn btn-sm btn-outline-primary" @click="dataSelezionata = oggiISO; carica()">Oggi</button>
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="carica">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>
        <button class="btn btn-sm btn-success" @click="esporta" :disabled="exporting">
          <span v-if="exporting" class="spinner-border spinner-border-sm me-1"></span>
          <svg v-else class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-download'"></use></svg>
          CSV
        </button>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-primary">{{ prenotazioni.length }}</div>
          <div class="small text-muted">Prenotazioni totali</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-success">{{ confermate }}</div>
          <div class="small text-muted">Confermate</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-secondary">{{ cancellate }}</div>
          <div class="small text-muted">Cancellate</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
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
      <div v-for="sede in sediConPrenotazioni" :key="sede.id" class="mb-4">
        <h5 class="fw-bold text-primary mb-2">
          <svg class="icon icon-primary icon-sm me-1"><use :href="sprites + '#it-map-marker'"></use></svg>
          {{ sede.nome }}
          <span class="badge bg-primary-subtle text-primary ms-2 fw-normal">{{ sede.prenotazioni.length }} prenotazioni</span>
        </h5>
        <div class="card border-0 shadow-sm">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 table-sm">
              <thead class="table-light">
                <tr><th>Aula</th><th>Corso</th><th>Orario</th><th>Operativo</th><th>Stato</th></tr>
              </thead>
              <tbody>
                <tr v-for="p in sede.prenotazioni" :key="p.id">
                  <td class="fw-semibold">{{ p.aula?.nome || '—' }}</td>
                  <td>{{ p.titolo_corso }}</td>
                  <td class="text-nowrap">{{ p.ora_inizio }} – {{ p.ora_fine }}</td>
                  <td>{{ p.utente?.nome_completo || p.utente?.username || '—' }}</td>
                  <td>
                    <span class="badge" :class="p.stato === 'confermata' || p.stato === 'CONFERMATA' ? 'bg-success' : 'bg-secondary'">
                      {{ p.stato }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div v-if="!sediConPrenotazioni.length" class="card border-0 shadow-sm">
        <div class="card-body text-center text-muted py-5">
          Nessuna prenotazione per questa data{{ filtroSede ? ' e sede' : '' }}.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSedi } from '@/api/sedi'
import { getPrenotazioni, esportaCsv } from '@/api/prenotazioni'
import { oggi, aggiungiGiorni } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading         = ref(false)
const exporting       = ref(false)
const sedi            = ref([])
const prenotazioni    = ref([])
const oggiISO         = oggi()
const dataSelezionata = ref(oggiISO)
const filtroSede      = ref('')

const confermate   = computed(() => prenotazioni.value.filter(p => p.stato === 'confermata' || p.stato === 'CONFERMATA').length)
const cancellate   = computed(() => prenotazioni.value.filter(p => p.stato === 'annullata'  || p.stato === 'CANCELLATA').length)
const auleOccupate = computed(() => new Set(prenotazioni.value.filter(p => p.stato === 'confermata' || p.stato === 'CONFERMATA').map(p => p.aula_id || p.aula?.id)).size)

const sediConPrenotazioni = computed(() => {
  const map = {}
  for (const p of prenotazioni.value) {
    const sedeId   = p.aula?.sede?.id   || p.sede_id || 0
    const sedeNome = p.aula?.sede?.nome || '—'
    if (!map[sedeId]) map[sedeId] = { id: sedeId, nome: sedeNome, prenotazioni: [] }
    map[sedeId].prenotazioni.push(p)
  }
  return Object.values(map).sort((a, b) => a.nome.localeCompare(b.nome))
})

function spostaGiorno(n) {
  dataSelezionata.value = aggiungiGiorni(dataSelezionata.value, n)
  carica()
}

async function carica() {
  loading.value = true
  try {
    const data = await getPrenotazioni({
      data_dal: dataSelezionata.value,
      data_al:  dataSelezionata.value,
      sede_id:  filtroSede.value || undefined,
    })
    prenotazioni.value = data?.items || data || []
  } catch (e) {
    console.warn('SituazioneOggi:', e.message)
  } finally {
    loading.value = false
  }
}

async function esporta() {
  exporting.value = true
  try {
    await esportaCsv({ data_dal: dataSelezionata.value, data_al: dataSelezionata.value, sede_id: filtroSede.value || undefined })
  } catch (e) {
    alert(`Errore export: ${e.message}`)
  } finally {
    exporting.value = false
  }
}

onMounted(async () => {
  const data = await getSedi()
  sedi.value = data?.items || data || []
  carica()
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
</style>