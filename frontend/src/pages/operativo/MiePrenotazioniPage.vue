<template>
  <div class="page-mie-prenotazioni">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">{{ titoloPageina }}</h2>
      <div class="ms-auto d-flex gap-2 flex-wrap align-items-center">

        <!-- Filtro sede -->
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="onSedeChange">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>

        <!-- Filtro aula -->
        <select v-model="filtroAula" class="form-select form-select-sm" style="width:auto">
          <option value="">Tutte le aule</option>
          <option v-for="a in auleFiltrate" :key="a.id" :value="a.id">{{ a.nome }}</option>
        </select>

        <!-- Filtro utente (solo COORDINAMENTO) -->
        <select v-if="authStore.isCoordinamento" v-model="filtroUtente"
          class="form-select form-select-sm" style="width:auto">
          <option value="">Tutti gli utenti</option>
          <option v-for="u in utenti" :key="u.id" :value="u.id">
            {{ u.nome }} {{ u.cognome }}
          </option>
        </select>

        <!-- Filtro stato/conflitti -->
        <select v-model="filtroStato" class="form-select form-select-sm" style="width:auto">
          <option value="">Tutti</option>
          <option value="confermata">Confermate</option>
          <option value="conflitto">Con conflitti</option>
        </select>

        <!-- Filtro date -->
        <input v-model="filtroDa" type="date" class="form-control form-control-sm" style="width:auto" />
        <span class="text-muted small">→</span>
        <input v-model="filtroA"  type="date" class="form-control form-control-sm" style="width:auto" />
        <button class="btn btn-sm btn-outline-secondary" @click="resetFiltri">Reset</button>

        <RouterLink :to="{ name: 'NuovaPrenotazione' }" class="btn btn-sm btn-primary">
          <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
          Nuova
        </RouterLink>
      </div>
    </div>

    <!-- KPI -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-md-4">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-primary">{{ conteggioSlot }}</div>
          <div class="small text-muted">Slot totali</div>
        </div>
      </div>
      <div class="col-6 col-md-4">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-danger">{{ conteggioConflitti }}</div>
          <div class="small text-muted">Con conflitti</div>
        </div>
      </div>
      <div class="col-6 col-md-4">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-secondary">{{ slotFiltrati.length }}</div>
          <div class="small text-muted">Risultati filtrati</div>
        </div>
      </div>
    </div>

    <!-- Tabella -->
    <div class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
        <div v-else-if="!paginaCorrente.length" class="text-center text-muted py-5">
          <p class="mb-0">Nessuna prenotazione trovata.</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light sticky-top">
              <tr>
                <th>Data</th>
                <th>Orario</th>
                <th>Aula</th>
                <th>Corso ID</th>
                <th v-if="authStore.isCoordinamento">Prenotato da</th>
                <th>Conflitti</th>
                <th class="text-end">Azioni</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="slot in paginaCorrente" :key="slot.key"
                :class="{ 'row-conflitto': slot.haConflitti }">

                <td>
                  <span class="fw-semibold">{{ formatData(slot.data) }}</span>
                </td>

                <td class="text-nowrap">
                  {{ slot.oraInizio }} – {{ slot.oraFine }}
                </td>

                <td>
                  <span class="small fw-semibold">{{ nomeAulaFn(slot.aulaId) }}</span><br>
                  <small class="text-muted">{{ sedeDiAulaFn(slot.aulaId) }}</small>
                </td>

                <td><code class="small">{{ slot.corsoId }}</code></td>

                <!-- Colonna richiedente (solo COORDINAMENTO) -->
                <td v-if="authStore.isCoordinamento">
                  <span class="small">{{ nomeUtente(slot.richiedenteId) }}</span>
                </td>

                <td>
                  <span v-if="slot.haConflitti" class="badge bg-danger">
                    <svg class="icon icon-xs icon-white"><use :href="sprites + '#it-error'"></use></svg>
                    Sì
                  </span>
                  <span v-else class="text-muted small">—</span>
                </td>

                <td class="text-end">
                  <button class="btn btn-sm btn-outline-danger"
                    :disabled="cancellando === slot.prenId"
                    @click="richiediCancellazione(slot)">
                    <span v-if="cancellando === slot.prenId" class="spinner-border spinner-border-sm"></span>
                    <svg v-else class="icon icon-sm"><use :href="sprites + '#it-delete'"></use></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Paginazione -->
      <div v-if="totalePagine > 1" class="card-footer bg-white d-flex justify-content-between align-items-center">
        <small class="text-muted">{{ slotFiltrati.length }} slot</small>
        <nav>
          <ul class="pagination pagination-sm mb-0">
            <li class="page-item" :class="{ disabled: pagina === 1 }">
              <button class="page-link" @click="pagina--">‹</button>
            </li>
            <li class="page-item active">
              <span class="page-link">{{ pagina }} / {{ totalePagine }}</span>
            </li>
            <li class="page-item" :class="{ disabled: pagina === totalePagine }">
              <button class="page-link" @click="pagina++">›</button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- Modal conferma cancellazione -->
    <div v-if="modalCancella" class="modal-backdrop-custom" @click.self="modalCancella = null">
      <div class="modal-dialog-custom card border-0 shadow-lg p-4">
        <h5 class="fw-bold mb-2">Conferma eliminazione</h5>
        <p class="text-muted mb-3">
          Stai per eliminare lo slot del
          <strong>{{ formatData(modalCancella.data) }}</strong>
          ore {{ modalCancella.oraInizio }}–{{ modalCancella.oraFine }}
          in <strong>{{ nomeAulaFn(modalCancella.aulaId) }}</strong>.
        </p>

        <!-- Prenotazione massiva: offre scelta -->
        <div v-if="modalCancella.isMassiva" class="alert alert-info py-2 small mb-3">
          Questo slot fa parte di una prenotazione ricorrente con
          <strong>{{ modalCancella.totaleSlot }} slot</strong> totali.
          Puoi eliminare solo questo slot oppure tutti.
        </div>

        <div class="d-flex gap-2 justify-content-end flex-wrap">
          <button class="btn btn-outline-secondary" @click="modalCancella = null">Annulla</button>
          <button v-if="modalCancella.isMassiva"
            class="btn btn-outline-danger" @click="confermaCancellazione(false)" :disabled="!!cancellando">
            <span v-if="cancellando" class="spinner-border spinner-border-sm me-1"></span>
            Solo questo slot
          </button>
          <button class="btn btn-danger" @click="confermaCancellazione(true)" :disabled="!!cancellando">
            <span v-if="cancellando" class="spinner-border spinner-border-sm me-1"></span>
            {{ modalCancella.isMassiva ? 'Elimina tutti gli slot' : 'Sì, elimina' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getMiePrenotazioni, cancellaPrenotazione, annullaSlot } from '@/api/prenotazioni'
import { getUtenti } from '@/api/utenti'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { useAule } from '@/composables/useAule'
import { formatData } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const authStore = useAuthStore()
const { nomeAula: nomeAulaFn, sedeDiAula: sedeDiAulaFn, carica: caricaAule } = useAule()

const loading       = ref(false)
const prenotazioni  = ref([])
const sedi          = ref([])
const aule          = ref([])
const utenti        = ref([])
const filtroSede    = ref('')
const filtroAula    = ref('')
const filtroUtente  = ref('')
const filtroStato   = ref('')
const filtroDa      = ref('')
const filtroA       = ref('')
const pagina        = ref(1)
const PER_PAGINA    = 20
const cancellando   = ref(null)
const modalCancella = ref(null)

const titoloPageina = computed(() =>
  authStore.isCoordinamento ? 'Prenotazioni' : 'Mie Prenotazioni'
)

const auleFiltrate = computed(() =>
  filtroSede.value
    ? aule.value.filter(a => a.sede_id == filtroSede.value)
    : aule.value
)
function onSedeChange() { filtroAula.value = '' }

// ── Mappa utenti per lookup ───────────────────────────────────────────────────
const mappaUtenti = computed(() =>
  Object.fromEntries(utenti.value.map(u => [u.id, u]))
)
function nomeUtente(id) {
  const u = mappaUtenti.value[id]
  return u ? `${u.nome} ${u.cognome}` : `#${id}`
}

// ── Espande ogni prenotazione in slot individuali ─────────────────────────────
const tuttiGliSlot = computed(() => {
  const list = []
  for (const p of prenotazioni.value) {
    // Filtra per utente se OPERATIVO
    if (!authStore.isCoordinamento && authStore.utente?.id) {
      if (p.richiedente_id !== authStore.utente.id) continue
    }
    const isMassiva = p.tipo === 'massiva'
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]
      if (!slot?.data) continue
      list.push({
        key:           `${p.id}-${si}`,
        prenId:        p.id,
        slotId:        slot.id,
        slotIdx:       si,
        aulaId:        p.aula_id,
        corsoId:       p.corso_id,
        richiedenteId: p.richiedente_id,
        haConflitti:   p.richiesta?.ha_conflitti || false,
        isMassiva,
        totaleSlot:    p.slots.length,
        data:          slot.data,
        oraInizio:     slot.ora_inizio?.slice(0, 5) || '—',
        oraFine:       slot.ora_fine?.slice(0, 5)   || '—',
      })
    }
  }
  // Ordina per data desc
  return list.sort((a, b) => a.data > b.data ? -1 : a.data < b.data ? 1 : 0)
})

// ── Slot filtrati ─────────────────────────────────────────────────────────────
const slotFiltrati = computed(() => {
  let list = tuttiGliSlot.value

  if (filtroAula.value) {
    list = list.filter(s => s.aulaId == filtroAula.value)
  } else if (filtroSede.value) {
    const ids = new Set(aule.value.filter(a => a.sede_id == filtroSede.value).map(a => a.id))
    list = list.filter(s => ids.has(s.aulaId))
  }

  if (filtroUtente.value) {
    list = list.filter(s => s.richiedenteId == filtroUtente.value)
  }

  if (filtroStato.value === 'conflitto') {
    list = list.filter(s => s.haConflitti)
  } else if (filtroStato.value === 'confermata') {
    list = list.filter(s => !s.haConflitti)
  }

  if (filtroDa.value) list = list.filter(s => s.data >= filtroDa.value)
  if (filtroA.value)  list = list.filter(s => s.data <= filtroA.value)

  return list
})

const paginaCorrente = computed(() => {
  const ini = (pagina.value - 1) * PER_PAGINA
  return slotFiltrati.value.slice(ini, ini + PER_PAGINA)
})

const totalePagine       = computed(() => Math.ceil(slotFiltrati.value.length / PER_PAGINA) || 1)
const conteggioSlot      = computed(() => tuttiGliSlot.value.length)
const conteggioConflitti = computed(() => tuttiGliSlot.value.filter(s => s.haConflitti).length)

function resetFiltri() {
  filtroSede.value = ''; filtroAula.value = ''; filtroUtente.value = ''
  filtroStato.value = ''; filtroDa.value = ''; filtroA.value = ''
  pagina.value = 1
}

function richiediCancellazione(slot) { modalCancella.value = slot }

async function confermaCancellazione(eliminaTutti = true) {
  const slot = modalCancella.value; if (!slot) return
  cancellando.value = slot.prenId
  try {
    if (!eliminaTutti && slot.isMassiva) {
      // Annulla solo questo slot via nuovo endpoint
      const res = await annullaSlot(slot.prenId, slot.slotId)
      if (res.prenotazione_eliminata) {
        // Era l'ultimo slot — rimuovi l'intera prenotazione
        prenotazioni.value = prenotazioni.value.filter(p => p.id !== slot.prenId)
      } else {
        // Marca lo slot come annullato nella lista locale
        const pren = prenotazioni.value.find(p => p.id === slot.prenId)
        if (pren) {
          const s = pren.slots.find(s => s.id === slot.slotId)
          if (s) s.annullato = true
        }
      }
    } else {
      // Elimina l'intera prenotazione
      await cancellaPrenotazione(slot.prenId)
      prenotazioni.value = prenotazioni.value.filter(p => p.id !== slot.prenId)
    }
    modalCancella.value = null
  } catch (e) {
    alert(`Errore: ${e.message}`)
  } finally {
    cancellando.value = null
  }
}

onMounted(async () => {
  await caricaAule()
  loading.value = true
  try {
    const calls = [getSedi(), getAule(), getMiePrenotazioni()]
    if (authStore.isCoordinamento) calls.push(getUtenti())
    const [dataSedi, dataAule, dataPren, dataUtenti] = await Promise.all(calls)
    sedi.value  = Array.isArray(dataSedi)  ? dataSedi  : []
    aule.value  = Array.isArray(dataAule)  ? dataAule  : []
    prenotazioni.value = Array.isArray(dataPren) ? dataPren : (dataPren?.items || [])
    if (dataUtenti) utenti.value = Array.isArray(dataUtenti) ? dataUtenti : []
  } catch (e) {
    console.warn('MiePrenotazioni:', e.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
.row-conflitto { background: #fff3f3 !important; }
.modal-backdrop-custom {
  position: fixed; inset: 0; background: rgba(0,0,0,.45);
  display: flex; align-items: center; justify-content: center; z-index: 2000;
}
.modal-dialog-custom { width: 100%; max-width: 500px; border-radius: 12px; }
</style>