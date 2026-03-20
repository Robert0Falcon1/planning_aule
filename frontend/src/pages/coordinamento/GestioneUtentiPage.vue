<template>
  <div class="page-utenti">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Gestione Utenti</h2>
      <div class="ms-auto d-flex gap-2 align-items-center">
        <!-- <input v-model="cerca" type="search" class="form-control form-control-sm" style="width:220px" placeholder="Cerca nome o username…" /> -->
        <select v-model="filtroRuolo" class="form-select form-select-sm" style="width:auto">
          <option value="">Tutti i ruoli</option>
          <option value="OPERATIVO">OPERATIVO</option>
          <option value="COORDINAMENTO">COORDINAMENTO</option>
        </select>
        <select v-model="filtroAttivo" class="form-select form-select-sm" style="width:auto">
          <option value="">Tutti</option>
          <option value="true">Attivi</option>
          <option value="false">Disattivati</option>
        </select>
        <button class="btn btn-sm btn-primary" @click="apriModale()">
          <svg class="icon icon-white icon-sm me-1"><use :href="sprites + '#it-plus-circle'"></use></svg>
          Nuovo
        </button>
      </div>
    </div>

    <div class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
        <div v-else-if="!utentiFiltrati.length" class="text-center text-muted py-5">Nessun utente trovato.</div>
        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light sticky-top">
              <tr>
                <th>Utente</th><th>Ruolo</th><th>Sede</th>
                <th>Stato</th><th>Creato&nbsp;il</th><th class="text-end">Azioni</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in utentiFiltrati" :key="u.id" :class="{ 'row-disattivato': !u.attivo }">
                <td>
                  <div class="d-flex align-items-center gap-2">
                    <div class="avatar-circle" :class="u.ruolo === 'COORDINAMENTO' ? 'avatar-coord' : 'avatar-op'">
                      {{ iniziali(u) }}
                    </div>
                    <div>
                      <div class="fw-semibold">{{ u.nome }} {{ u.cognome }}</div>
                      <small class="text-muted">{{ u.email || '' }}</small>
                    </div>
                  </div>
                </td>
                <!-- <td><code class="small">{{ u.username }}</code></td> -->
                <td>
                  <span class="badge" :class="u.ruolo === 'COORDINAMENTO' ? 'bg-warning text-dark' : 'badge-ruolo'">
                    {{ u.ruolo }}
                  </span>
                </td>
                <td>{{ nomeSede(u.sede_id) }}</td>
                <td>
                  <span class="badge" :class="u.attivo ? 'bg-success' : 'bg-secondary'">
                    {{ u.attivo ? 'Attivo' : 'Disattivato' }}
                  </span>
                </td>
                <td><small class="text-muted">{{ formatData(u.data_creazione) }}</small></td>
                <td class="text-end">
                  <div class="d-flex gap-1 justify-content-end">
                    <button class="btn btn-sm btn-outline-success" @click="apriModale(u)">
                      <svg class="icon icon-sm"><use :href="sprites + '#it-pencil'"></use></svg>
                    </button>
                    <button
                      class="btn btn-sm"
                      :class="u.attivo ? 'btn-outline-danger' : 'btn-outline-success'"
                      @click="toggleAttivo(u)"
                      :disabled="toggling === u.id"
                    >
                      <span v-if="toggling === u.id" class="spinner-border spinner-border-sm"></span>
                      <svg v-else class="icon icon-sm">
                        <use :href="`${sprites}#${u.attivo ? 'it-close-circle' : 'it-check-circle'}`"></use>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal crea/modifica utente -->
    <div v-if="modale" class="modal-backdrop-custom" @click.self="chiudiModale">
      <div class="modal-dialog-custom card border-0 shadow-lg p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="fw-bold mb-0">{{ utenteInEdit ? 'Modifica utente' : 'Nuovo utente' }}</h5>
          <button class="btn-close" @click="chiudiModale"></button>
        </div>
        <form @submit.prevent="salva" novalidate>
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label fw-semibold">Nome *</label>
              <input v-model="form.nome" type="text" class="form-control" :class="{ 'is-invalid': fe.nome }" />
              <div class="invalid-feedback">{{ fe.nome }}</div>
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Cognome *</label>
              <input v-model="form.cognome" type="text" class="form-control" :class="{ 'is-invalid': fe.cognome }" />
              <div class="invalid-feedback">{{ fe.cognome }}</div>
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Email</label>
              <input v-model="form.email" type="email" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Ruolo *</label>
              <select v-model="form.ruolo" class="form-select" :class="{ 'is-invalid': fe.ruolo }">
                <option value="">— seleziona —</option>
                <option value="OPERATIVO">OPERATIVO</option>
                <option value="COORDINAMENTO">COORDINAMENTO</option>
              </select>
              <div class="invalid-feedback">{{ fe.ruolo }}</div>
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Sede di riferimento</label>
              <select v-model="form.sede_id" class="form-select">
                <option value="">— nessuna —</option>
                <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
              </select>
            </div>
            <div v-if="!utenteInEdit" class="col-md-6">
              <label class="form-label fw-semibold">Password *</label>
              <input v-model="form.password" type="password" class="form-control" :class="{ 'is-invalid': fe.password }" autocomplete="new-password" />
              <div class="invalid-feedback">{{ fe.password }}</div>
            </div>
          </div>
          <div v-if="errModale" class="alert alert-danger mt-3 py-2 small">{{ errModale }}</div>
          <div class="d-flex gap-2 justify-content-end mt-4">
            <button type="button" class="btn btn-secondary" @click="chiudiModale">Annulla</button>
            <button type="submit" class="btn btn-primary" :disabled="salvando">
              <span v-if="salvando" class="spinner-border spinner-border-sm me-1"></span>
              {{ utenteInEdit ? 'Salva modifiche' : 'Crea utente' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getUtenti, creaUtente, modificaUtente, disattivaUtente, attivaUtente } from '@/api/utenti'
import { getSedi } from '@/api/sedi'
import { formatData } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading      = ref(false)
const salvando     = ref(false)
const toggling     = ref(null)
const utenti       = ref([])
const sedi         = ref([])
const cerca        = ref('')
const filtroRuolo  = ref('')
const filtroAttivo = ref('')
const modale       = ref(false)
const utenteInEdit = ref(null)
const errModale    = ref('')

const form = reactive({ nome: '', cognome: '', email: '', ruolo: '', sede_id: '', password: '' })
const fe   = reactive({ nome: '', cognome: '', ruolo: '', password: '' })

function nomeSede(sedeId) {
  if (!sedeId) return '—'
  return sedi.value.find(s => s.id === sedeId)?.nome || `Sede ${sedeId}`
}

const utentiFiltrati = computed(() => {
  return utenti.value
    .filter(u => {
      const q = cerca.value.toLowerCase()
      if (q && !u.nome_completo?.toLowerCase().includes(q) && !u.username?.toLowerCase().includes(q)) return false
      if (filtroRuolo.value && u.ruolo !== filtroRuolo.value) return false
      if (filtroAttivo.value !== '') {
        if (u.attivo !== (filtroAttivo.value === 'true')) return false
      }
      return true
    })
    .sort((a, b) => {
      // Ordine alfabetico: prima per cognome, poi per nome
      const cognomeA = (a.cognome || '').toLowerCase()
      const cognomeB = (b.cognome || '').toLowerCase()
      if (cognomeA !== cognomeB) return cognomeA.localeCompare(cognomeB)
      return (a.nome || '').toLowerCase().localeCompare((b.nome || '').toLowerCase())
    })
})

function iniziali(u) {
  const parts = [u.nome || '', u.cognome || ''].filter(Boolean)
  return parts.slice(0, 2).map(p => p[0]?.toUpperCase() || '').join('')
}

function apriModale(u = null) {
  utenteInEdit.value = u
  errModale.value    = ''
  Object.assign(form, {
    nome:    u?.nome    || '',
    cognome: u?.cognome || '',
    email:   u?.email   || '',
    ruolo:   u?.ruolo   || '',
    sede_id: u?.sede_id || '',
    password: '',
  })
  Object.keys(fe).forEach(k => (fe[k] = ''))
  modale.value = true
}

function chiudiModale() {
  modale.value = false; utenteInEdit.value = null
}

function valida() {
  fe.nome    = form.nome.trim()    ? '' : 'Obbligatorio'
  fe.cognome = form.cognome.trim() ? '' : 'Obbligatorio'
  fe.ruolo   = form.ruolo          ? '' : 'Obbligatorio'
  fe.password = (utenteInEdit.value || form.password) ? '' : 'Obbligatoria per nuovo utente'
  return !Object.values(fe).some(Boolean)
}

async function salva() {
  if (!valida()) return
  salvando.value = true; errModale.value = ''
  try {
    const payload = {
      nome:    form.nome,
      cognome: form.cognome,
      email:   form.email || undefined,
      ruolo:   form.ruolo,
      sede_id: form.sede_id || undefined,
    }
    if (utenteInEdit.value) {
      const updated = await modificaUtente(utenteInEdit.value.id, payload)
      const idx = utenti.value.findIndex(u => u.id === utenteInEdit.value.id)
      if (idx !== -1) utenti.value[idx] = { ...utenti.value[idx], ...updated }
    } else {
      const created = await creaUtente({ ...payload, password: form.password })
      utenti.value.unshift(created)
    }
    chiudiModale()
  } catch (e) {
    errModale.value = e.message || 'Errore durante il salvataggio'
  } finally {
    salvando.value = false
  }
}

async function toggleAttivo(u) {
  toggling.value = u.id
  try {
    u.attivo ? await disattivaUtente(u.id) : await attivaUtente(u.id)
    const idx = utenti.value.findIndex(x => x.id === u.id)
    if (idx !== -1) utenti.value[idx].attivo = !u.attivo
  } catch (e) {
    alert(`Errore: ${e.message}`)
  } finally {
    toggling.value = null
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const [du, ds] = await Promise.all([getUtenti(), getSedi()])
    utenti.value = du?.items || du || []
    sedi.value   = ds?.items || ds || []
  } catch (e) {
    console.warn('GestioneUtenti:', e.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title { font-size: 1.4rem; font-weight: 700; }
.row-disattivato td { opacity: .5; }
.avatar-circle {
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: .75rem; font-weight: 700; color: white; flex-shrink: 0;
}
.avatar-op    { background: #0066cc; }
.avatar-coord { background: #cc8800; }
.modal-backdrop-custom {
  position: fixed; inset: 0; background: rgba(0,0,0,.45);
  display: flex; align-items: center; justify-content: center; z-index: 2000;
}
.modal-dialog-custom { width: 100%; max-width: 560px; border-radius: 12px; max-height: 90vh; overflow-y: auto; }
</style>