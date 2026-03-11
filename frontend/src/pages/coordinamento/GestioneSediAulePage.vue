<template>
  <div class="page-gestione-sedi">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Gestione Sedi &amp; Aule</h2>
      <div class="ms-auto d-flex gap-2">
        <button class="btn btn-sm btn-outline-primary" @click="apriModaleSede()">
          <svg class="icon icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
          Nuova sede
        </button>
        <button class="btn btn-sm btn-primary" @click="apriModaleAula()">
          <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
          Nuova aula
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else>
      <div v-for="sede in sedi" :key="sede.id" class="mb-4">
        <div class="sede-row d-flex align-items-center gap-3 mb-3 p-3 rounded-3">
          <svg class="icon icon-white flex-shrink-0"><use :href="sprites + '#it-map-marker'"></use></svg>
          <div class="flex-grow-1">
            <h5 class="mb-0 text-white fw-bold">{{ sede.nome }}</h5>
            <small class="text-white-50">{{ sede.indirizzo || 'Indirizzo non specificato' }}</small>
          </div>
          <span class="badge bg-white text-primary">{{ auleDiSede(sede.id).length }} aule</span>
          <button class="btn btn-sm btn-light" @click="apriModaleSede(sede)">
            <svg class="icon icon-sm"><use :href="sprites + '#it-pencil'"></use></svg>
          </button>
        </div>

        <div class="card border-0 shadow-sm">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 table-sm">
              <thead class="table-light">
                <tr>
                  <th><span class="ms-2">Nome aula</span></th><th>Capienza</th><th>Note</th><th>Stato</th><th class="text-end"><span class="me-2">Azioni</span></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="aula in auleDiSede(sede.id)" :key="aula.id">
                  <td class="fw-semibold"><span class="ms-2">{{ aula.nome }}</span></td>
                  <td><span class="badge bg-info-subtle text-info">{{ aula.capienza }} posti</span></td>
                  <td><small class="text-muted">{{ aula.note || '—' }}</small></td>
                  <td>
                    <span class="badge" :class="aula.attiva !== false ? 'bg-success' : 'bg-secondary'">
                      {{ aula.attiva !== false ? 'Attiva' : 'Inattiva' }}
                    </span>
                  </td>
                  <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary" @click="apriModaleAula(aula, sede)">
                      <svg class="icon icon-sm"><use :href="sprites + '#it-pencil'"></use></svg>
                    </button>
                  </td>
                </tr>
                <tr v-if="!auleDiSede(sede.id).length">
                  <td colspan="5" class="text-muted text-center py-3">Nessuna aula registrata.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="card-footer bg-white text-end pt-3 pb-2 pe-0">
            <button class="btn btn-sm btn-outline-primary" @click="apriModaleAula(null, sede)">
              <svg class="icon icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
              Aggiungi aula a {{ sede.nome }}
            </button>
          </div>
        </div>
      </div>
      <div v-if="!sedi.length" class="text-center text-muted py-5">Nessuna sede trovata.</div>
    </div>

    <!-- Modal SEDE -->
    <div v-if="modaleSede" class="modal-backdrop-custom" @click.self="modaleSede = false">
      <div class="modal-dialog-custom card border-0 shadow-lg p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="fw-bold mb-0">{{ sedeInEdit ? 'Modifica sede' : 'Nuova sede' }}</h5>
          <button class="btn-close" @click="modaleSede = false"></button>
        </div>
        <form @submit.prevent="salvaSede" novalidate>
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label fw-semibold">Nome sede *</label>
              <input v-model="formSede.nome" type="text" class="form-control"
                :class="{ 'is-invalid': fse.nome }" />
              <div class="invalid-feedback">{{ fse.nome }}</div>
            </div>
            <div class="col-md-8">
              <label class="form-label fw-semibold">Indirizzo</label>
              <input v-model="formSede.indirizzo" type="text" class="form-control"
                placeholder="Via e numero civico" />
            </div>
            <!-- FIX: aggiunto campo città (richiesto dal backend) -->
            <div class="col-md-4">
              <label class="form-label fw-semibold">Città *</label>
              <input v-model="formSede.citta" type="text" class="form-control"
                :class="{ 'is-invalid': fse.citta }" placeholder="es. Torino" />
              <div class="invalid-feedback">{{ fse.citta }}</div>
            </div>
            <!-- FIX: aggiunto campo capienza massima (richiesto dal backend) -->
            <div class="col-md-4">
              <label class="form-label fw-semibold">Capienza massima</label>
              <input v-model.number="formSede.capienza_massima" type="number" min="0"
                class="form-control" placeholder="0" />
            </div>
          </div>
          <div v-if="errSede" class="alert alert-danger mt-3 py-2 small">{{ errSede }}</div>
          <div class="d-flex gap-2 justify-content-end mt-4">
            <button type="button" class="btn btn-secondary" @click="modaleSede = false">Annulla</button>
            <button type="submit" class="btn btn-primary" :disabled="salvandoSede">
              <span v-if="salvandoSede" class="spinner-border spinner-border-sm me-1"></span>
              {{ sedeInEdit ? 'Salva' : 'Crea sede' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal AULA -->
    <div v-if="modaleAula" class="modal-backdrop-custom" @click.self="modaleAula = false">
      <div class="modal-dialog-custom card border-0 shadow-lg p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="fw-bold mb-0">{{ aulaInEdit ? 'Modifica aula' : 'Nuova aula' }}</h5>
          <button class="btn-close" @click="modaleAula = false"></button>
        </div>
        <form @submit.prevent="salvaAula" novalidate>
          <div class="row g-3">
            <div class="col-md-8">
              <label class="form-label fw-semibold">Nome aula *</label>
              <input v-model="formAula.nome" type="text" class="form-control"
                :class="{ 'is-invalid': fau.nome }" />
              <div class="invalid-feedback">{{ fau.nome }}</div>
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold">Capienza *</label>
              <input v-model.number="formAula.capienza" type="number" min="1" max="500"
                class="form-control" :class="{ 'is-invalid': fau.capienza }" />
              <div class="invalid-feedback">{{ fau.capienza }}</div>
            </div>
            <div class="col-12">
              <label class="form-label fw-semibold">Sede *</label>
              <select v-model="formAula.sede_id" class="form-select"
                :class="{ 'is-invalid': fau.sede_id }">
                <option value="">— seleziona —</option>
                <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
              </select>
              <div class="invalid-feedback">{{ fau.sede_id }}</div>
            </div>
            <div class="col-12">
              <label class="form-label fw-semibold">Note</label>
              <textarea v-model="formAula.note" class="form-control" rows="2"
                placeholder="Dotazioni, accessibilità, ecc."></textarea>
            </div>
            <div v-if="aulaInEdit" class="col-12">
              <div class="form-check form-switch">
                <input v-model="formAula.attiva" class="form-check-input" type="checkbox"
                  role="switch" id="switchAttiva" />
                <label class="form-check-label" for="switchAttiva">Aula attiva</label>
              </div>
            </div>
          </div>
          <div v-if="errAula" class="alert alert-danger mt-3 py-2 small">{{ errAula }}</div>
          <div class="d-flex gap-2 justify-content-end mt-4">
            <button type="button" class="btn btn-secondary" @click="modaleAula = false">Annulla</button>
            <button type="submit" class="btn btn-primary" :disabled="salvandoAula">
              <span v-if="salvandoAula" class="spinner-border spinner-border-sm me-1"></span>
              {{ aulaInEdit ? 'Salva modifiche' : 'Crea aula' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getSedi, creaSede, modificaSede } from '@/api/sedi'
import { getAule, creaAula, modificaAula } from '@/api/aule'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading = ref(false)
const sedi    = ref([])
const aule    = ref([])

const modaleSede   = ref(false)
const sedeInEdit   = ref(null)
const salvandoSede = ref(false)
const errSede      = ref('')
// FIX: aggiunti citta e capienza_massima (mancanti → 422 dal backend)
const formSede = reactive({ nome: '', indirizzo: '', citta: '', capienza_massima: 0 })
const fse      = reactive({ nome: '', citta: '' })

function auleDiSede(sedeId) {
  return aule.value.filter(a => a.sede_id === sedeId || a.sede?.id === sedeId)
}

function apriModaleSede(s = null) {
  sedeInEdit.value = s
  errSede.value    = ''
  Object.assign(formSede, {
    nome:             s?.nome             || '',
    indirizzo:        s?.indirizzo        || '',
    citta:            s?.citta            || '',
    capienza_massima: s?.capienza_massima || 0,
  })
  fse.nome = ''; fse.citta = ''
  modaleSede.value = true
}

async function salvaSede() {
  fse.nome  = formSede.nome.trim()  ? '' : 'Obbligatorio'
  fse.citta = formSede.citta.trim() ? '' : 'Obbligatorio'
  if (fse.nome || fse.citta) return
  salvandoSede.value = true; errSede.value = ''
  try {
    const payload = {
      nome:             formSede.nome,
      indirizzo:        formSede.indirizzo || undefined,
      citta:            formSede.citta,
      capienza_massima: formSede.capienza_massima || 0,
    }
    if (sedeInEdit.value) {
      const updated = await modificaSede(sedeInEdit.value.id, payload)
      const idx = sedi.value.findIndex(s => s.id === sedeInEdit.value.id)
      if (idx !== -1) sedi.value[idx] = { ...sedi.value[idx], ...updated }
    } else {
      const created = await creaSede(payload)
      sedi.value.push(created)
    }
    modaleSede.value = false
  } catch (e) {
    errSede.value = e.message || 'Errore'
  } finally {
    salvandoSede.value = false
  }
}

const modaleAula   = ref(false)
const aulaInEdit   = ref(null)
const salvandoAula = ref(false)
const errAula      = ref('')
const formAula     = reactive({ nome: '', capienza: 20, sede_id: '', note: '', attiva: true })
const fau          = reactive({ nome: '', capienza: '', sede_id: '' })

function apriModaleAula(a = null, sede = null) {
  aulaInEdit.value = a
  errAula.value    = ''
  Object.assign(formAula, {
    nome:     a?.nome     || '',
    capienza: a?.capienza || 20,
    sede_id:  a?.sede_id  || a?.sede?.id || sede?.id || '',
    note:     a?.note     || '',
    attiva:   a?.attiva !== false,
  })
  Object.keys(fau).forEach(k => (fau[k] = ''))
  modaleAula.value = true
}

async function salvaAula() {
  fau.nome     = formAula.nome.trim()  ? '' : 'Obbligatorio'
  fau.capienza = formAula.capienza > 0 ? '' : 'Deve essere > 0'
  fau.sede_id  = formAula.sede_id      ? '' : 'Obbligatorio'
  if (Object.values(fau).some(Boolean)) return
  salvandoAula.value = true; errAula.value = ''
  try {
    const payload = {
      nome:     formAula.nome,
      capienza: formAula.capienza,
      sede_id:  formAula.sede_id,
      note:     formAula.note || undefined,
      attiva:   formAula.attiva,
    }
    if (aulaInEdit.value) {
      const updated = await modificaAula(aulaInEdit.value.id, payload)
      const idx = aule.value.findIndex(a => a.id === aulaInEdit.value.id)
      if (idx !== -1) aule.value[idx] = { ...aule.value[idx], ...payload, ...(updated || {}) }
    } else {
      const created = await creaAula(payload)
      aule.value.push(created)
    }
    modaleAula.value = false
  } catch (e) {
    errAula.value = e.message || 'Errore'
  } finally {
    salvandoAula.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const [ds, da] = await Promise.all([getSedi(), getAule()])
    sedi.value = ds?.items || ds || []
    aule.value = da?.items || da || []
  } catch (e) {
    console.warn('GestioneSedi:', e.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
.sede-row { background: var(--bs-primary, #0066cc); }
.modal-backdrop-custom {
  position: fixed; inset: 0; background: rgba(0,0,0,.45);
  display: flex; align-items: center; justify-content: center; z-index: 2000;
}
.modal-dialog-custom {
  width: 100%; max-width: 520px; border-radius: 12px; max-height: 90vh; overflow-y: auto;
}
</style>