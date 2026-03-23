<template>
  <teleport to="body">
    <div v-if="aperta" class="modal fade show d-block" tabindex="-1" style="background:rgba(0,0,0,.5)">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">Modifica slot</h5>
            <button type="button" class="btn-close" @click="chiudi"></button>
          </div>

          <div class="modal-body">
            <!-- <div v-if="slot?.isMassiva" class="alert alert-info py-2 small mb-3">
              <svg class="icon icon-sm me-1"><use :href="sprites + '#it-info-circle'"></use></svg>
              Questo slot appartiene a una prenotazione ricorrente.
              Tutte le modifiche si applicano <strong>solo a questo slot</strong>.
            </div> -->

            <div v-if="esito" class="alert" :class="esito.tipo === 'ok' ? 'alert-success' : 'alert-danger'">
              {{ esito.msg }}
            </div>

            <div class="row g-3">
              <!-- Sede -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Sede *</label>
                <select v-model="form.sede_id" class="form-select"
                  :class="{ 'is-invalid': err.sede_id }" @change="onSedeChange">
                  <option value="">— seleziona —</option>
                  <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
                </select>
                <div class="invalid-feedback">{{ err.sede_id }}</div>
              </div>

              <!-- Aula -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Aula *</label>
                <select v-model="form.aula_id" class="form-select"
                  :class="{ 'is-invalid': err.aula_id }"
                  :disabled="!form.sede_id || caricandoAule">
                  <option value="">{{ caricandoAule ? 'Caricamento…' : '— seleziona sede prima —' }}</option>
                  <option v-for="a in aule" :key="a.id" :value="a.id">
                    {{ a.nome }} (cap. {{ a.capienza }})
                  </option>
                </select>
                <div class="invalid-feedback">{{ err.aula_id }}</div>
              </div>

              <!-- Corso ID -->
              <div class="col-12">
                <label class="form-label fw-semibold">Titolo Corso (ID) *</label>
                <input v-model.number="form.corso_id" type="number" min="1"
                  class="form-control" :class="{ 'is-invalid': err.corso_id }" />
                <div class="invalid-feedback">{{ err.corso_id }}</div>
              </div>

              <!-- Data -->
              <div class="col-md-4">
                <label class="form-label fw-semibold">Data *</label>
                <input v-model="form.data" type="date" class="form-control"
                  :class="{ 'is-invalid': err.data }" />
                <div class="invalid-feedback">{{ err.data }}</div>
              </div>

              <!-- Ora inizio -->
              <div class="col-md-4">
                <label class="form-label fw-semibold">Ora inizio *</label>
                <select v-model="form.ora_inizio" class="form-select"
                  :class="{ 'is-invalid': err.ora_inizio }">
                  <option value="">—</option>
                  <option v-for="h in oreSlot" :key="h" :value="h">{{ h }}</option>
                </select>
                <div class="invalid-feedback">{{ err.ora_inizio }}</div>
              </div>

              <!-- Ora fine -->
              <div class="col-md-4">
                <label class="form-label fw-semibold">Ora fine *</label>
                <select v-model="form.ora_fine" class="form-select"
                  :class="{ 'is-invalid': err.ora_fine }">
                  <option value="">—</option>
                  <option v-for="h in oreSlot" :key="h" :value="h">{{ h }}</option>
                </select>
                <div class="invalid-feedback">{{ err.ora_fine }}</div>
              </div>

              <!-- Note -->
              <div class="col-12">
                <label class="form-label fw-semibold">Note</label>
                <textarea v-model="form.note" class="form-control" rows="2"
                  placeholder="es. DOCENTE - ATTREZZATURE - Altro"></textarea>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-outline-secondary" @click="chiudi" :disabled="loading">Annulla</button>
            <button class="btn btn-primary" @click="submit" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
              Salva modifiche
            </button>
          </div>

        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { getAuleBySede } from '@/api/aule'
import { modificaSlot } from '@/api/prenotazioni'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const props = defineProps({
  aperta:  Boolean,
  slot:    Object,  // riga dalla tabella MiePrenotazioni
  sedi:    Array,
  aulaMap: Object,  // { aulaId: { sede_id, ... } }
})
const emit = defineEmits(['update:aperta', 'salvato'])

const loading       = ref(false)
const caricandoAule = ref(false)
const aule          = ref([])
const esito         = ref(null)

const oreSlot = Array.from({ length: 29 }, (_, i) => {
  const totalMin = 7 * 60 + i * 30
  return `${String(Math.floor(totalMin / 60)).padStart(2, '0')}:${String(totalMin % 60).padStart(2, '0')}`
})

const form = reactive({
  sede_id: '', aula_id: '', corso_id: null,
  data: '', ora_inizio: '', ora_fine: '', note: '',
})
const err = reactive({
  sede_id: '', aula_id: '', corso_id: '',
  data: '', ora_inizio: '', ora_fine: '',
})

watch(() => props.aperta, async (val) => {
  if (!val || !props.slot) return
  esito.value = null
  Object.keys(err).forEach(k => err[k] = '')

  const s = props.slot
  const sedeId = props.aulaMap?.[s.aulaId]?.sede_id || ''

  Object.assign(form, {
    sede_id:    sedeId,
    aula_id:    s.aulaId,
    corso_id:   s.corsoId,
    data:       s.data,
    ora_inizio: s.oraInizio.slice(0, 5),
    ora_fine:   s.oraFine.slice(0, 5),
    note:       s.note || '',
  })

  if (sedeId) {
    caricandoAule.value = true
    try { aule.value = await getAuleBySede(sedeId) || [] }
    finally { caricandoAule.value = false }
  }
})

async function onSedeChange() {
  form.aula_id = ''
  aule.value = []
  if (!form.sede_id) return
  caricandoAule.value = true
  try { aule.value = await getAuleBySede(form.sede_id) || [] }
  finally { caricandoAule.value = false }
}

function valida() {
  err.sede_id    = form.sede_id    ? '' : 'Obbligatorio'
  err.aula_id    = form.aula_id    ? '' : 'Obbligatorio'
  err.corso_id   = form.corso_id   ? '' : 'Obbligatorio'
  err.data       = form.data       ? '' : 'Obbligatorio'
  err.ora_inizio = form.ora_inizio ? '' : 'Obbligatorio'
  err.ora_fine   = form.ora_fine   ? '' : 'Obbligatorio'
  if (form.ora_inizio && form.ora_fine && form.ora_inizio >= form.ora_fine)
    err.ora_fine = "Deve essere dopo l'ora di inizio"
  return !Object.values(err).some(Boolean)
}

async function submit() {
  if (!valida()) return
  loading.value = true
  esito.value = null
  try {
    await modificaSlot(props.slot.prenId, props.slot.slotId, {
      aula_id:    form.aula_id,
      corso_id:   form.corso_id,
      data:       form.data,
      ora_inizio: form.ora_inizio,
      ora_fine:   form.ora_fine,
      note:       form.note || null,
    })
    esito.value = { tipo: 'ok', msg: '✓ Slot aggiornato con successo.' }
    emit('salvato')
    setTimeout(chiudi, 1200)
  } catch (e) {
    esito.value = { tipo: 'err', msg: e.message }
  } finally {
    loading.value = false
  }
}

function chiudi() { emit('update:aperta', false) }
</script>