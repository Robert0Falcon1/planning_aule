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
            <div v-if="esito" class="alert" :class="esito.tipo === 'ok' ? 'alert-success' : 'alert-danger'">
              {{ esito.msg }}
            </div>
            <div v-if="alertConflitti" class="alert alert-warning">
              <svg class="icon icon-sm me-1">
                <use :href="sprites + '#it-error'"></use>
              </svg>
              {{ alertConflitti.msg }}
            </div>
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label fw-semibold">Sede *</label>
                <select v-model="form.sede_id" class="form-select" :class="{ 'is-invalid': err.sede_id }"
                  @change="onSedeChange">
                  <option value="">— seleziona —</option>
                  <option v-for="s in sediMostrate" :key="s.id" :value="s.id">{{ s.nome }}</option>
                </select>
                <div class="invalid-feedback">{{ err.sede_id }}</div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Aula *</label>
                <select v-model="form.aula_id" class="form-select" :class="{ 'is-invalid': err.aula_id }"
                  :disabled="!form.sede_id || caricandoAule">
                  <option value="">{{ caricandoAule ? 'Caricamento…' : '— seleziona sede prima —' }}</option>
                  <option v-for="a in aule" :key="a.id" :value="a.id">
                    {{ a.nome }} (cap. {{ a.capienza }}){{ a.attiva === false ? ' - INATTIVA' : '' }}
                  </option>
                </select>
                <div class="invalid-feedback">{{ err.aula_id }}</div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Corso *</label>
                <select v-model="form.corso_id" class="form-select" :class="{ 'is-invalid': err.corso_id }"
                  :disabled="caricandoCorsi || !form.sede_id">
                  <option value="">
                    {{ caricandoCorsi ? 'Caricamento…' : (!form.sede_id ? '— seleziona sede prima —' : '— seleziona —')
                    }}
                  </option>
                  <option v-for="c in corsiPerSelect" :key="c.id" :value="c.id">
                    {{ c.codice }} — {{ c.titolo }}
                  </option>
                </select>
                <div class="invalid-feedback">{{ err.corso_id }}</div>
              </div>
              <!-- Docente — filtrato per sede -->
              <div class="col-md-6">
                <label class="form-label fw-semibold">Docente *</label>
                <select v-model="form.docente_id" class="form-select" :class="{ 'is-invalid': err.docente_id }"
                  :disabled="caricandoDocenti || !form.sede_id">
                  <option value="">
                    {{ caricandoDocenti ? 'Caricamento…' : (!form.sede_id ? '— seleziona sede prima —' : '— seleziona —')
                    }}
                  </option>
                  <option v-for="d in docentiPerSelect" :key="d.id" :value="d.id">
                    {{ d.cognome }} {{ d.nome }}
                  </option>
                </select>
                <div class="invalid-feedback">{{ err.docente_id }}</div>
              </div>
              <div class="col-md-4">
                <label class="form-label fw-semibold">Data *</label>
                <input v-model="form.data" type="date" class="form-control" :class="{ 'is-invalid': err.data }" />
                <div class="invalid-feedback">{{ err.data }}</div>
              </div>
              <div class="col-md-4">
                <label class="form-label fw-semibold">Ora inizio *</label>
                <select v-model="form.ora_inizio" class="form-select" :class="{ 'is-invalid': err.ora_inizio }">
                  <option value="">—</option>
                  <option v-for="h in oreSlot" :key="h" :value="h">{{ h }}</option>
                </select>
                <div class="invalid-feedback">{{ err.ora_inizio }}</div>
              </div>
              <div class="col-md-4">
                <label class="form-label fw-semibold">Ora fine *</label>
                <select v-model="form.ora_fine" class="form-select" :class="{ 'is-invalid': err.ora_fine }">
                  <option value="">—</option>
                  <option v-for="h in oreSlot" :key="h" :value="h">{{ h }}</option>
                </select>
                <div class="invalid-feedback">{{ err.ora_fine }}</div>
              </div>
              <div class="col-12">
                <label class="form-label fw-semibold">Note</label>
                <textarea v-model="form.note" class="form-control" rows="2"
                  placeholder="es. Attrezzature necessarie, richieste particolari..."></textarea>
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
import { ref, reactive, watch, computed, onMounted } from 'vue'
import { getAuleBySede, getAule } from '@/api/aule'
import { getSedi } from '@/api/sedi'
import { modificaSlot } from '@/api/prenotazioni'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import { useConflittiAlert } from '@/composables/useConflittiAlert'
import { useCorsi } from '@/composables/useCorsi'
import { useCorsiPerSede } from '@/composables/useCorsiPerSede'
import { useDocenti } from '@/composables/useDocenti'  // ← AGGIUNTO

const props = defineProps({
  aperta: Boolean,
  slot: Object,
  sedi: Array,
  aulaMap: Object,
})
const emit = defineEmits(['update:aperta', 'salvato'])

const loading = ref(false)
const caricandoAule = ref(false)
const aule = ref([])
const tutteLeAule = ref([])
const tutteLeSedi = ref([])
const sediMostrate = ref([])
const esito = ref(null)
const { alertConflitti, verificaConflittiNuovaPrenotazione, resetAlert } = useConflittiAlert()

// ── Composable corsi ─────────────────────────────────────────────────────────
const { corsi, corsiAttivi, caricandoCorsi, caricaCorsi, getCorsoById } = useCorsi()

// ── Composable docenti ───────────────────────────────────────────────────────
const { docenti, docentiOrdinati, caricandoDocenti, caricaDocenti, getDocenteById } = useDocenti()

const form = reactive({
  sede_id: '', aula_id: '', corso_id: '', docente_id: '',  // ← AGGIUNTO docente_id
  data: '', ora_inizio: '', ora_fine: '', note: '',
})

// Filtraggio corsi per sede
const sedeRef = computed(() => form.sede_id)
const { corsiFiltrati } = useCorsiPerSede(corsiAttivi, sediMostrate, sedeRef)

// Computed: Corsi filtrati per sede + il corso corrente (anche se inattivo o fuori sede)
const corsiPerSelect = computed(() => {
  let lista = [...corsiFiltrati.value]
  // Recupero il corso attualmente selezionato nello slot (originale o da form)
  const corsoCorrente = getCorsoById(form.corso_id)
  // Se il corso corrente non è nella lista filtrata (perché inattivo o di un'altra sede), lo aggiungo
  if (corsoCorrente && !lista.some(c => c.id === corsoCorrente.id)) {
    lista.push(corsoCorrente)
  }
  return lista.sort((a, b) => (a.codice || '').localeCompare(b.codice || ''))
})

// Computed: Docenti filtrati per sede + il docente corrente
const docentiPerSelect = computed(() => {
  if (!form.sede_id) return []
  
  // Filtra docenti che operano nella sede selezionata
  let lista = docentiOrdinati.value.filter(d => 
    d.sedi?.some(s => s.id === Number(form.sede_id))
  )
  
  // Aggiungi il docente corrente se non è nella lista
  const docenteCorrente = getDocenteById(form.docente_id)
  if (docenteCorrente && !lista.some(d => d.id === docenteCorrente.id)) {
    lista.push(docenteCorrente)
  }
  
  return lista.sort((a, b) => 
    a.cognome.localeCompare(b.cognome) || a.nome.localeCompare(b.nome)
  )
})

const oreSlot = Array.from({ length: 29 }, (_, i) => {
  const totalMin = 7 * 60 + i * 30
  return `${String(Math.floor(totalMin / 60)).padStart(2, '0')}:${String(totalMin % 60).padStart(2, '0')}`
})

const err = reactive({
  sede_id: '', aula_id: '', corso_id: '', docente_id: '',  // ← AGGIUNTO
  data: '', ora_inizio: '', ora_fine: '',
})

// Reset corso/docente se cambio sede e quello attuale non è più compatibile
watch(corsiFiltrati, (nuovaLista) => {
  if (form.corso_id && !nuovaLista.some(c => c.id === form.corso_id)) {
    // In modifica, non resettiamo il corso se è il valore originale
  }
})

watch(() => props.aperta, async (val) => {
  if (!val || !props.slot) return
  esito.value = null
  resetAlert()
  Object.keys(err).forEach(k => err[k] = '')
  
  const s = props.slot
  const sedeId = props.aulaMap?.[s.aulaId]?.sede_id
  
  // 1. Calcola sedi da mostrare
  const auleAttive = tutteLeAule.value.filter(a => a.attiva !== false)
  const sediConAuleAttive = (props.sedi || []).filter(sede =>
    auleAttive.some(aula => aula.sede_id === sede.id)
  )
  const sedeCorrente = tutteLeSedi.value.find(sede => Number(sede.id) === Number(sedeId))
  if (sedeCorrente && !sediConAuleAttive.find(s => s.id === sedeCorrente.id)) {
    sediMostrate.value = [sedeCorrente, ...sediConAuleAttive]
  } else {
    sediMostrate.value = sediConAuleAttive
  }
  
  // 2. Popola form
  Object.assign(form, {
    sede_id: sedeId,
    aula_id: s.aulaId,
    corso_id: s.corsoId,
    docente_id: s.docenteId || '',  // ← AGGIUNTO
    data: s.data,
    ora_inizio: s.oraInizio.slice(0, 5),
    ora_fine: s.oraFine.slice(0, 5),
    note: s.note || '',
  })
  
  // 3. Carica aule della sede
  if (sedeId) {
    caricandoAule.value = true
    try {
      const data = await getAuleBySede(sedeId) || []
      // Mostriamo tutte le aule della sede, includendo quella corrente anche se inattiva
      aule.value = data.filter(a => a.attiva !== false || a.id === s.aulaId)
    } finally {
      caricandoAule.value = false
    }
  }
})

async function onSedeChange() {
  form.aula_id = ''
  // Non resettiamo forzatamente corso/docente per permettere il ricalcolo dei computed
  aule.value = []
  if (!form.sede_id) return
  caricandoAule.value = true
  try {
    const data = await getAuleBySede(form.sede_id)
    aule.value = (data || []).filter(a => a.attiva !== false)
  } finally {
    caricandoAule.value = false
  }
}

function chiudi() {
  emit('update:aperta', false)
}

function valida() {
  err.sede_id = form.sede_id ? '' : 'Obbligatorio'
  err.aula_id = form.aula_id ? '' : 'Obbligatorio'
  err.corso_id = form.corso_id ? '' : 'Obbligatorio'
  err.docente_id = form.docente_id ? '' : 'Obbligatorio'  // ← AGGIUNTO
  err.data = form.data ? '' : 'Obbligatorio'
  err.ora_inizio = form.ora_inizio ? '' : 'Obbligatorio'
  err.ora_fine = form.ora_fine ? '' : 'Obbligatorio'
  if (form.ora_inizio && form.ora_fine && form.ora_inizio >= form.ora_fine) {
    err.ora_fine = "Deve essere dopo l'ora di inizio"
  }
  return !Object.values(err).some(Boolean)
}

async function submit() {
  if (!valida()) return
  loading.value = true
  esito.value = null
  resetAlert()
  
  try {
    const pId = props.slot?.prenId
    const sId = props.slot?.slotId
    
    if (pId === undefined || sId === undefined) {
      throw new Error(`Dati identificativi mancanti! (prenId: ${pId}, slotId: ${sId})`)
    }
    
    await modificaSlot(pId, sId, {
      aula_id: form.aula_id,
      corso_id: form.corso_id,
      docente_id: form.docente_id,  // ← AGGIUNTO
      data: form.data,
      ora_inizio: form.ora_inizio,
      ora_fine: form.ora_fine,
      note: form.note,
    })
    
    esito.value = { tipo: 'ok', msg: 'Modifica salvata con successo.' }
    
    if (typeof verificaConflittiNuovaPrenotazione === 'function') {
      await verificaConflittiNuovaPrenotazione(pId, 'singola')
    }
    
    setTimeout(() => {
      emit('salvato')
      chiudi()
    }, 1000)
  } catch (e) {
    console.error("Errore durante il submit:", e)
    esito.value = { tipo: 'err', msg: e.message || 'Errore nel salvataggio' }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const [s, a] = await Promise.all([
    getSedi(), 
    getAule(), 
    caricaCorsi(),
    caricaDocenti()  // ← AGGIUNTO
  ])
  tutteLeSedi.value = s || []
  tutteLeAule.value = a?.items || a || []
})
</script>

<style scoped>
input[type=date] {
    padding: .25rem .5rem !important;
}
.form-select {
    border-bottom: 1px solid hsl(210,17%,44%) !important;
    border-radius: 0 !important;
}
</style>