<template>
  <div>
    <h2 class="h4 fw-bold mb-4">👥 Gestione Utenti</h2>

    <div class="row g-4">
      <!-- Form creazione utente -->
      <div class="col-lg-5">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white fw-semibold">➕ Crea Nuovo Utente</div>
          <div class="card-body p-4">
            <form @submit.prevent="creaUtente" novalidate>
              <div class="mb-3">
                <label class="form-label fw-semibold">Nome *</label>
                <input v-model="form.nome" type="text" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Cognome *</label>
                <input v-model="form.cognome" type="text" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Email *</label>
                <input v-model="form.email" type="email" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Password iniziale *</label>
                <input v-model="form.password" type="password" class="form-control" />
                <div class="form-text">Comunicare la password all'utente perché la cambi.</div>
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Ruolo *</label>
                <select v-model="form.ruolo" class="form-select">
                  <option value="">— Seleziona ruolo —</option>
                  <option v-for="(label, val) in RUOLI_LABEL" :key="val" :value="val">
                    {{ label }}
                  </option>
                </select>
              </div>
              <div class="mb-4">
                <label class="form-label fw-semibold">Sede</label>
                <select v-model.number="form.sede_id" class="form-select">
                  <option :value="null">Nessuna (es. Coordinamento)</option>
                  <option v-for="s in sedi" :key="s.id" :value="s.id">
                    {{ s.nome }} ({{ s.citta }})
                  </option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="loadingCrea">
                {{ loadingCrea ? 'Creazione…' : '➕ Crea Utente' }}
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Lista utenti -->
      <div class="col-lg-7">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white fw-semibold">Lista Utenti</div>
          <LoadingSpinner v-if="loading" />
          <div v-else class="table-responsive">
            <table class="table table-hover table-sm mb-0">
              <thead class="table-light">
                <tr>
                  <th>Nome</th><th>Email</th><th>Ruolo</th><th>Sede</th><th>Attivo</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="u in utenti" :key="u.id">
                  <td class="fw-semibold">{{ u.nome }} {{ u.cognome }}</td>
                  <td class="small text-muted">{{ u.email }}</td>
                  <td><span class="badge bg-primary bg-opacity-10 text-primary">{{ labelRuolo(u.ruolo) }}</span></td>
                  <td class="small">{{ u.sede_id ?? '—' }}</td>
                  <td>
                    <span :class="u.attivo ? 'text-success' : 'text-danger'">
                      {{ u.attivo ? '✅' : '❌' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUiStore }               from '@/stores/ui'
import { getUtenti, creaUtente as apiCreaUtente } from '@/api/utenti'
import { getSedi }                  from '@/api/sedi'
import { labelRuolo }               from '@/utils/formatters'
import { RUOLI_LABEL }              from '@/utils/constants'
import LoadingSpinner               from '@/components/ui/LoadingSpinner.vue'

const uiStore   = useUiStore()
const loading   = ref(false)
const loadingCrea = ref(false)
const utenti    = ref([])
const sedi      = ref([])

const form = reactive({
  nome: '', cognome: '', email: '', password: '',
  ruolo: '', sede_id: null,
})

onMounted(async () => {
  loading.value = true
  try {
    [utenti.value, sedi.value] = await Promise.all([getUtenti(), getSedi()])
  } finally {
    loading.value = false
  }
})

async function creaUtente() {
  if (!form.nome || !form.cognome || !form.email || !form.password || !form.ruolo) {
    uiStore.avviso('Compila tutti i campi obbligatori.')
    return
  }
  loadingCrea.value = true
  try {
    await apiCreaUtente({ ...form })
    uiStore.successo(`Utente ${form.email} creato con successo.`)
    Object.assign(form, { nome: '', cognome: '', email: '', password: '', ruolo: '', sede_id: null })
    utenti.value = await getUtenti()
  } catch (err) {
    uiStore.errore(err.response?.data?.detail ?? 'Errore durante la creazione.')
  } finally {
    loadingCrea.value = false
  }
}
</script>
