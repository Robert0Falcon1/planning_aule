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
        <select v-model="filtroAula" class="form-select form-select-sm" style="width:auto" :disabled="!filtroSede">
          <option value="">Tutte le aule</option>
          <option v-for="a in auleFiltrate" :key="a.id" :value="a.id">{{ a.nome }}</option>
        </select>

        <!-- Filtro utente (solo COORDINAMENTO) -->
        <select v-if="authStore.isCoordinamento" v-model="filtroUtente" class="form-select form-select-sm"
          style="width:auto">
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

        <!-- Filtro ID Corso -->
        <input v-model.number="filtroCorso" type="number" class="form-control form-control-sm" style="width:180px"
          placeholder="Titolo Corso (ID)" />

        <!-- Filtro date -->
        <input v-model="filtroDa" type="date" class="form-control form-control-sm" style="width:auto" />
        <span class="text-muted small">→</span>
        <input v-model="filtroA" type="date" class="form-control form-control-sm" style="width:auto" />
        <button class="btn btn-sm btn-outline-secondary" @click="resetFiltri">Reset</button>

        <RouterLink :to="{ name: 'NuovaPrenotazione' }" class="btn btn-sm btn-primary">
          <svg class="icon icon-white icon-sm me-1">
            <use :href="sprites + '#it-plus-circle'"></use>
          </svg>
          Nuova
        </RouterLink>
      </div>
    </div>

    <!-- KPI -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-md-4">
        <div class="card border-0 shadow-sm text-center py-3">
          <div class="fs-3 fw-bold text-primary">{{ conteggioSlot }}</div>
          <div class="small text-muted">Prenotazioni totali</div>
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
                <th>Corso&nbsp;ID</th>
                <th>Note</th>
                <th v-if="authStore.isCoordinamento">Prenotato&nbsp;da</th>
                <th>Conflitti</th>
                <th class="text-end">Azioni</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="slot in paginaCorrente" :key="slot.key" :class="{ 'row-conflitto': slot.haConflitti }"
                @click="vaiACalendario(slot.data)" style="cursor: pointer;">

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

                <td>
                  <span v-if="slot.note" class="small text-muted fst-italic">{{ slot.note }}</span>
                  <span v-else class="text-muted small">—</span>
                </td>

                <!-- Colonna richiedente (solo COORDINAMENTO) -->
                <td v-if="authStore.isCoordinamento">
                  <span class="small">{{ nomeUtente(slot.richiedenteId) }}</span>
                </td>

                <td>
                  <span v-if="slot.haConflitti" class="badge bg-danger d-flex justify-content-center width-fit-content">
                    <svg class="icon icon-xs icon-white me-1">
                      <use :href="sprites + '#it-error'"></use>
                    </svg>
                    Sì
                  </span>
                  <span v-else class="text-muted small">—</span>
                </td>

                <td class="text-end">
                  <div class="d-flex gap-1 justify-content-end">
                    <button class="btn btn-sm btn-outline-primary" @click.stop="apriModifica(slot)"
                      title="Modifica prenotazione">
                      <svg class="icon icon-sm">
                        <use :href="sprites + '#it-pencil'"></use>
                      </svg>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" :disabled="cancellando === slot.prenId"
                      @click.stop="richiediCancellazione(slot)">
                      <span v-if="cancellando === slot.prenId" class="spinner-border spinner-border-sm"></span>
                      <svg v-else class="icon icon-sm">
                        <use :href="sprites + '#it-delete'"></use>
                      </svg>
                    </button>
                  </div>
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
        <!-- <div v-if="modalCancella.isMassiva" class="alert alert-info py-2 small mb-3">
          <svg class="icon icon-sm me-1"><use :href="sprites + '#it-info-circle'"></use></svg>
          Questo slot fa parte di una prenotazione ricorrente con
          <strong>{{ modalCancella.totaleSlot }} slot</strong> totali.
          Puoi eliminare solo questo slot oppure tutti.
        </div> -->

        <div class="d-flex gap-2 justify-content-end flex-wrap">
          <button class="btn btn-secondary" @click="modalCancella = null">Annulla</button>
          <button class="btn btn-danger" @click="confermaCancellazione(false)" :disabled="!!cancellando">
            <span v-if="cancellando" class="spinner-border spinner-border-sm me-1"></span>
            Elimina
          </button>
        </div>
      </div>
    </div>
  </div>
  <ModificaSlotModal v-model:aperta="modalModifica" :slot="slotInModifica" :sedi="sedi" :aula-map="aulaMap"
    @salvato="caricaTutto" />
</template>

<script setup>
import { ref, computed, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getMiePrenotazioni, cancellaPrenotazione, annullaSlot, getConflitti } from '@/api/prenotazioni'
import { getUtenti } from '@/api/utenti'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { useAule } from '@/composables/useAule'
import { formatData, oggi } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import ModificaSlotModal from '@/components/layout/ModificaSlotModal.vue'


const router = useRouter()
const authStore = useAuthStore()
const { nomeAula: nomeAulaFn, sedeDiAula: sedeDiAulaFn, carica: caricaAule } = useAule()

const loading = ref(false)
const prenotazioni = ref([])
const sedi = ref([])
const aule = ref([])
const utenti = ref([])
const filtroSede = ref('')
const filtroAula = ref('')
const filtroUtente = ref('')
const filtroStato = ref('')
const filtroCorso = ref('')
const filtroDa = ref(oggi())
const filtroA = ref('')
const pagina = ref(1)
const PER_PAGINA = 20
const cancellando = ref(null)
const modalCancella = ref(null)
const conflittiAttivi = ref([])
const modalModifica = ref(false)
const slotInModifica = ref(null)

const titoloPageina = computed(() =>
  authStore.isCoordinamento ? 'Prenotazioni' : 'Mie Prenotazioni'
)

const auleFiltrate = computed(() =>
  filtroSede.value !== ''
    ? aule.value.filter(a => String(a.sede_id) === String(filtroSede.value))
    : aule.value
)
function onSedeChange() { filtroAula.value = '' }

// ── Set slot ID con conflitti attivi ─────────────────────────────────────────
// Check preciso slot-level: usa solo slot_id_1/slot_id_2 dai conflitti NON_RISOLTO.
// I conflitti senza slot_id (dati vecchi) vanno rigenerati con rigenera_conflitti.py.
const slotIdConConflitti = computed(() => {
  const s = new Set()
  for (const cf of conflittiAttivi.value) {
    if (cf.slot_id_1) s.add(cf.slot_id_1)
    if (cf.slot_id_2) s.add(cf.slot_id_2)
  }
  return s
})

// ── Mappa utenti per lookup ───────────────────────────────────────────────────
const mappaUtenti = computed(() =>
  Object.fromEntries(utenti.value.map(u => [u.id, u]))
)

const aulaMap = computed(() =>
  Object.fromEntries(aule.value.map(a => [a.id, a]))
)

function nomeUtente(id) {
  const u = mappaUtenti.value[id]
  return u ? `${u.nome} ${u.cognome}` : `#${id}`
}

function apriModifica(slot) {
  slotInModifica.value = slot
  modalModifica.value = true
}

const tuttiGliSlot = computed(() => {
  const ids = slotIdConConflitti.value
  const list = []
  for (const p of prenotazioni.value) {
    if (!authStore.isCoordinamento && authStore.utente?.id) {
      if (p.richiedente_id !== authStore.utente.id) continue
    }
    const isMassiva = p.tipo === 'massiva'
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]
      if (!slot?.data || slot.annullato) continue
      list.push({
        key: `${p.id}-${si}`,
        prenId: p.id,
        slotId: slot.id,
        slotIdx: si,
        aulaId: slot.aula_id,    // ← da slot
        corsoId: slot.corso_id,   // ← da slot
        note: slot.note || '', // ← da slot
        richiedenteId: p.richiedente_id,
        haConflitti: ids.has(slot.id),
        isMassiva,
        totaleSlot: p.slots.length,
        data: slot.data,
        oraInizio: slot.ora_inizio?.slice(0, 5) || '—',
        oraFine: slot.ora_fine?.slice(0, 5) || '—',
      })
    }
  }
  return list.sort((a, b) => a.data > b.data ? 1 : a.data < b.data ? -1 : 0)
})

// ── Slot filtrati ─────────────────────────────────────────────────────────────
const slotFiltrati = computed(() => {
  let list = tuttiGliSlot.value

  if (filtroAula.value !== '') {
    list = list.filter(s => String(s.aulaId) === String(filtroAula.value))
  } else if (filtroSede.value !== '') {
    const ids = new Set(
      aule.value
        .filter(a => String(a.sede_id) === String(filtroSede.value))
        .map(a => String(a.id))
    )
    list = list.filter(s => ids.has(String(s.aulaId)))
  }

  if (filtroUtente.value) {
    list = list.filter(s => Number(s.richiedenteId) === Number(filtroUtente.value))
  }

  if (filtroStato.value === 'conflitto') {
    list = list.filter(s => s.haConflitti)
  } else if (filtroStato.value === 'confermata') {
    list = list.filter(s => !s.haConflitti)
  }

  if (filtroCorso.value) {
    list = list.filter(s => Number(s.corsoId) === Number(filtroCorso.value))
  }

  if (filtroDa.value) list = list.filter(s => s.data >= filtroDa.value)
  if (filtroA.value) list = list.filter(s => s.data <= filtroA.value)

  return list
})

const paginaCorrente = computed(() => {
  const ini = (pagina.value - 1) * PER_PAGINA
  return slotFiltrati.value.slice(ini, ini + PER_PAGINA)
})

const totalePagine = computed(() => Math.ceil(slotFiltrati.value.length / PER_PAGINA) || 1)
const conteggioSlot = computed(() => tuttiGliSlot.value.length)
// Conta conflitti DISTINTI che coinvolgono le prenotazioni dell'utente corrente
// (non gli slot, per evitare doppio conteggio: 1 conflitto = 2 slot marcati)

// Conta gli slot con conflitti — coerente con "Slot totali" e la tabella.
// tuttiGliSlot è già filtrato per utente (OPERATIVO) o globale (COORDINAMENTO)
// e ha haConflitti corretto (slot-level per COORD, richiesta.ha_conflitti per OPERATIVO).
const conteggioConflitti = computed(() =>
  tuttiGliSlot.value.filter(s => s.haConflitti).length
)

function resetFiltri() {
  filtroSede.value = ''; filtroAula.value = ''; filtroUtente.value = ''
  filtroStato.value = ''; filtroCorso.value = ''
  filtroStato.value = ''; filtroDa.value = ''; filtroA.value = ''
  pagina.value = 1
}

function richiediCancellazione(slot) { modalCancella.value = slot }

async function confermaCancellazione(eliminaTutti = true) {
  const slot = modalCancella.value; if (!slot) return
  cancellando.value = slot.prenId
  try {
    if (!eliminaTutti && slot.isMassiva) {
      await annullaSlot(slot.prenId, slot.slotId)
    } else {
      await cancellaPrenotazione(slot.prenId)
    }
    modalCancella.value = null
    await caricaTutto()  // ricarica prenotazioni + conflitti
  } catch (e) {
    alert(`Errore: ${e.message}`)
  } finally {
    cancellando.value = null
  }
}

async function caricaTutto() {
  loading.value = true
  try {
    const calls = [getSedi(), getAule(), getMiePrenotazioni(), getConflitti({ solo_attivi: true })]
    if (authStore.isCoordinamento) calls.push(getUtenti())
    const results = await Promise.all(calls)
    const [dataSedi, dataAule, dataPren, dataConflitti] = results
    const dataUtenti = results[4]
    sedi.value = Array.isArray(dataSedi) ? dataSedi : []
    aule.value = Array.isArray(dataAule) ? dataAule : []
    prenotazioni.value = Array.isArray(dataPren) ? dataPren : (dataPren?.items || [])
    conflittiAttivi.value = Array.isArray(dataConflitti) ? dataConflitti : (dataConflitti?.items || [])

    if (dataUtenti) utenti.value = Array.isArray(dataUtenti) ? dataUtenti : []
  } catch (e) {
    console.warn('MiePrenotazioni:', e.message)
  } finally {
    loading.value = false
  }
}

// ── Naviga al calendario sulla data esatta ───────────────────────────────────
function vaiACalendario(data) {
  router.push({ name: 'Calendario', query: { data } })
}

onMounted(async () => {
  await caricaAule()
  await caricaTutto()
})

// Ricarica ogni volta che si torna sulla pagina (es. dopo aver risolto un conflitto)
onActivated(caricaTutto)
</script>

<style scoped>
.page-title {
  font-size: 1.4rem;
  font-weight: 700;
}

.row-conflitto {
  background: #fff3f3 !important;
}

.modal-backdrop-custom {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, .45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-dialog-custom {
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
}
</style>