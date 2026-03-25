<template>
  <div class="page-conflitti">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Conflitti</h2>

      <!-- Conflitti + numero -->
      <span v-if="conflittiOrdinati.length" class="badge bg-danger fs-6 ms-1">{{ conflittiOrdinati.length }}</span>



      <div class="ms-auto d-flex gap-2 align-items-center">



        <!-- Solo attivi -->
        <div class="form-check form-switch mb-0 ps-0 me-3">
          <input class="form-check-input" type="checkbox" id="soloAttivi" v-model="soloAttivi" @change="carica" />
          <label class="form-check-label small" for="soloAttivi">Solo attivi</label>
        </div>

        <!-- Filtro Sedi -->
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="carica">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>

        <!-- Filtro utenti multi-selezione (max 2) -->
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown"
            style="min-width: 180px">
            <span v-if="!filtroUtenti.length">Filtra per utente</span>
            <span v-else-if="filtroUtenti.length === 1">1 utente</span>
            <span v-else>2 utenti</span>
          </button>
          <div class="dropdown-menu p-2" style="max-height: 300px; overflow-y: auto; min-width: 250px">
            <div class="small text-muted mb-2 px-2">Seleziona max 2 utenti</div>
            <div v-for="u in opzioniUtenti" :key="u.value" class="form-check">
              <input :id="`user-${u.value}`" v-model="filtroUtenti" :value="u.value" type="checkbox"
                class="form-check-input" :disabled="filtroUtenti.length >= 2 && !filtroUtenti.includes(u.value)" />
              <label :for="`user-${u.value}`" class="form-check-label small">
                {{ u.label }}
              </label>
            </div>
            <div v-if="filtroUtenti.length > 0" class="border-top mt-2 pt-2">
              <button class="btn btn-sm btn-outline-secondary w-100" @click.stop="filtroUtenti = []">
                Cancella selezione
              </button>
            </div>
          </div>
        </div>

        <!-- Aggiorna -->
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

      <div class="d-flex flex-column gap-3">
        <div v-for="c in conflittiOrdinati" :key="c.id" class="card border-0 shadow-sm">

          <!-- Header -->
          <div class="card-header bg-white d-flex align-items-center gap-2 py-2">
            <span class="badge bg-danger">Conflitto tra {{
              nomeUtente(prenById(c.prenotazione_id_1)?.richiedente_id) }} e {{
                nomeUtente(prenById(c.prenotazione_id_2)?.richiedente_id) }}</span>
            <span v-if="c.stato_risoluzione" class="badge bg-success ms-1">
              {{ messaggioRisoluzione(c) }}
            </span>
            <small class="ms-auto text-muted">{{ formatData(c.rilevato_il) }}</small>
          </div>

          <!-- Corpo: slot in conflitto -->
          <!-- Corpo: dati comuni + slot in conflitto -->
          <div class="card-body pb-2">
            <!-- DATI COMUNI -->
            <div class="mb-3 p-2 bg-lighter rounded d-flex gap-3 align-items-center flex-wrap">
              <div class="d-flex align-items-center gap-1">
                <svg class="icon icon-sm text-primary">
                  <use :href="sprites + '#it-map-marker'"></use>
                </svg>
                <strong class="small">Sede:</strong>
                <span class="small">{{ sedeDiAulaFn(infoSlot(c, 1)?.aula_id) }}</span>
              </div>
              <div class="d-flex align-items-center gap-1">
                <i class="bi bi-door-open"></i>
                <strong class="small pe-1">Aula:</strong>
                <span :style="getAulaBadgeStyle(nomeAulaFn(infoSlot(c, 1)?.aula_id))"></span>
                <span class="small">{{ nomeAulaFn(infoSlot(c, 1)?.aula_id) }}</span>
              </div>
              <div class="d-flex align-items-center gap-1">
                <svg class="icon icon-sm text-primary">
                  <use :href="sprites + '#it-calendar'"></use>
                </svg>
                <strong class="small">Data:</strong>
                <span class="small">{{ formatData(infoSlot(c, 1)?.data) }}</span>
              </div>
            </div>

            <!-- PRENOTAZIONI A vs B -->
            <div class="row g-3 align-items-stretch">

              <!-- Prenotazione A -->
              <div class="col-md-5">
                <div class="conflitto-pill pill-a h-100">
                  <div class="fw-bold mb-2">Prenotazione A</div>
                  <template v-for="s in [infoSlot(c, 1)]">
                    <template v-if="s">
                      <div class="mb-1">
                        <svg class="icon icon-xs me-1">
                          <use :href="sprites + '#it-user'"></use>
                        </svg>
                        <span class="small">{{ nomeUtente(prenById(c.prenotazione_id_1)?.richiedente_id) }}</span>
                      </div>
                      <div class="mb-1">
                        <svg class="icon icon-xs me-1">
                          <use :href="sprites + '#it-card'"></use>
                        </svg>
                        <span class="small">Corso {{ s.corso_id }}</span>
                      </div>
                      <div class="mb-1">
                        <svg class="icon icon-xs me-1">
                          <use :href="sprites + '#it-clock'"></use>
                        </svg>
                        <span class="small fw-semibold">{{ s.ora_inizio?.slice(0, 5) }} – {{ s.ora_fine?.slice(0, 5)
                          }}</span>
                      </div>
                      <div v-if="s.note" class="mt-2 pt-2 border-top">
                        <div class="text-muted small fst-italic d-flex align-items-start">
                          <svg class="icon icon-xs me-1 mt-1 flex-shrink-0">
                            <use :href="sprites + '#it-note'"></use>
                          </svg>
                          <span>{{ s.note }}</span>
                        </div>
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
                  <div class="fw-bold mb-2">Prenotazione B</div>
                  <template v-for="s in [infoSlot(c, 2)]">
                    <template v-if="s">
                      <div class="mb-1">
                        <svg class="icon icon-xs me-1">
                          <use :href="sprites + '#it-user'"></use>
                        </svg>
                        <span class="small">{{ nomeUtente(prenById(c.prenotazione_id_2)?.richiedente_id) }}</span>
                      </div>
                      <div class="mb-1">
                        <svg class="icon icon-xs me-1">
                          <use :href="sprites + '#it-card'"></use>
                        </svg>
                        <span class="small">Corso {{ s.corso_id }}</span>
                      </div>
                      <div class="mb-1">
                        <svg class="icon icon-xs me-1">
                          <use :href="sprites + '#it-clock'"></use>
                        </svg>
                        <span class="small fw-semibold">{{ s.ora_inizio?.slice(0, 5) }} – {{ s.ora_fine?.slice(0, 5)
                          }}</span>
                      </div>
                      <div v-if="s.note" class="mt-2 pt-2 border-top">
                        <div class="text-muted small fst-italic d-flex align-items-start">
                          <svg class="icon icon-xs me-1 mt-1 flex-shrink-0">
                            <use :href="sprites + '#it-note'"></use>
                          </svg>
                          <span>{{ s.note }}</span>
                        </div>
                      </div>
                    </template>
                    <div v-else class="text-muted small">Caricamento...</div>
                  </template>
                </div>
              </div>
            </div>
          </div>

          <!-- Azioni risoluzione -->
          <div v-if="!c.stato_risoluzione" class="card-footer bg-white">
            <div class="d-flex flex-wrap gap-2 align-items-center">
              <small class="text-muted me-1">Risolvi:</small>

              <button class="btn btn-sm btn-outline-warning" @click="risolvi(c.id, 'mantieni_1')"
                :disabled="risolvendo === c.id" title="Mantieni A, annulla B">
                Mantieni A, annulla B
              </button>
              <button class="btn btn-sm btn-outline-warning" @click="risolvi(c.id, 'mantieni_2')"
                :disabled="risolvendo === c.id" title="Mantieni B, annulla A">
                Mantieni B, annulla A
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="risolvi(c.id, 'elimina_entrambe')"
                :disabled="risolvendo === c.id" title="Annulla entrambe le prenotazioni in conflitto">
                Annulla entrambe le prenotazioni
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
import { useUiStore } from '@/stores/ui'
import { getConflitti, risolviConflitto, getMiePrenotazioni, getPrenotazione } from '@/api/prenotazioni'
import { getSedi } from '@/api/sedi'
import { useAule } from '@/composables/useAule'
import { useAulaColor } from '@/composables/useAulaColor'
import { formatData } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import { getUtenti } from '@/api/utenti'
import { useSedePerFiltro } from '@/composables/useSedePerFiltro'

const { nomeAula: nomeAulaFn, sedeDiAula: sedeDiAulaFn, carica: caricaAule } = useAule()
const { getAulaBadgeStyle } = useAulaColor()
const uiStore = useUiStore()
const utenti = ref([])
const loading = ref(false)
const conflitti = ref([])
const prenotazioni = ref([])   // cache prenotazioni per lookup
const sedi = ref([])
const filtroSede = ref('')
const filtroUtenti = ref([])
const soloAttivi = ref(true)
const risolvendo = ref(null)
const { sedeDefaultFiltro } = useSedePerFiltro()

// ── Lookup prenotazione per id ────────────────────────────────────────────────
const mappaPrenotazioni = computed(() =>
  Object.fromEntries(prenotazioni.value.map(p => [p.id, p]))
)
function prenById(id) { return mappaPrenotazioni.value[id] || null }

const mappaUtenti = computed(() =>
  Object.fromEntries(utenti.value.map(u => [u.id, u]))
)

// ── Opzioni utenti ordinate alfabeticamente ──────────────────────────────────
const opzioniUtenti = computed(() =>
  utenti.value
    .map(u => ({
      value: u.id,
      label: `${u.nome} ${u.cognome}`
    }))
    .sort((a, b) => a.label.localeCompare(b.label))
)

// ── Conflitti ordinati cronologicamente e filtrati per utenti ────────────────
const conflittiOrdinati = computed(() => {
  let lista = conflitti.value

  // Filtra per utenti selezionati (esattamente quei due)
  if (filtroUtenti.value.length === 2) {
    const [id1, id2] = filtroUtenti.value
    lista = lista.filter(c => {
      const richA = prenById(c.prenotazione_id_1)?.richiedente_id
      const richB = prenById(c.prenotazione_id_2)?.richiedente_id
      // Mostra solo conflitti tra esattamente questi due utenti
      return (richA === id1 && richB === id2) || (richA === id2 && richB === id1)
    })
  } else if (filtroUtenti.value.length === 1) {
    // Se solo 1 utente: mostra tutti i suoi conflitti con chiunque
    const idUtente = filtroUtenti.value[0]
    lista = lista.filter(c => {
      const richA = prenById(c.prenotazione_id_1)?.richiedente_id
      const richB = prenById(c.prenotazione_id_2)?.richiedente_id
      return richA === idUtente || richB === idUtente
    })
  }

  // Ordina cronologicamente
  return [...lista].sort((a, b) => {
    const dataA = infoSlot(a, 1)?.data || infoSlot(a, 2)?.data || '9999-12-31'
    const dataB = infoSlot(b, 1)?.data || infoSlot(b, 2)?.data || '9999-12-31'
    return dataA.localeCompare(dataB)
  })
})

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
    console.log('CONFLITTI:', JSON.stringify(conflitti.value.map(c => ({
      id: c.id,
      stato_risoluzione: c.stato_risoluzione,
      tipo: typeof c.stato_risoluzione
    })), null, 2))
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

    // Messaggio di successo
    let msg = 'Conflitto risolto con successo'
    if (azione === 'mantieni_1') msg = '✓ Conflitto risolto: mantenuta prenotazione A'
    else if (azione === 'mantieni_2') msg = '✓ Conflitto risolto: mantenuta prenotazione B'
    else if (azione === 'elimina_entrambe') msg = '✓ Conflitto risolto: entrambe le prenotazioni annullate'

    uiStore.successo(msg)
    await carica()
  } catch (e) {
    uiStore.errore(e.message)
  } finally {
    risolvendo.value = null
  }
}

onMounted(async () => {
  await caricaAule()
  filtroSede.value = sedeDefaultFiltro.value
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

// ── Messaggio risoluzione conflitto ──────────────────────────────────────────
function messaggioRisoluzione(c) {
  if (!c.stato_risoluzione) return null

  const stato = c.stato_risoluzione.toUpperCase()

  if (stato.includes('MANTENUTA_1')) {
    return '✓ Mantenuta A'
  } else if (stato.includes('MANTENUTA_2')) {
    return '✓ Mantenuta B'
  } else if (stato.includes('ELIMINATE_ENTRAMBE')) {
    return '✗ Entrambe annullate'
  }

  return 'Risolto'
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