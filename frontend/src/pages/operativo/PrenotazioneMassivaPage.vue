<template>
  <div>
    <h2 class="h4 fw-bold mb-4">🔄 Prenotazione Massiva (Ricorrente)</h2>

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
                  <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }} ({{ s.citta }})</option>
                </select>
              </div>

              <!-- Aula -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Aula *</label>
                <select v-model="form.aula_id" class="form-select" :disabled="!form.sede_id">
                  <option value="">— Seleziona aula —</option>
                  <option v-for="a in aule" :key="a.id" :value="a.id">{{ a.nome }} (cap. {{ a.capienza }})</option>
                </select>
              </div>

              <!-- Corso -->
              <div class="mb-3">
                <label class="form-label fw-semibold">ID Corso *</label>
                <input v-model.number="form.corso_id" type="number" min="1" class="form-control" placeholder="Es: 1" />
                <div class="form-text">⚠️ Il corso deve esistere nel sistema.</div>
              </div>

              <!-- Periodo -->
              <div class="row mb-3">
                <div class="col-6">
                  <label class="form-label fw-semibold">Data inizio *</label>
                  <input v-model="form.data_inizio" type="date" class="form-control" :min="oggi()" />
                </div>
                <div class="col-6">
                  <label class="form-label fw-semibold">Data fine *</label>
                  <input v-model="form.data_fine" type="date" class="form-control" :min="form.data_inizio || oggi()" />
                </div>
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
                </div>
              </div>

              <!-- Tipo ricorrenza -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Tipo di ricorrenza *</label>
                <select v-model="form.tipo_ricorrenza" class="form-select">
                  <option v-for="t in TIPI_RICORRENZA" :key="t.value" :value="t.value">{{ t.label }}</option>
                </select>
              </div>

              <!-- Giorni della settimana -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Giorni della settimana *</label>
                <div class="d-flex flex-wrap gap-2 mt-1">
                  <div v-for="g in GIORNI_SETTIMANA" :key="g.value" class="form-check form-check-inline">
                    <input
                      :id="`g-${g.value}`"
                      v-model="form.giorni_settimana"
                      class="form-check-input"
                      type="checkbox"
                      :value="g.value"
                    />
                    <label :for="`g-${g.value}`" class="form-check-label">{{ g.label }}</label>
                  </div>
                </div>
              </div>

              <!-- Stima slot -->
              <div v-if="stimaSlot > 0" class="alert alert-info py-2 small mb-3">
                📊 Stima: <strong>{{ stimaSlot }} slot</strong> verranno generati.
              </div>

              <!-- Note -->
              <div class="mb-4">
                <label class="form-label fw-semibold">Note (opzionale)</label>
                <textarea v-model="form.note" class="form-control" rows="2" />
              </div>

              <!-- Errore backend -->
              <div v-if="erroreBackend" class="alert alert-danger py-2 small mb-3">
                <strong>Errore:</strong> {{ erroreBackend }}
              </div>

              <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="progress-spinner progress-spinner-sm me-2" role="status" />
                  {{ loading ? 'Invio in corso…' : '📤 Invia Richiesta Massiva' }}
                </button>
                <router-link :to="{ name: 'MiePrenotazioni' }" class="btn btn-outline-secondary">
                  Annulla
                </router-link>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Pannello avvertenza -->
      <div class="col-lg-5 mt-4 mt-lg-0">
        <div class="card border-0 bg-warning bg-opacity-10">
          <div class="card-body">
            <h6 class="fw-bold text-warning">⚠️ Attenzione</h6>
            <p class="small text-muted">
              La prenotazione massiva genera <strong>tutti gli slot in una volta</strong>.
              Verifica periodo, giorni e orario prima di confermare.
            </p>
            <hr />
            <p class="small text-muted mb-0">
              <strong>Esempio:</strong> Ogni Lunedì e Giovedì 9:00–13:00
              dal 3 marzo al 30 giugno → circa <strong>56 slot</strong>.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter }   from 'vue-router'
import { useUiStore }  from '@/stores/ui'
import { getSedi }     from '@/api/sedi'
import { getAule }     from '@/api/aule'
import { creaPrenotazioneMassiva } from '@/api/prenotazioni'
import { oggi }        from '@/utils/formatters'
import { estraiErrore } from '@/utils/errori'
import { TIPI_RICORRENZA, GIORNI_SETTIMANA } from '@/utils/constants'

const router  = useRouter()
const uiStore = useUiStore()

const sedi    = ref([])
const aule    = ref([])
const loading = ref(false)
const erroreBackend = ref('')

const form = reactive({
  sede_id:         '',
  aula_id:         '',
  corso_id:        '',
  data_inizio:     oggi(),
  data_fine:       '',
  ora_inizio:      '09:00',
  ora_fine:        '13:00',
  tipo_ricorrenza: 'settimanale',
  giorni_settimana: [],
  note:            '',
})

onMounted(async () => { sedi.value = await getSedi() })

async function onSedeChange() {
  form.aula_id = ''
  aule.value   = form.sede_id ? await getAule(form.sede_id) : []
}

/** Stima slot calcolata lato client */
const stimaSlot = computed(() => {
  if (!form.data_inizio || !form.data_fine || form.giorni_settimana.length === 0) return 0
  let count = 0
  const fine = new Date(form.data_fine)
  const cur  = new Date(form.data_inizio)
  while (cur <= fine) {
    const g = cur.getDay() === 0 ? 7 : cur.getDay()
    if (form.giorni_settimana.includes(g)) count++
    cur.setDate(cur.getDate() + 1)
  }
  return count
})

function valida() {
  erroreBackend.value = ''
  if (!form.aula_id)                      { uiStore.avviso('Seleziona sede e aula.');          return false }
  if (!form.corso_id)                     { uiStore.avviso('Inserisci l\'ID corso.');           return false }
  if (!form.data_inizio || !form.data_fine) { uiStore.avviso('Inserisci periodo completo.');   return false }
  if (form.data_fine < form.data_inizio)  { uiStore.avviso('La data fine deve essere dopo la data inizio.'); return false }
  if (form.ora_fine <= form.ora_inizio)   { uiStore.avviso('L\'ora fine deve essere dopo l\'ora inizio.');   return false }
  if (form.giorni_settimana.length === 0) { uiStore.avviso('Seleziona almeno un giorno della settimana.');    return false }
  return true
}

async function handleSubmit() {
  if (!valida()) return
  loading.value = true
  try {
    await creaPrenotazioneMassiva({
      aula_id:          Number(form.aula_id),
      corso_id:         Number(form.corso_id),
      data_inizio:      form.data_inizio,
      data_fine:        form.data_fine,
      ora_inizio:       form.ora_inizio,
      ora_fine:         form.ora_fine,
      tipo_ricorrenza:  form.tipo_ricorrenza,
      giorni_settimana: [...form.giorni_settimana].sort((a, b) => a - b),
      note:             form.note || null,
    })
    uiStore.successo(`Prenotazione massiva inviata! ${stimaSlot.value} slot generati.`)
    router.push({ name: 'MiePrenotazioni' })
  } catch (err) {
    erroreBackend.value = estraiErrore(err)
  } finally {
    loading.value = false
  }
}
</script>
