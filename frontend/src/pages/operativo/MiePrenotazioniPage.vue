<template>
  <div class="page-mie-prenotazioni">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Mie Prenotazioni</h2>
      <div class="ms-auto d-flex gap-2 flex-wrap align-items-center">
        <select v-model="filtroStato" class="form-select form-select-sm" style="width:auto">
          <option value="">Tutti gli stati</option>
          <option value="confermata">Confermate</option>
          <option value="in_attesa">In attesa</option>
          <option value="annullata">Annullate</option>
          <option value="conflitto">Con conflitti</option>
        </select>
        <input v-model="filtroDa" type="date" class="form-control form-control-sm" style="width:auto" />
        <span class="text-muted small">→</span>
        <input v-model="filtroA" type="date" class="form-control form-control-sm" style="width:auto" />
        <button class="btn btn-sm btn-outline-secondary" @click="resetFiltri">Reset</button>
        <RouterLink :to="{ name: 'NuovaPrenotazione' }" class="btn btn-sm btn-primary">
          <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
          Nuova
        </RouterLink>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-primary">{{ conteggioAttive }}</div>
          <div class="small text-muted">Confermate</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-warning">{{ conteggioInAttesa }}</div>
          <div class="small text-muted">In attesa</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-danger">{{ conteggioConflitti }}</div>
          <div class="small text-muted">Con conflitti</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-secondary">{{ prenotazioni.length }}</div>
          <div class="small text-muted">Totale</div>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
        <div v-else-if="!prenotazioniFiltrate.length" class="text-center text-muted py-5">
          <p class="mb-0">Nessuna prenotazione trovata.</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light sticky-top">
              <tr>
                <th>Tipo</th>
                <th>Data / Slot</th>
                <th>Aula ID</th>
                <th>Corso ID</th>
                <th>Stato</th>
                <th>Conflitti</th>
                <th>Creata il</th>
                <th class="text-end">Azioni</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in prenotazioniFiltrate" :key="p.id"
                :class="{ 'row-cancellata': p.stato === 'annullata', 'row-conflitto': p.stato === 'conflitto' }">
                <td>
                  <span class="badge" :class="p.tipo === 'massiva' ? 'bg-info text-dark' : 'bg-secondary'">
                    {{ p.tipo }}
                  </span>
                </td>
                <td>
                  <div v-if="p.slots && p.slots.length">
                    <div v-for="(slot, si) in p.slots.slice(0, 3)" :key="si" class="small">
                      <span class="fw-semibold">{{ formatData(slot.data) }}</span>
                      <span class="text-muted ms-1">{{ slot.ora_inizio?.slice(0,5) }}–{{ slot.ora_fine?.slice(0,5) }}</span>
                    </div>
                    <div v-if="p.slots.length > 3" class="small text-muted">+ altri {{ p.slots.length - 3 }} slot</div>
                  </div>
                  <span v-else class="text-muted small">—</span>
                </td>
                <td><code class="small">{{ p.aula_id }}</code></td>
                <td><code class="small">{{ p.corso_id }}</code></td>
                <td>
                  <span class="badge" :class="badgeStato(p.stato)">{{ p.stato }}</span>
                </td>
                <td>
                  <span v-if="p.richiesta?.ha_conflitti" class="badge bg-danger">Sì</span>
                  <span v-else class="text-muted small">—</span>
                </td>
                <td><small class="text-muted">{{ formatData(p.data_creazione) }}</small></td>
                <td class="text-end">
                  <button v-if="p.stato !== 'annullata'"
                    class="btn btn-sm btn-outline-danger" :disabled="cancellando === p.id"
                    @click="richiediCancellazione(p)">
                    <span v-if="cancellando === p.id" class="spinner-border spinner-border-sm"></span>
                    <svg v-else class="icon icon-sm"><use :href="sprites + '#it-delete'"></use></svg>
                  </button>
                  <span v-else class="text-muted small">—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="totalePagine > 1" class="card-footer bg-white d-flex justify-content-between align-items-center">
        <small class="text-muted">{{ prenotazioni.length }} totali</small>
        <nav>
          <ul class="pagination pagination-sm mb-0">
            <li class="page-item" :class="{ disabled: pagina === 1 }">
              <button class="page-link" @click="pagina--">‹</button>
            </li>
            <li class="page-item active"><span class="page-link">{{ pagina }} / {{ totalePagine }}</span></li>
            <li class="page-item" :class="{ disabled: pagina === totalePagine }">
              <button class="page-link" @click="pagina++">›</button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <div v-if="modalCancella" class="modal-backdrop-custom" @click.self="modalCancella = null">
      <div class="modal-dialog-custom card border-0 shadow-lg p-4">
        <h5 class="fw-bold mb-2">Conferma eliminazione</h5>
        <p class="text-muted mb-3">
          Stai per eliminare la prenotazione <strong>#{{ modalCancella.id }}</strong>
          (aula {{ modalCancella.aula_id }}, corso {{ modalCancella.corso_id }}).
        </p>
        <div v-if="modalCancella.slots?.length > 1" class="alert alert-warning py-2 small">
          Prenotazione massiva con <strong>{{ modalCancella.slots.length }} slot</strong>. Verranno eliminati tutti.
        </div>
        <div class="d-flex gap-2 justify-content-end">
          <button class="btn btn-secondary" @click="modalCancella = null">Annulla</button>
          <button class="btn btn-danger" @click="confermaCancellazione" :disabled="!!cancellando">
            <span v-if="cancellando" class="spinner-border spinner-border-sm me-1"></span>
            Sì, elimina
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMiePrenotazioni, cancellaPrenotazione } from '@/api/prenotazioni'
import { formatData } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading       = ref(false)
const prenotazioni  = ref([])
const filtroStato   = ref('')
const filtroDa      = ref('')
const filtroA       = ref('')
const pagina        = ref(1)
const PER_PAGINA    = 15
const cancellando   = ref(null)
const modalCancella = ref(null)

function dataPrenotazione(p) {
  return p.slots?.[0]?.data || p.data_creazione?.slice(0, 10) || ''
}

const prenotazioniFiltrate = computed(() => {
  let list = [...prenotazioni.value]
  if (filtroStato.value) list = list.filter(p => p.stato === filtroStato.value)
  if (filtroDa.value)    list = list.filter(p => dataPrenotazione(p) >= filtroDa.value)
  if (filtroA.value)     list = list.filter(p => dataPrenotazione(p) <= filtroA.value)
  list.sort((a, b) => {
    const da = dataPrenotazione(a); const db = dataPrenotazione(b)
    return da > db ? -1 : da < db ? 1 : 0
  })
  const ini = (pagina.value - 1) * PER_PAGINA
  return list.slice(ini, ini + PER_PAGINA)
})

const totalePagine       = computed(() => Math.ceil(prenotazioni.value.length / PER_PAGINA) || 1)
const conteggioAttive    = computed(() => prenotazioni.value.filter(p => p.stato === 'confermata').length)
const conteggioInAttesa  = computed(() => prenotazioni.value.filter(p => p.stato === 'in_attesa').length)
const conteggioConflitti = computed(() => prenotazioni.value.filter(p => p.stato === 'conflitto' || p.richiesta?.ha_conflitti).length)

function badgeStato(stato) {
  return { confermata: 'bg-success', in_attesa: 'bg-warning text-dark', rifiutata: 'bg-danger', annullata: 'bg-secondary', conflitto: 'bg-danger' }[stato] || 'bg-secondary'
}

function resetFiltri() { filtroStato.value = ''; filtroDa.value = ''; filtroA.value = ''; pagina.value = 1 }
function richiediCancellazione(p) { modalCancella.value = p }

async function confermaCancellazione() {
  const p = modalCancella.value; if (!p) return
  cancellando.value = p.id
  try {
    await cancellaPrenotazione(p.id)
    prenotazioni.value = prenotazioni.value.filter(x => x.id !== p.id)
    modalCancella.value = null
  } catch (e) {
    alert(`Errore: ${e.message}`)
  } finally {
    cancellando.value = null
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const data = await getMiePrenotazioni()
    prenotazioni.value = Array.isArray(data) ? data : (data?.items || [])
  } catch (e) {
    console.warn('MiePrenotazioni:', e.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
.row-cancellata td { opacity: .55; }
.row-conflitto { background: #fff8f0 !important; }
.modal-backdrop-custom {
  position: fixed; inset: 0; background: rgba(0,0,0,.45);
  display: flex; align-items: center; justify-content: center; z-index: 2000;
}
.modal-dialog-custom { width: 100%; max-width: 480px; border-radius: 12px; }
</style>