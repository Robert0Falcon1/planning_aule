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
          <span class="info-popover">
            <i class="bi bi-info-circle" style="font-size: .8rem;"></i>
            <span class="popover-content">
              Crea più prenotazioni contemporaneamente per date ricorrenti
            </span>
          </span>
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
              <!-- Corso — filtrato per sede -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Corso *</label>
                <select v-model="singola.corso_id" class="form-select" :class="{ 'is-invalid': err.corso_id }"
                  :disabled="caricandoCorsi || !singola.sede_id">
                  <option value="">
                    {{ caricandoCorsi ? 'Caricamento…' : (!singola.sede_id ? '— seleziona sede prima —' : '— seleziona —') }}
                  </option>
                  <option v-for="c in corsiPerSedeSingola" :key="c.id" :value="c.id">
                    {{ c.codice }} — {{ c.titolo }}
                  </option>
                </select>
                <div class="invalid-feedback">{{ err.corso_id }}</div>
                <div v-if="singola.sede_id && !caricandoCorsi && corsiPerSedeSingola.length === 0"
                  class="form-text text-warning">
                  Nessun corso disponibile per questa sede.
                </div>
              </div>
              <!-- Docente — filtrato per sede -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Docente *</label>
                <select v-model="singola.docente_id" class="form-select" :class="{ 'is-invalid': err.docente_id }"
                  :disabled="caricandoDocenti || !singola.sede_id">
                  <option value="">
                    {{ caricandoDocenti ? 'Caricamento…' : (!singola.sede_id ? '— seleziona sede prima —' : '— seleziona —') }}
                  </option>
                  <option v-for="d in docentiPerSede" :key="d.id" :value="d.id">
                    {{ d.cognome }} {{ d.nome }}
                  </option>
                </select>
                <div class="invalid-feedback">{{ err.docente_id }}</div>
                <div v-if="singola.sede_id && !caricandoDocenti && docentiPerSede.length === 0"
                  class="form-text text-warning">
                  Nessun docente disponibile per questa sede.
                </div>
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
                  placeholder="es. Attrezzature necessarie, richieste particolari..."></textarea>
              </div>
            </div>
            <div v-if="esito" class="alert mt-3" :class="esito.tipo === 'ok' ? 'alert-success' : 'alert-danger'">
              {{ esito.msg }}
            </div>
            <div v-if="alertConflitti" class="alert alert-warning mt-3">
              <svg class="icon icon-sm me-1">
                <use :href="sprites + '#it-error'"></use>
              </svg>
              {{ alertConflitti.msg }}
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
              <!-- Corso — filtrato per sede -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Corso *</label>
                <select v-model="massiva.corso_id" class="form-select" :class="{ 'is-invalid': errM.corso_id }"
                  :disabled="caricandoCorsi || !massiva.sede_id">
                  <option value="">
                    {{ caricandoCorsi ? 'Caricamento…' : (!massiva.sede_id ? '— seleziona sede prima —' : '— seleziona —') }}
                  </option>
                  <option v-for="c in corsiPerSedeMassiva" :key="c.id" :value="c.id">
                    {{ c.codice }} — {{ c.titolo }}
                  </option>
                </select>
                <div class="invalid-feedback">{{ errM.corso_id }}</div>
                <div v-if="massiva.sede_id && !caricandoCorsi && corsiPerSedeMassiva.length === 0"
                  class="form-text text-warning">
                  Nessun corso disponibile per questa sede.
                </div>
              </div>
              <!-- Docente — filtrato per sede -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Docente *</label>
                <select v-model="massiva.docente_id" class="form-select" :class="{ 'is-invalid': errM.docente_id }"
                  :disabled="caricandoDocenti || !massiva.sede_id">
                  <option value="">
                    {{ caricandoDocenti ? 'Caricamento…' : (!massiva.sede_id ? '— seleziona sede prima —' : '— seleziona —') }}
                  </option>
                  <option v-for="d in docentiPerSede" :key="d.id" :value="d.id">
                    {{ d.cognome }} {{ d.nome }}
                  </option>
                </select>
                <div class="invalid-feedback">{{ errM.docente_id }}</div>
                <div v-if="massiva.sede_id && !caricandoDocenti && docentiPerSede.length === 0"
                  class="form-text text-warning">
                  Nessun docente disponibile per questa sede.
                </div>
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
                  placeholder="es. Attrezzature necessarie, richieste particolari..."></textarea>
              </div>
            </div>
            <div v-if="esitoMassiva" class="alert mt-3"
              :class="esitoMassiva.tipo === 'ok' ? 'alert-success' : 'alert-danger'">
              {{ esitoMassiva.msg }}
            </div>
            <div v-if="alertConflitti" class="alert alert-warning mt-3">
              <svg class="icon icon-sm me-1">
                <use :href="sprites + '#it-error'"></use>
              </svg>
              {{ alertConflitti.msg }}
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
  <!-- Modal prima prenotazione -->
  <div v-if="mostraPrimaPrenotazione" class="modal-backdrop-celebration" @click="mostraPrimaPrenotazione = false">
    <div class="modal-celebration" @click.stop>
      <div class="celebration-icon">🎉</div>
      <h3 class="celebration-title">Complimenti, {{ auth.nomeUtenteInformale }}!</h3>
      <p class="celebration-text">Hai effettuato la tua prima prenotazione!</p>
      <button class="btn btn-primary" @click="mostraPrimaPrenotazione = false">Fantastico!</button>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getSedi } from '@/api/sedi'
import { getAuleBySede, getAule } from '@/api/aule'
import { creaPrenotazione, creaPrenotazioneMassiva } from '@/api/prenotazioni'
import { oggi } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import { useSedePerFiltro } from '@/composables/useSedePerFiltro'
import { useConflittiAlert } from '@/composables/useConflittiAlert'
import { useCorsi } from '@/composables/useCorsi'
import { useCorsiPerSede } from '@/composables/useCorsiPerSede'
import { useDocenti } from '@/composables/useDocenti'  // ← AGGIUNTO

const route = useRoute()
const auth = useAuthStore()
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
const mostraPrimaPrenotazione = ref(false)
const { sedeDefaultFiltro } = useSedePerFiltro()
const { alertConflitti, verificaConflittiNuovaPrenotazione, resetAlert } = useConflittiAlert()

// ── Composable corsi ─────────────────────────────────────────────────────────
const { corsiAttivi, caricandoCorsi, caricaCorsi } = useCorsi()

// ── Composable docenti ───────────────────────────────────────────────────────
const { docenti, docentiOrdinati, caricandoDocenti, caricaDocenti } = useDocenti()

// ── Form reactive — DEVONO stare PRIMA dei computed che li leggono ───────────
const singola = reactive({
  sede_id: '', aula_id: '', corso_id: '', docente_id: '',  // ← AGGIUNTO docente_id
  data: '', ora_inizio: '09:00', ora_fine: '13:00', note: '',
})
const massiva = reactive({
  sede_id: '', aula_id: '', corso_id: '', docente_id: '',  // ← AGGIUNTO docente_id
  data_inizio: '', data_fine: '',
  ora_inizio: '09:00', ora_fine: '13:00',
  tipo_ricorrenza: 'settimanale',
  giorni_settimana: [],
  note: '',
})
const err = reactive({
  sede_id: '', aula_id: '', corso_id: '', docente_id: '',  // ← AGGIUNTO
  data: '', ora_inizio: '', ora_fine: '',
})
const errM = reactive({
  sede_id: '', aula_id: '', corso_id: '', docente_id: '',  // ← AGGIUNTO
  ora_inizio: '', ora_fine: '',
  data_inizio: '', data_fine: '', giorni_settimana: '',
})

// ── Computed ref sede compatibili con useCorsiPerSede ────────────────────────
const sedeSingolaRef = computed(() => singola.sede_id)
const sedeMassivaRef = computed(() => massiva.sede_id)

// ── Composable filtro corsi per sede ─────────────────────────────────────────
const { corsiFiltrati: corsiFiltrati_singola } = useCorsiPerSede(corsiAttivi, sedi, sedeSingolaRef)
const { corsiFiltrati: corsiFiltrati_massiva } = useCorsiPerSede(corsiAttivi, sedi, sedeMassivaRef)

const corsiPerSedeSingola = computed(() =>
  [...corsiFiltrati_singola.value].sort((a, b) => a.codice.localeCompare(b.codice))
)
const corsiPerSedeMassiva = computed(() =>
  [...corsiFiltrati_massiva.value].sort((a, b) => a.codice.localeCompare(b.codice))
)

// ── Docenti filtrati per sede ────────────────────────────────────────────────
const docentiPerSede = computed(() => {
  if (!singola.sede_id && !massiva.sede_id) return []
  const sedeId = tab.value === 'singola' ? singola.sede_id : massiva.sede_id
  if (!sedeId) return []
  
  // Filtra docenti che operano nella sede selezionata
  return docentiOrdinati.value.filter(d => 
    d.sedi?.some(s => s.id === Number(sedeId))
  )
})

const oreSlot = Array.from({ length: 29 }, (_, i) => {
  const totalMin = 7 * 60 + i * 30
  return `${String(Math.floor(totalMin / 60)).padStart(2, '0')}:${String(totalMin % 60).padStart(2, '0')}`
})

// Reset corso/docente se sede cambia e non sono più nella lista
watch(corsiPerSedeSingola, (nuovaLista) => {
  if (singola.corso_id && !nuovaLista.some(c => c.id === singola.corso_id)) {
    singola.corso_id = ''
  }
})
watch(corsiPerSedeMassiva, (nuovaLista) => {
  if (massiva.corso_id && !nuovaLista.some(c => c.id === massiva.corso_id)) {
    massiva.corso_id = ''
  }
})
watch(docentiPerSede, (nuovaLista) => {
  if (singola.docente_id && !nuovaLista.some(d => d.id === singola.docente_id)) {
    singola.docente_id = ''
  }
  if (massiva.docente_id && !nuovaLista.some(d => d.id === massiva.docente_id)) {
    massiva.docente_id = ''
  }
})

async function checkPrimaPrenotazione() {
  const key = `prima_prenotazione_${auth.utente?.id}`
  if (localStorage.getItem(key)) return
  try {
    const { getPrenotazioni } = await import('@/api/prenotazioni')
    const response = await getPrenotazioni()
    const prenotazioniUtente = response?.items || response || []
    const miePrenotazioni = prenotazioniUtente.filter(p =>
      p.richiedente_id === auth.utente?.id &&
      p.stato === 'confermata' &&
      p.slots?.some(s => !s.annullato)
    )
    if (miePrenotazioni.length === 1) {
      mostraPrimaPrenotazione.value = true
      localStorage.setItem(key, 'true')
    }
  } catch (error) {
    console.warn('Errore verifica prima prenotazione:', error)
  }
}

watch(() => singola.ora_inizio, (nuovaOra) => {
  if (nuovaOra === '14:00') singola.ora_fine = '18:00'
})
watch(() => massiva.ora_inizio, (nuovaOra) => {
  if (nuovaOra === '14:00') massiva.ora_fine = '18:00'
})

async function onSedeChange() {
  singola.aula_id = ''
  singola.corso_id = ''
  singola.docente_id = ''  // ← AGGIUNTO reset docente
  aule.value = []
  if (!singola.sede_id) return
  caricandoAule.value = true
  try {
    const data = await getAuleBySede(singola.sede_id)
    aule.value = (data || []).filter(a => a.attiva !== false)
  } finally {
    caricandoAule.value = false
  }
}

async function onSedeChangeMassiva() {
  massiva.aula_id = ''
  massiva.corso_id = ''
  massiva.docente_id = ''  // ← AGGIUNTO reset docente
  auleMassiva.value = []
  if (!massiva.sede_id) return
  const data = await getAuleBySede(massiva.sede_id)
  auleMassiva.value = (data || []).filter(a => a.attiva !== false)
}

function validaSingola() {
  err.sede_id = singola.sede_id ? '' : 'Obbligatorio'
  err.aula_id = singola.aula_id ? '' : 'Obbligatorio'
  err.corso_id = singola.corso_id ? '' : 'Obbligatorio'
  err.docente_id = singola.docente_id ? '' : 'Obbligatorio'  // ← AGGIUNTO
  err.data = singola.data ? '' : 'Obbligatorio'
  err.ora_inizio = singola.ora_inizio ? '' : 'Obbligatorio'
  err.ora_fine = singola.ora_fine ? '' : 'Obbligatorio'
  if (singola.ora_inizio && singola.ora_fine && singola.ora_inizio >= singola.ora_fine)
    err.ora_fine = "Deve essere dopo l'ora di inizio"
  return !Object.values(err).some(Boolean)
}

async function submitSingola() {
  if (!validaSingola()) return
  loading.value = true
  esito.value = null
  resetAlert()
  try {
    const risposta = await creaPrenotazione({
      aula_id: singola.aula_id,
      corso_id: singola.corso_id,
      docente_id: singola.docente_id,  // ← AGGIUNTO
      slot: { data: singola.data, ora_inizio: singola.ora_inizio, ora_fine: singola.ora_fine },
      note: singola.note || undefined,
    })
    esito.value = { tipo: 'ok', msg: '✓ Prenotazione confermata con successo.' }
    if (risposta?.id) await verificaConflittiNuovaPrenotazione(risposta.id, 'singola')
    await checkPrimaPrenotazione()
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
  errM.docente_id = massiva.docente_id ? '' : 'Obbligatorio'  // ← AGGIUNTO
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
  loadingMassiva.value = true
  esitoMassiva.value = null
  resetAlert()
  try {
    const risposta = await creaPrenotazioneMassiva({
      aula_id: massiva.aula_id,
      corso_id: massiva.corso_id,
      docente_id: massiva.docente_id,  // ← AGGIUNTO
      data_inizio: massiva.data_inizio,
      data_fine: massiva.data_fine,
      ora_inizio: massiva.ora_inizio,
      ora_fine: massiva.ora_fine,
      tipo_ricorrenza: massiva.tipo_ricorrenza,
      giorni_settimana: massiva.giorni_settimana,
      note: massiva.note || undefined,
    })
    esitoMassiva.value = { tipo: 'ok', msg: '✓ Prenotazioni ricorrenti create con successo.' }
    if (risposta?.id) await verificaConflittiNuovaPrenotazione(risposta.id, 'massiva')
    massiva.giorni_settimana = []
  } catch (e) {
    esitoMassiva.value = { tipo: 'err', msg: e.message }
  } finally {
    loadingMassiva.value = false
  }
}

function resetSingola() {
  Object.assign(singola, { 
    sede_id: '', aula_id: '', corso_id: '', docente_id: '',  // ← AGGIUNTO docente_id
    data: '', ora_inizio: '09:00', ora_fine: '13:00', note: '' 
  })
  Object.keys(err).forEach(k => (err[k] = ''))
  aule.value = []
}

function resetMassiva() {
  Object.assign(massiva, {
    sede_id: '', aula_id: '', corso_id: '', docente_id: '',  // ← AGGIUNTO docente_id
    data_inizio: '', data_fine: '',
    ora_inizio: '09:00', ora_fine: '13:00',
    tipo_ricorrenza: 'settimanale',
    giorni_settimana: [],
    note: ''
  })
  Object.keys(errM).forEach(k => (errM[k] = ''))
  auleMassiva.value = []
  esitoMassiva.value = null
}

onMounted(async () => {
  const [dataSedi, dataAule] = await Promise.all([
    getSedi(),
    getAule(),
    caricaCorsi(),
    caricaDocenti()  // ← AGGIUNTO
  ])
  const tutteLeSedi = dataSedi || []
  const tutteLeAule = (dataAule?.items || dataAule || []).filter(a => a.attiva !== false)
  sedi.value = tutteLeSedi.filter(sede =>
    tutteLeAule.some(aula => aula.sede_id === sede.id)
  )
  if (route.query.sede_id) {
    singola.sede_id = Number(route.query.sede_id)
    await onSedeChange()
  } else {
    const sedeDefault = sedeDefaultFiltro.value
    if (sedeDefault) {
      const sedeHaAuleAttive = sedi.value.some(s => s.id === Number(sedeDefault))
      if (sedeHaAuleAttive) {
        singola.sede_id = sedeDefault
        massiva.sede_id = sedeDefault
        await onSedeChange()
        await onSedeChangeMassiva()
      }
    }
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
.modal-backdrop-celebration {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  animation: fadeIn 0.3s ease-out;
}
.modal-celebration {
  background: #fff;
  border-radius: 16px;
  padding: 40px;
  max-width: 500px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.4s ease-out;
}
.celebration-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  animation: bounce 0.6s ease-out;
}
.celebration-title {
  font-size: 2rem;
  font-weight: 700;
  color: #0066cc;
  margin-bottom: 12px;
}
.celebration-text {
  font-size: 1.125rem;
  color: #5c6f82;
  margin-bottom: 24px;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}
</style>