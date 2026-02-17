<template>
  <div>
    <h2 class="h4 fw-bold mb-4">📅 Nuova Prenotazione Singola</h2>

    <div class="row">
      <div class="col-lg-7">
        <div class="card border-0 shadow-sm">
          <div class="card-body p-4">
            <form @submit.prevent="handleSubmit" novalidate>

              <!-- Sede -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Sede *</label>
                <select v-model="form.sede_id" class="form-select" @change="onSedeChange">
                  <option value="">— Seleziona sede —</option>
                  <option v-for="s in sedi" :key="s.id" :value="s.id">
                    {{ s.nome }} ({{ s.citta }})
                  </option>
                </select>
              </div>

              <!-- Aula -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Aula *</label>
                <select v-model="form.aula_id" class="form-select" :disabled="!form.sede_id">
                  <option value="">— Seleziona aula —</option>
                  <option v-for="a in aule" :key="a.id" :value="a.id">
                    {{ a.nome }} (cap. {{ a.capienza }})
                  </option>
                </select>
              </div>

              <!-- Corso ID con avviso -->
              <div class="mb-3">
                <label class="form-label fw-semibold">ID Corso *</label>
                <input
                  v-model.number="form.corso_id"
                  type="number"
                  min="1"
                  class="form-control"
                  :class="{ 'is-invalid': erroreCorso }"
                  placeholder="Es: 1"
                />
                <div v-if="erroreCorso" class="invalid-feedback">{{ erroreCorso }}</div>
                <div class="form-text">
                  ⚠️ Il corso deve esistere nel sistema. Chiedere all'amministratore l'ID del proprio corso.
                </div>
              </div>

              <!-- Data -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Data *</label>
                <input v-model="form.data" type="date" class="form-control" :min="oggi()" />
              </div>

              <!-- Orario -->
              <div class="row mb-3">
                <div class="col-6">
                  <label class="form-label fw-semibold">Ora inizio *</label>
                  <input v-model="form.ora_inizio" type="time" class="form-control" />
                </div>
                <div class="col-6">
                  <label class="form-label fw-semibold">Ora fine *</label>
                  <input v-model="form.ora_fine" type="time" class="form-control" />
                  <div v-if="erroreOrario" class="text-danger small mt-1">{{ erroreOrario }}</div>
                </div>
              </div>

              <!-- Note -->
              <div class="mb-4">
                <label class="form-label fw-semibold">Note (opzionale)</label>
                <textarea v-model="form.note" class="form-control" rows="2" />
              </div>

              <!-- Errore dettagliato dal backend -->
              <div v-if="erroreBackend" class="alert alert-danger py-2 small mb-3">
                <strong>Errore:</strong> {{ erroreBackend }}
              </div>

              <!-- Submit -->
              <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="progress-spinner progress-spinner-sm me-2" role="status" />
                  {{ loading ? 'Invio in corso…' : '📤 Invia Richiesta' }}
                </button>
                <router-link :to="{ name: 'MiePrenotazioni' }" class="btn btn-outline-secondary">
                  Annulla
                </router-link>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Pannello laterale -->
      <div class="col-lg-5 mt-4 mt-lg-0">
        <!-- Guida -->
        <div class="card border-0 bg-light mb-3">
          <div class="card-body">
            <h6 class="fw-bold">💡 Come funziona</h6>
            <ol class="small text-muted mb-0">
              <li class="mb-1">Scegli sede e aula</li>
              <li class="mb-1">Inserisci l'ID del tuo corso</li>
              <li class="mb-1">Indica data e orario</li>
              <li class="mb-1">Invia: la Segreteria validerà la richiesta</li>
            </ol>
          </div>
        </div>

        <!-- Slot occupati in anteprima -->
        <div v-if="form.aula_id && form.data" class="card border-0 shadow-sm">
          <div class="card-header bg-white small fw-semibold">
            🔍 Occupazioni il {{ formatData(form.data) }}
          </div>
          <div class="card-body p-2">
            <LoadingSpinner v-if="loadingSlot" />
            <div v-else-if="slotOccupati.length === 0" class="text-success small p-2">
              ✅ Aula libera in questa data
            </div>
            <ul v-else class="list-unstyled small mb-0">
              <li
                v-for="s in slotOccupati"
                :key="`${s.prenotazione_id}-${s.ora_inizio}`"
                class="text-danger px-2 py-1 border-bottom"
              >
                🚫 {{ formatOra(s.ora_inizio) }} – {{ formatOra(s.ora_fine) }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { useRouter }                       from 'vue-router'
import { useUiStore }                      from '@/stores/ui'
import { getSedi }                         from '@/api/sedi'
import { getAule, getSlotOccupati }        from '@/api/aule'
import { creaPrenotazioneSingola }         from '@/api/prenotazioni'
import { formatData, formatOra, oggi }     from '@/utils/formatters'
import { estraiErrore }                    from '@/utils/errori'
import LoadingSpinner                      from '@/components/ui/LoadingSpinner.vue'

const router  = useRouter()
const uiStore = useUiStore()

const sedi         = ref([])
const aule         = ref([])
const loading      = ref(false)
const loadingSlot  = ref(false)
const slotOccupati = ref([])

// Errori specifici per campo e errore backend generico
const erroreCorso   = ref('')
const erroreOrario  = ref('')
const erroreBackend = ref('')

const form = reactive({
  sede_id:    '',
  aula_id:    '',
  corso_id:   '',
  data:       oggi(),
  ora_inizio: '09:00',
  ora_fine:   '13:00',
  note:       '',
})

onMounted(async () => { sedi.value = await getSedi() })

async function onSedeChange() {
  form.aula_id = ''
  aule.value   = []
  if (form.sede_id) aule.value = await getAule(form.sede_id)
}

// Aggiorna anteprima slot occupati al cambio aula o data
watch([() => form.aula_id, () => form.data], async ([aulaId, data]) => {
  if (!aulaId || !data) { slotOccupati.value = []; return }
  loadingSlot.value = true
  try {
    slotOccupati.value = await getSlotOccupati(aulaId, data, data)
  } finally {
    loadingSlot.value = false
  }
})

function valida() {
  erroreCorso.value  = ''
  erroreOrario.value = ''
  erroreBackend.value = ''

  if (!form.aula_id)  { uiStore.avviso('Seleziona una sede e un\'aula.'); return false }
  if (!form.corso_id) { erroreCorso.value = 'Inserisci l\'ID del corso.'; return false }
  if (!form.data)     { uiStore.avviso('Seleziona una data.'); return false }
  if (!form.ora_inizio || !form.ora_fine) { uiStore.avviso('Inserisci orario di inizio e fine.'); return false }
  if (form.ora_fine <= form.ora_inizio) {
    erroreOrario.value = 'L\'ora di fine deve essere successiva all\'ora di inizio.'
    return false
  }
  return true
}

async function handleSubmit() {
  if (!valida()) return

  loading.value = true
  erroreBackend.value = ''
  try {
    await creaPrenotazioneSingola({
      aula_id:  Number(form.aula_id),
      corso_id: Number(form.corso_id),
      slot: {
        data:       form.data,
        ora_inizio: form.ora_inizio,
        ora_fine:   form.ora_fine,
      },
      note: form.note || null,
    })
    uiStore.successo('Richiesta inviata! La Segreteria la esaminerà a breve.')
    router.push({ name: 'MiePrenotazioni' })
  } catch (err) {
    // Mostra il messaggio reale del backend (gestisce sia stringhe che array 422)
    erroreBackend.value = estraiErrore(err)
  } finally {
    loading.value = false
  }
}
</script>
