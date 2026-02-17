<template>
  <div>
    <h2 class="h4 fw-bold mb-4">👥 Gestione Utenti</h2>

    <div class="row g-4">
      <!-- Form creazione -->
      <div class="col-lg-4">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white fw-semibold">➕ Nuovo Utente</div>
          <div class="card-body">
            <form @submit.prevent="handleCrea" novalidate>
              <div class="mb-3">
                <label class="form-label small fw-semibold">Nome *</label>
                <input v-model="form.nome" type="text" class="form-control form-control-sm" />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-semibold">Cognome *</label>
                <input v-model="form.cognome" type="text" class="form-control form-control-sm" />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-semibold">Email *</label>
                <input v-model="form.email" type="email" class="form-control form-control-sm" />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-semibold">Password *</label>
                <input v-model="form.password" type="password" class="form-control form-control-sm" />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-semibold">Ruolo *</label>
                <select v-model="form.ruolo" class="form-select form-select-sm">
                  <option value="">— Seleziona —</option>
                  <option v-for="(label, val) in RUOLI_LABEL" :key="val" :value="val">
                    {{ label }}
                  </option>
                </select>
              </div>
              <div class="mb-4">
                <label class="form-label small fw-semibold">Sede</label>
                <select v-model="form.sede_id" class="form-select form-select-sm">
                  <option :value="null">— Nessuna (es. Coordinamento) —</option>
                  <option v-for="s in sedi" :key="s.id" :value="s.id">
                    {{ s.nome }}
                  </option>
                </select>
              </div>

              <div v-if="erroreForm" class="alert alert-danger py-2 small mb-3">
                {{ erroreForm }}
              </div>

              <button type="submit" class="btn btn-primary btn-sm w-100" :disabled="loadingForm">
                {{ loadingForm ? 'Creazione…' : '➕ Crea Utente' }}
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Lista utenti -->
      <div class="col-lg-8">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white d-flex justify-content-between align-items-center">
            <span class="fw-semibold">Utenti registrati</span>
            <span class="badge bg-secondary">{{ utenti.length }}</span>
          </div>
          <div class="card-body p-0">
            <LoadingSpinner v-if="loading" />
            <table v-else class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>Nome</th>
                  <th>Email</th>
                  <th>Ruolo</th>
                  <th class="text-center">Stato</th>
                  <th class="text-center">Azioni</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="u in utenti"
                  :key="u.id"
                  :class="{ 'text-muted opacity-50': !u.attivo }"
                >
                  <td>
                    <span class="fw-semibold">{{ u.nome }} {{ u.cognome }}</span>
                    <span v-if="u.id === me?.id" class="badge bg-primary ms-1 small">Tu</span>
                  </td>
                  <td class="small">{{ u.email }}</td>
                  <td>
                    <span class="badge bg-info text-dark small">
                      {{ RUOLI_LABEL[u.ruolo] ?? u.ruolo }}
                    </span>
                  </td>
                  <td class="text-center">
                    <span v-if="u.attivo" class="badge bg-success">✅ Attivo</span>
                    <span v-else class="badge bg-secondary">⛔ Disattivato</span>
                  </td>
                  <td class="text-center">
                    <!-- Non si può disattivare se stessi -->
                    <template v-if="u.id !== me?.id">
                      <button
                        v-if="u.attivo"
                        class="btn btn-sm btn-outline-danger"
                        :disabled="loadingAzione === u.id"
                        @click="disattiva(u)"
                        title="Disattiva utente"
                      >
                        {{ loadingAzione === u.id ? '…' : '⛔' }}
                      </button>
                      <button
                        v-else
                        class="btn btn-sm btn-outline-success"
                        :disabled="loadingAzione === u.id"
                        @click="riattiva(u)"
                        title="Riattiva utente"
                      >
                        {{ loadingAzione === u.id ? '…' : '✅' }}
                      </button>
                    </template>
                    <span v-else class="text-muted small">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal conferma disattivazione -->
    <div v-if="utenteSelezionato" class="modal-backdrop" style="background:rgba(0,0,0,.5);position:fixed;inset:0;z-index:1040;" />
    <div v-if="utenteSelezionato" class="modal d-block" style="z-index:1050;" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">⛔ Conferma disattivazione</h5>
            <button class="btn-close" @click="utenteSelezionato = null" />
          </div>
          <div class="modal-body">
            <p>Stai per disattivare l'account di <strong>{{ utenteSelezionato.nome }} {{ utenteSelezionato.cognome }}</strong> (<em>{{ utenteSelezionato.email }}</em>).</p>
            <p class="text-muted small mb-0">
              L'utente non potrà più accedere al sistema. Le prenotazioni esistenti rimarranno invariate.
              Potrai riattivarlo in qualsiasi momento.
            </p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" @click="utenteSelezionato = null">Annulla</button>
            <button class="btn btn-danger" @click="confermaDisattiva">⛔ Disattiva</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore }  from '@/stores/auth'
import { useUiStore }    from '@/stores/ui'
import { getUtenti, creaUtente, disattivaUtente, riattivaUtente } from '@/api/utenti'
import { getSedi }       from '@/api/sedi'
import { estraiErrore }  from '@/utils/errori'
import { RUOLI_LABEL }   from '@/utils/constants'
import LoadingSpinner    from '@/components/ui/LoadingSpinner.vue'

const authStore = useAuthStore()
const uiStore   = useUiStore()

const me              = authStore.user
const utenti          = ref([])
const sedi            = ref([])
const loading         = ref(false)
const loadingForm     = ref(false)
const loadingAzione   = ref(null)
const erroreForm      = ref('')
const utenteSelezionato = ref(null)

const form = reactive({
  nome: '', cognome: '', email: '', password: '',
  ruolo: '', sede_id: null,
})

async function caricaUtenti() {
  loading.value = true
  try { utenti.value = await getUtenti() }
  finally { loading.value = false }
}

async function handleCrea() {
  erroreForm.value = ''
  if (!form.nome || !form.cognome || !form.email || !form.password || !form.ruolo) {
    erroreForm.value = 'Compila tutti i campi obbligatori.'
    return
  }
  loadingForm.value = true
  try {
    await creaUtente({ ...form })
    uiStore.successo(`Utente ${form.email} creato con successo.`)
    Object.assign(form, { nome:'', cognome:'', email:'', password:'', ruolo:'', sede_id: null })
    await caricaUtenti()
  } catch (err) {
    erroreForm.value = estraiErrore(err)
  } finally {
    loadingForm.value = false
  }
}

// Apre modal di conferma
function disattiva(u) {
  utenteSelezionato.value = u
}

async function confermaDisattiva() {
  const u = utenteSelezionato.value
  utenteSelezionato.value = null
  loadingAzione.value = u.id
  try {
    await disattivaUtente(u.id)
    uiStore.successo(`${u.nome} ${u.cognome} disattivato.`)
    await caricaUtenti()
  } catch (err) {
    uiStore.errore(estraiErrore(err))
  } finally {
    loadingAzione.value = null
  }
}

async function riattiva(u) {
  loadingAzione.value = u.id
  try {
    await riattivaUtente(u.id)
    uiStore.successo(`${u.nome} ${u.cognome} riattivato.`)
    await caricaUtenti()
  } catch (err) {
    uiStore.errore(estraiErrore(err))
  } finally {
    loadingAzione.value = null
  }
}

onMounted(async () => {
  await caricaUtenti()
  sedi.value = await getSedi()
})
</script>
