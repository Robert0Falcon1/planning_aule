<template>
  <div class="page-prenotazione">
    <div class="page-header mb-4">
      <h2 class="page-title">Nuova Prenotazione</h2>
    </div>

    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <button class="nav-link" :class="{ active: tab === 'singola' }" @click="tab = 'singola'">
          <svg class="icon icon-sm me-1">
            <use :href="sprites + '#it-calendar'"></use>
          </svg>
          Prenotazione singola
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link" :class="{ active: tab === 'massiva' }" @click="tab = 'massiva'">
          <svg class="icon icon-sm me-1">
            <use :href="sprites + '#it-files'"></use>
          </svg>
          Prenotazione massiva
        </button>
      </li>
    </ul>

    <!-- ── SINGOLA ─────────────────────────────────────────────────────────── -->
    <div v-if="tab === 'singola'">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <form @submit.prevent="submitSingola" novalidate>
            <div class="row g-3">

              <!-- Sede -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Sede *</label>
                <select v-model="singola.sede_id" class="form-select" :class="{ 'is-invalid': err.sede_id }"
                  @change="onSedeChange">
                  <option value="">— seleziona —</option>
                  <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
                </select>
                <div class="invalid-feedback">{{ err.sede_id }}</div>
              </div>

              <!-- Aula -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Aula *</label>
                <select v-model="singola.aula_id" class="form-select" :class="{ 'is-invalid': err.aula_id }"
                  :disabled="!singola.sede_id || caricandoAule">
                  <option value="">{{ caricandoAule ? 'Caricamento…' : '— seleziona sede prima —' }}</option>
                  <option v-for="a in aule" :key="a.id" :value="a.id">{{ a.nome }} (cap. {{ a.capienza }})</option>
                </select>
                <div class="invalid-feedback">{{ err.aula_id }}</div>
              </div>

              <!-- Corso&nbsp;ID -->
              <div class="col-12">
                <label class="form-label fw-semibold">Titolo Corso (ID) *</label>
                <input v-model.number="singola.corso_id" type="number" min="1" class="form-control"
                  :class="{ 'is-invalid': err.corso_id }" placeholder="Inserisci l'ID del corso" />
                <div class="invalid-feedback">{{ err.corso_id }}</div>
                <div class="form-text text-muted">Inserisci l'ID numerico del corso dalla piattaforma.</div>

                <!-- <select v-model="form.corso_id">
                  <option v-for="c in corsi" :key="c.id" :value="c.id">
                    {{ c.codice }} — {{ c.titolo }}
                  </option>
                </select> -->

              </div>

              <!-- Data -->
              <div class="col-md-4">
                <label class="form-label fw-semibold">Data *</label>
                <input v-model="singola.data" type="date" class="form-control" :class="{ 'is-invalid': err.data }"
                  :min="oggiISO" />
                <div class="invalid-feedback">{{ err.data }}</div>
              </div>

              <!-- Ora inizio -->
              <div class="col-md-4">
                <label class="form-label fw-semibold">Ora inizio *</label>
                <select v-model="singola.ora_inizio" class="form-select" :class="{ 'is-invalid': err.ora_inizio }">
                  <option value="">—</option>
                  <option v-for="h in oreSlot" :key="h" :value="h">{{ h }}</option>
                </select>
                <div class="invalid-feedback">{{ err.ora_inizio }}</div>
              </div>

              <!-- Ora fine -->
              <div class="col-md-4">
                <label class="form-label fw-semibold">Ora fine *</label>
                <select v-model="singola.ora_fine" class="form-select" :class="{ 'is-invalid': err.ora_fine }">
                  <option value="">—</option>
                  <option v-for="h in oreSlot" :key="h" :value="h">{{ h }}</option>
                </select>
                <div class="invalid-feedback">{{ err.ora_fine }}</div>
              </div>

              <!-- Note -->
              <div class="col-12">
                <label class="form-label fw-semibold">Note</label>
                <textarea v-model="singola.note" class="form-control" rows="2"
                  placeholder="es. DOCENTE - ATTREZZATURE - Altro"></textarea>
              </div>
            </div>

            <div v-if="esito" class="alert mt-3" :class="esito.tipo === 'ok' ? 'alert-success' : 'alert-danger'">
              {{ esito.msg }}
            </div>

            <div class="mt-4 d-flex gap-2">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                Conferma prenotazione
              </button>
              <button type="button" class="btn btn-outline-secondary" @click="resetSingola">Pulisci</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- ── MASSIVA ─────────────────────────────────────────────────────────── -->
    <div v-else>
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <p class="text-muted mb-4 small">
            Prenota la stessa aula in modo ricorrente (es. ogni lunedì e mercoledì per un mese).
          </p>
          <form @submit.prevent="submitMassiva" novalidate>
            <div class="row g-3">

              <div class="col-md-6">
                <label class="form-label fw-semibold">Sede *</label>
                <select v-model="massiva.sede_id" class="form-select" :class="{ 'is-invalid': errM.sede_id }"
                  @change="onSedeChangeMassiva">
                  <option value="">— seleziona —</option>
                  <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
                </select>
                <div class="invalid-feedback">{{ errM.sede_id }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Aula *</label>
                <select v-model="massiva.aula_id" class="form-select" :class="{ 'is-invalid': errM.aula_id }"
                  :disabled="!massiva.sede_id">
                  <option value="">— seleziona sede prima —</option>
                  <option v-for="a in auleMassiva" :key="a.id" :value="a.id">{{ a.nome }}</option>
                </select>
                <div class="invalid-feedback">{{ errM.aula_id }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Titolo Corso (ID) *</label>
                <input v-model.number="massiva.corso_id" type="number" min="1" class="form-control"
                  :class="{ 'is-invalid': errM.corso_id }" placeholder="ID numerico corso" />
                <div class="invalid-feedback">{{ errM.corso_id }}</div>
              </div>

              <div class="col-md-3">
                <label class="form-label fw-semibold">Ora inizio *</label>
                <select v-model="massiva.ora_inizio" class="form-select" :class="{ 'is-invalid': errM.ora_inizio }">
                  <option value="">—</option>
                  <option v-for="h in oreSlot" :key="h" :value="h">{{ h }}</option>
                </select>
                <div class="invalid-feedback">{{ errM.ora_inizio }}</div>
              </div>

              <div class="col-md-3">
                <label class="form-label fw-semibold">Ora fine *</label>
                <select v-model="massiva.ora_fine" class="form-select" :class="{ 'is-invalid': errM.ora_fine }">
                  <option value="">—</option>
                  <option v-for="h in oreSlot" :key="h" :value="h">{{ h }}</option>
                </select>
                <div class="invalid-feedback">{{ errM.ora_fine }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Data inizio *</label>
                <input v-model="massiva.data_inizio" type="date" class="form-control"
                  :class="{ 'is-invalid': errM.data_inizio }" :min="oggiISO" />
                <div class="invalid-feedback">{{ errM.data_inizio }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Data fine *</label>
                <input v-model="massiva.data_fine" type="date" class="form-control"
                  :class="{ 'is-invalid': errM.data_fine }" :min="massiva.data_inizio || oggiISO" />
                <div class="invalid-feedback">{{ errM.data_fine }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Tipo ricorrenza *</label>
                <select v-model="massiva.tipo_ricorrenza" class="form-select">
                  <option value="settimanale">Settimanale</option>
                  <option value="bisettimanale">Bisettimanale</option>
                </select>
              </div>

              <!-- Giorni settimana (solo se settimanale/bisettimanale) -->
              <div v-if="massiva.tipo_ricorrenza === 'settimanale' || massiva.tipo_ricorrenza === 'bisettimanale'"
                class="col-12">
                <label class="form-label fw-semibold">Giorni della settimana *</label>
                <div class="d-flex flex-wrap gap-2 align-items-center">
                  <div v-for="(nome, idx) in nomiGiorni" :key="idx" class="form-check form-check-inline my-0">
                    <input class="form-check-input" type="checkbox" :id="`g${idx}`" :value="idx + 1"
                      v-model="massiva.giorni_settimana" />
                    <label class="form-check-label" :for="`g${idx}`">{{ nome }}</label>
                  </div>
                </div>
                <div v-if="errM.giorni_settimana" class="text-danger small mt-1">{{ errM.giorni_settimana }}</div>
              </div>

              <div class="col-12">
                <label class="form-label fw-semibold">Note</label>
                <textarea v-model="massiva.note" class="form-control" rows="2"
                  placeholder="es. DOCENTE - ATTREZZATURE - Altro"></textarea>
              </div>
            </div>

            <div v-if="esitoMassiva" class="alert mt-3"
              :class="esitoMassiva.tipo === 'ok' ? 'alert-success' : 'alert-danger'">
              {{ esitoMassiva.msg }}
            </div>

            <div class="mt-4 d-flex gap-2">
              <button type="submit" class="btn btn-primary" :disabled="loadingMassiva">
                <span v-if="loadingMassiva" class="spinner-border spinner-border-sm me-1"></span>
                Crea prenotazioni ricorrenti
              </button>
              <button type="button" class="btn btn-outline-secondary" @click="resetMassiva">Pulisci</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getSedi } from '@/api/sedi'
import { getAuleBySede } from '@/api/aule'
import { creaPrenotazione, creaPrenotazioneMassiva } from '@/api/prenotazioni'
import { oggi } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const route = useRoute()
const tab = ref(route.query.tipo === 'massiva' ? 'massiva' : 'singola')
const oggiISO = oggi()
const loading = ref(false)
const loadingMassiva = ref(false)
const caricandoAule = ref(false)
const sedi = ref([])
const aule = ref([])
const auleMassiva = ref([])
const esito = ref(null)
const esitoMassiva = ref(null)
const nomiGiorni = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']

const oreSlot = Array.from({ length: 29 }, (_, i) => {
  const totalMin = 7 * 60 + i * 30
  return `${String(Math.floor(totalMin / 60)).padStart(2, '0')}:${String(totalMin % 60).padStart(2, '0')}`
})

const singola = reactive({
  sede_id: '', aula_id: '', corso_id: null,
  data: '', ora_inizio: '09:00', ora_fine: '13:00', note: '',
})

const err = reactive({
  sede_id: '', aula_id: '', corso_id: '', data: '', ora_inizio: '', ora_fine: '',
})

const errM = reactive({
  sede_id: '', aula_id: '', corso_id: '', ora_inizio: '', ora_fine: '',
  data_inizio: '', data_fine: '', giorni_settimana: '',
})

const massiva = reactive({
  sede_id: '', aula_id: '', corso_id: null,
  data_inizio: '', data_fine: '',
  ora_inizio: '09:00', ora_fine: '13:00',
  tipo_ricorrenza: 'settimanale',
  giorni_settimana: [],
  note: '',
})

// ── AUTO-AGGIORNAMENTO ORA FINE (14:00 → 18:00) ──────────────────────────

watch(() => singola.ora_inizio, (nuovaOra) => {
  if (nuovaOra === '14:00') {
    singola.ora_fine = '18:00'
  }
})

watch(() => massiva.ora_inizio, (nuovaOra) => {
  if (nuovaOra === '14:00') {
    massiva.ora_fine = '18:00'
  }
})

async function onSedeChange() {
  singola.aula_id = ''; aule.value = []
  if (!singola.sede_id) return
  caricandoAule.value = true
  try {
    const data = await getAuleBySede(singola.sede_id)
    aule.value = data || []
  } finally {
    caricandoAule.value = false
  }
}

async function onSedeChangeMassiva() {
  massiva.aula_id = ''; auleMassiva.value = []
  if (!massiva.sede_id) return
  const data = await getAuleBySede(massiva.sede_id)
  auleMassiva.value = data || []
}

function validaSingola() {
  err.sede_id = singola.sede_id ? '' : 'Obbligatorio'
  err.aula_id = singola.aula_id ? '' : 'Obbligatorio'
  err.corso_id = singola.corso_id ? '' : 'Obbligatorio'
  err.data = singola.data ? '' : 'Obbligatorio'
  err.ora_inizio = singola.ora_inizio ? '' : 'Obbligatorio'
  err.ora_fine = singola.ora_fine ? '' : 'Obbligatorio'
  if (singola.ora_inizio && singola.ora_fine && singola.ora_inizio >= singola.ora_fine)
    err.ora_fine = 'Deve essere dopo l\'ora di inizio'
  return !Object.values(err).some(Boolean)
}

async function submitSingola() {
  if (!validaSingola()) return
  loading.value = true; esito.value = null
  try {
    await creaPrenotazione({
      aula_id: singola.aula_id,
      corso_id: singola.corso_id,
      slot: {
        data: singola.data,
        ora_inizio: singola.ora_inizio,
        ora_fine: singola.ora_fine,
      },
      note: singola.note || undefined,
    })
    esito.value = { tipo: 'ok', msg: '✓ Prenotazione confermata con successo.' }
    resetSingola()
  } catch (e) {
    esito.value = { tipo: 'err', msg: e.message }
  } finally {
    loading.value = false
  }
}

function validaMassiva() {
  errM.sede_id = massiva.sede_id ? '' : 'Obbligatorio'
  errM.aula_id = massiva.aula_id ? '' : 'Obbligatorio'
  errM.corso_id = massiva.corso_id ? '' : 'Obbligatorio'
  errM.data_inizio = massiva.data_inizio ? '' : 'Obbligatorio'
  errM.data_fine = massiva.data_fine ? '' : 'Obbligatorio'
  errM.ora_inizio = massiva.ora_inizio ? '' : 'Obbligatorio'
  errM.ora_fine = massiva.ora_fine ? '' : 'Obbligatorio'
  if (!errM.ora_fine && massiva.ora_inizio >= massiva.ora_fine)
    errM.ora_fine = "Deve essere dopo l'ora di inizio"
  if (!errM.data_fine && massiva.data_inizio > massiva.data_fine)
    errM.data_fine = 'Deve essere uguale o successiva alla data di inizio'
  const needGiorni = massiva.tipo_ricorrenza === 'settimanale' || massiva.tipo_ricorrenza === 'bisettimanale'
  errM.giorni_settimana = (needGiorni && !massiva.giorni_settimana.length) ? 'Seleziona almeno un giorno' : ''
  return !Object.values(errM).some(Boolean)
}

async function submitMassiva() {
  if (!validaMassiva()) return
  loadingMassiva.value = true; esitoMassiva.value = null
  try {
    const payload = {
      aula_id: massiva.aula_id,
      corso_id: massiva.corso_id,
      data_inizio: massiva.data_inizio,
      data_fine: massiva.data_fine,
      ora_inizio: massiva.ora_inizio,
      ora_fine: massiva.ora_fine,
      tipo_ricorrenza: massiva.tipo_ricorrenza,
      giorni_settimana: massiva.giorni_settimana,
      note: massiva.note || undefined,
    }
    
    await creaPrenotazioneMassiva(payload)
    esitoMassiva.value = { tipo: 'ok', msg: '✓ Prenotazioni ricorrenti create con successo.' }
    massiva.giorni_settimana = []
  } catch (e) {
    esitoMassiva.value = { tipo: 'err', msg: e.message }
  } finally {
    loadingMassiva.value = false
  }
}

function resetSingola() {
  Object.assign(singola, { sede_id: '', aula_id: '', corso_id: null, data: '', ora_inizio: '09:00', ora_fine: '13:00', note: '' })
  Object.keys(err).forEach(k => (err[k] = ''))
  aule.value = []
}

function resetMassiva() {
  Object.assign(massiva, {
    sede_id: '',
    aula_id: '',
    corso_id: null,
    data_inizio: '',
    data_fine: '',
    ora_inizio: '09:00',
    ora_fine: '13:00',
    tipo_ricorrenza: 'settimanale',
    giorni_settimana: [],
    note: ''
  })
  Object.keys(errM).forEach(k => (errM[k] = ''))
  auleMassiva.value = []
  esitoMassiva.value = null
}

onMounted(async () => {
  const data = await getSedi()
  sedi.value = data || []
  if (route.query.sede_id) {
    singola.sede_id = Number(route.query.sede_id)
    await onSedeChange()
  }
  if (route.query.aula_id) singola.aula_id = Number(route.query.aula_id)
  if (route.query.data) singola.data = route.query.data
})
</script>

<style scoped>
.page-title {
  font-size: 1.4rem;
  font-weight: 700;
}
</style>