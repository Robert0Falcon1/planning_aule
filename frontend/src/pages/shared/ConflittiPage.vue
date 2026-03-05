<template>
  <div class="page-conflitti">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Conflitti</h2>
      <span v-if="conflitti.length" class="badge bg-danger fs-6 ms-1">{{ conflitti.length }}</span>
      <div class="ms-auto d-flex gap-2 align-items-center">
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="carica">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>
        <div class="form-check form-switch mb-0">
          <input class="form-check-input" type="checkbox" id="soloAttivi" v-model="soloAttivi" @change="carica" />
          <label class="form-check-label small" for="soloAttivi">Solo attivi</label>
        </div>
        <button class="btn btn-sm btn-outline-secondary" @click="carica">
          <svg class="icon icon-sm me-1"><use :href="sprites + '#it-refresh'"></use></svg>
          Aggiorna
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="!conflitti.length" class="card border-0 shadow-sm">
      <div class="card-body text-center py-5">
        <svg class="icon icon-xl text-success mb-3"><use :href="sprites + '#it-check-circle'"></use></svg>
        <h5 class="text-success">Nessun conflitto rilevato</h5>
        <p class="text-muted mb-0">Tutte le prenotazioni sono coerenti.</p>
      </div>
    </div>

    <div v-else>
      <div class="alert alert-warning d-flex align-items-center gap-2 mb-4">
        <svg class="icon icon-warning flex-shrink-0"><use :href="sprites + '#it-error'"></use></svg>
        <span><strong>{{ conflitti.length }} {{ conflitti.length === 1 ? 'conflitto' : 'conflitti' }}</strong> rilevati.</span>
      </div>

      <div class="d-flex flex-column gap-3">
        <div v-for="c in conflitti" :key="c.id" class="card border-0 shadow-sm">
          <div class="card-header bg-white d-flex align-items-center gap-2 py-2">
            <span class="badge bg-danger">Conflitto #{{ c.id }}</span>
            <span class="badge bg-secondary ms-1">{{ c.tipo_conflitto }}</span>
            <span v-if="c.stato_risoluzione !== 'NON_RISOLTO'" class="badge bg-success ms-1">Risolto</span>
            <small class="ms-auto text-muted">{{ formatData(c.rilevato_il) }}</small>
          </div>

          <div class="card-body">
            <div class="row g-3 align-items-center">
              <!-- Prenotazione A -->
              <div class="col-md-5">
                <div class="conflitto-pill pill-a h-100">
                  <div class="small fw-semibold text-muted mb-1">Prenotazione A</div>
                  <div class="fw-bold">#{{ c.prenotazione_id_1 }}</div>
                </div>
              </div>

              <!-- Centro -->
              <div class="col-md-2 d-flex flex-column align-items-center justify-content-center text-center">
                <svg class="icon text-danger mb-1"><use :href="sprites + '#it-error'"></use></svg>
                <small class="text-muted">vs</small>
              </div>

              <!-- Prenotazione B -->
              <div class="col-md-5">
                <div class="conflitto-pill pill-b h-100">
                  <div class="small fw-semibold text-muted mb-1">Prenotazione B</div>
                  <div class="fw-bold">#{{ c.prenotazione_id_2 }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Azioni risoluzione -->
          <div v-if="c.stato_risoluzione === 'NON_RISOLTO'" class="card-footer bg-white d-flex flex-wrap gap-2">
            <small class="text-muted me-2 align-self-center">Risolvi:</small>
            <button class="btn btn-sm btn-outline-warning" @click="risolvi(c.id, 'mantieni_1')" :disabled="risolvendo === c.id">
              Mantieni A (#{{ c.prenotazione_id_1 }})
            </button>
            <button class="btn btn-sm btn-outline-warning" @click="risolvi(c.id, 'mantieni_2')" :disabled="risolvendo === c.id">
              Mantieni B (#{{ c.prenotazione_id_2 }})
            </button>
            <button class="btn btn-sm btn-outline-danger" @click="risolvi(c.id, 'elimina_entrambe')" :disabled="risolvendo === c.id">
              Elimina entrambe
            </button>
            <button class="btn btn-sm btn-outline-secondary" @click="risolvi(c.id, 'manuale')" :disabled="risolvendo === c.id">
              Segna risolto
            </button>
            <span v-if="risolvendo === c.id" class="spinner-border spinner-border-sm align-self-center ms-2"></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getConflitti, risolviConflitto } from '@/api/prenotazioni'
import { getSedi } from '@/api/sedi'
import { formatData } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading    = ref(false)
const conflitti  = ref([])
const sedi       = ref([])
const filtroSede = ref('')
const soloAttivi = ref(true)
const risolvendo = ref(null)

async function carica() {
  loading.value = true
  try {
    const params = { solo_attivi: soloAttivi.value }
    if (filtroSede.value) params.sede_id = filtroSede.value
    const data = await getConflitti(params)
    if (Array.isArray(data))           conflitti.value = data
    else if (data?.items)              conflitti.value = data.items
    else if (typeof data === 'string') { try { conflitti.value = JSON.parse(data) } catch { conflitti.value = [] } }
    else                               conflitti.value = []
  } catch (e) {
    console.warn('Conflitti:', e.message)
    conflitti.value = []
  } finally {
    loading.value = false
  }
}

async function risolvi(id, azione) {
  if (!id) return
  risolvendo.value = id
  try {
    await risolviConflitto(id, azione)
    await carica()
  } catch (e) {
    alert(`Errore: ${e.message}`)
  } finally {
    risolvendo.value = null
  }
}

onMounted(async () => {
  const data = await getSedi()
  sedi.value = Array.isArray(data) ? data : []
  carica()
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
.conflitto-pill { padding: 10px 14px; border-radius: 8px; font-size: .82rem; }
.pill-a { background: #fff3cd; border-left: 4px solid #ffc107; }
.pill-b { background: #f8d7da; border-left: 4px solid #dc3545; }
</style>