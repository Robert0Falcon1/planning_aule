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
          <svg class="icon icon-sm me-1">
            <use :href="sprites + '#it-refresh'"></use>
          </svg>
          Aggiorna
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="!conflitti.length" class="card border-0 shadow-sm">
      <div class="card-body text-center py-5">
        <svg class="icon icon-xl text-success mb-3">
          <use :href="sprites + '#it-check-circle'"></use>
        </svg>
        <h5 class="text-success">Nessun conflitto rilevato</h5>
        <p class="text-muted mb-0">Tutte le prenotazioni sono coerenti.</p>
      </div>
    </div>

    <div v-else>
      <!-- <div class="alert alert-warning d-flex align-items-center gap-2 mb-4">
        <svg class="icon icon-warning flex-shrink-0">
          <use :href="sprites + '#it-error'"></use>
        </svg>
        <span>
          <strong>{{ conflitti.length }} {{ conflitti.length === 1 ? 'conflitto' : 'conflitti' }}</strong> {{
            conflitti.length === 1 ? 'rilevato' : 'rilevati' }}. </span>
      </div> -->

      <div class="d-flex flex-column gap-3">
        <div v-for="c in conflitti" :key="c.id" class="card border-0 shadow-sm">

          <!-- Header -->
          <div class="card-header bg-white d-flex align-items-center gap-2 py-2">
            <!-- <span class="badge bg-danger">Conflitto #{{ c.id }}</span> -->
            <span class="badge bg-danger">Conflitto tra {{
              nomeUtente(prenById(c.prenotazione_id_1)?.richiedente_id) }} e {{
                nomeUtente(prenById(c.prenotazione_id_2)?.richiedente_id) }}</span>
            <span v-if="c.stato_risoluzione !== null" class="badge bg-success ms-1">Risolto</span>
            <small class="ms-auto text-muted">{{ formatData(c.rilevato_il) }}</small>
          </div>

          <!-- Corpo: slot in conflitto -->
          <div class="card-body pb-2">
            <div class="row g-3 align-items-stretch">

              <!-- Prenotazione A -->
              <div class="col-md-5">
                <div class="conflitto-pill pill-a h-100">
                  <strong>Prenotazione A ({{
                    nomeUtente(prenById(c.prenotazione_id_1)?.richiedente_id) }})</strong>
                  <template v-for="s in [infoSlot(c, 1)]">
                    <template v-if="s">
                      <div class="text-muted small">
                        Corso {{ prenById(c.prenotazione_id_1)?.corso_id }}
                        <span v-if="prenById(c.prenotazione_id_1)?.tipo === 'massiva'"
                          class="badge bg-info ms-1">Ricorrente</span>
                      </div>
                      <div class="mt-1 small mb-2">
                        <strong>{{ sedeDiAulaFn(prenById(c.prenotazione_id_1)?.aula_id) }}</strong>
                        <span class="text-muted ms-1">- {{ nomeAulaFn(prenById(c.prenotazione_id_1)?.aula_id) }}</span>
                      </div>
                      <div class="fw-bold">{{ formatData(s.data) }}</div>
                      <div class="text-nowrap">Dalle {{ s.ora_inizio }} alle {{ s.ora_fine }}</div>
                      <div v-if="prenById(c.prenotazione_id_1)?.note" class="text-muted small mt-1 fst-italic">
                        <svg class="icon icon-xs me-1"><use :href="sprites + '#it-note'"></use></svg> {{ prenById(c.prenotazione_id_1)?.note }}
                      </div>
                    </template>
                    <div v-else class="text-muted small">Caricamento...</div>
                  </template>
                </div>
              </div>

              <!-- VS -->
              <div class="col-md-2 d-flex flex-column align-items-center justify-content-center text-center">
                <svg class="icon text-danger mb-1">
                  <use :href="sprites + '#it-error'"></use>
                </svg>
                <small class="text-muted fw-semibold">vs</small>
              </div>

              <!-- Prenotazione B -->
              <div class="col-md-5">
                <div class="conflitto-pill pill-b h-100">
                  <strong>Prenotazione B ({{
                    nomeUtente(prenById(c.prenotazione_id_2)?.richiedente_id) }})</strong>
                  <template v-for="s in [infoSlot(c, 2)]">
                    <template v-if="s">
                      <div class="text-muted small">
                        Corso {{ prenById(c.prenotazione_id_2)?.corso_id }}
                        <span v-if="prenById(c.prenotazione_id_2)?.tipo === 'massiva'"
                          class="badge bg-info ms-1">Ricorrente</span>
                      </div>
                      <div class="mt-1 small mb-2">
                        <strong>{{ sedeDiAulaFn(prenById(c.prenotazione_id_2)?.aula_id) }}</strong>
                        <span class="text-muted ms-1">- {{ nomeAulaFn(prenById(c.prenotazione_id_2)?.aula_id) }}</span>
                      </div>
                      <div class="fw-bold">{{ formatData(s.data) }}</div>
                      <div class="text-nowrap">Dalle {{ s.ora_inizio }} alle {{ s.ora_fine }}</div>
                      <div v-if="prenById(c.prenotazione_id_2)?.note" class="text-muted small mt-1 fst-italic">
                        <svg class="icon icon-xs me-1"><use :href="sprites + '#it-note'"></use></svg> {{ prenById(c.prenotazione_id_2)?.note }}
                      </div>
                    </template>
                    <div v-else class="text-muted small">Caricamento...</div>
                  </template>
                </div>
              </div>
            </div>
          </div>

          <!-- Azioni risoluzione -->
          <div v-if="c.stato_risoluzione === null" class="card-footer bg-white">
            <div class="d-flex flex-wrap gap-2 align-items-center">
              <small class="text-muted me-1">Risolvi:</small>

              <button class="btn btn-sm btn-outline-warning" @click="risolvi(c.id, 'mantieni_1')"
                :disabled="risolvendo === c.id" title="Mantieni lo slot A, annulla lo slot B in conflitto">
                Mantieni A, annulla slot B
              </button>
              <button class="btn btn-sm btn-outline-warning" @click="risolvi(c.id, 'mantieni_2')"
                :disabled="risolvendo === c.id" title="Mantieni lo slot B, annulla lo slot A in conflitto">
                Mantieni B, annulla slot A
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="risolvi(c.id, 'elimina_entrambe')"
                :disabled="risolvendo === c.id" title="Annulla entrambi gli slot in conflitto">
                Annulla entrambi gli slot
              </button>
              <span v-if="risolvendo === c.id" class="spinner-border spinner-border-sm align-self-center ms-2"></span>
            </div>
            <div class="mt-2">
              <small class="text-muted">
                <svg class="icon icon-xs me-1">
                  <use :href="sprites + '#it-info-circle'"></use>
                </svg>
                Le azioni annullano solo lo slot in conflitto.
                Per le prenotazioni ricorrenti, gli altri slot rimangono attivi.
              </small>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getConflitti, risolviConflitto, getMiePrenotazioni, getPrenotazione } from '@/api/prenotazioni'
import { getSedi } from '@/api/sedi'
import { useAule } from '@/composables/useAule'
import { formatData } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import { getUtenti } from '@/api/utenti'

const { nomeAula: nomeAulaFn, sedeDiAula: sedeDiAulaFn, carica: caricaAule } = useAule()

const utenti = ref([])
const loading = ref(false)
const conflitti = ref([])
const prenotazioni = ref([])   // cache prenotazioni per lookup
const sedi = ref([])
const filtroSede = ref('')
const soloAttivi = ref(true)
const risolvendo = ref(null)

// ── Lookup prenotazione per id ────────────────────────────────────────────────
const mappaPrenotazioni = computed(() =>
  Object.fromEntries(prenotazioni.value.map(p => [p.id, p]))
)
function prenById(id) { return mappaPrenotazioni.value[id] || null }

const mappaUtenti = computed(() =>
  Object.fromEntries(utenti.value.map(u => [u.id, u]))
)

// ── Info slot specifico dal conflitto ─────────────────────────────────────────
// c.slot_id_1 / c.slot_id_2 → cerca nello slot array della prenotazione
function infoSlot(c, quale) {
  const prenId = quale === 1 ? c.prenotazione_id_1 : c.prenotazione_id_2
  const slotId = quale === 1 ? c.slot_id_1 : c.slot_id_2
  const pren = prenById(prenId)
  if (!pren) return null

  // Se abbiamo lo slot_id specifico, usalo
  if (slotId) {
    const slot = pren.slots?.find(s => s.id === slotId)
    if (slot) return slot
  }
  // Fallback: primo slot non annullato
  return pren.slots?.find(s => !s.annullato) || pren.slots?.[0] || null
}

// ── Caricamento ───────────────────────────────────────────────────────────────
async function carica() {
  loading.value = true
  try {
    const params = { solo_attivi: soloAttivi.value }
    if (filtroSede.value) params.sede_id = filtroSede.value

    const dataConflitti = await getConflitti(params)

    if (Array.isArray(dataConflitti)) conflitti.value = dataConflitti
    else if (dataConflitti?.items) conflitti.value = dataConflitti.items
    else conflitti.value = []

    const prenIds = [...new Set(
      conflitti.value.flatMap(c => [c.prenotazione_id_1, c.prenotazione_id_2])
    )]

    try {
      const dataPren = prenIds.length
        ? await Promise.all(prenIds.map(id => getPrenotazione(id)))
        : []
      prenotazioni.value = dataPren.filter(Boolean)
    } catch (e) {
      console.warn('Errore caricamento prenotazioni per conflitti:', e.message)
      prenotazioni.value = []
    }

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
  await caricaAule()
  const [dataSedi, dataUtenti] = await Promise.all([
    getSedi(),
    getUtenti()
  ])
  sedi.value = Array.isArray(dataSedi) ? dataSedi : []
  utenti.value = Array.isArray(dataUtenti) ? dataUtenti : (dataUtenti?.items || [])
  carica()
})

function nomeUtente(id) {
  const u = mappaUtenti.value[id]
  return u ? `${u.nome} ${u.cognome}` : `#${id}`
}
</script>

<style scoped>
.page-title {
  font-size: 1.4rem;
  font-weight: 700;
}

.conflitto-pill {
  padding: 12px 14px;
  border-radius: 8px;
  font-size: .82rem;
  line-height: 1.5;
}

.pill-a {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
}

.pill-b {
  background: #f8d7da;
  border-left: 4px solid #dc3545;
}
</style>