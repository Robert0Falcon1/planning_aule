<template>
  <div>
    <h2 class="h4 fw-bold mb-4">⚠️ Gestione Conflitti</h2>
    <p class="text-muted mb-4">
      Queste prenotazioni sono state inviate ma presentano sovrapposizioni.
      Valuta se approvarle (se il conflitto è gestibile) o rifiutarle con motivazione.
    </p>
    <LoadingSpinner v-if="loading" />
    <div v-else-if="conflitti.length === 0" class="alert alert-success">
      ✅ Nessun conflitto aperto. Tutto in ordine!
    </div>
    <div v-else class="d-flex flex-column gap-3">
      <div
        v-for="p in conflitti"
        :key="p.id"
        class="card border-start border-4 border-warning shadow-sm"
      >
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-8">
              <div class="fw-semibold mb-1">⚠️ Prenotazione #{{ p.id }}</div>
              <div class="text-muted small">
                Aula {{ p.slots?.[0]?.aula_id }} | {{ getTitoloCorso(p.slots?.[0]?.corso_id) }} | {{ p.tipo }} |
                {{ p.slots?.length ?? 0 }} Prenotazioni
              </div>
              <div v-if="p.slots?.[0]" class="small mt-1">
                📅 {{ formatData(p.slots[0].data) }}
                {{ formatOra(p.slots[0].ora_inizio) }}–{{ formatOra(p.slots[0].ora_fine) }}
              </div>
              <div v-if="p.slots?.[0]?.note" class="small text-muted fst-italic mt-1">Note: {{ p.slots?.[0]?.note }}</div>
            </div>
            <div class="col-md-4">
              <div class="d-grid gap-2">
                <button
                  class="btn btn-success btn-sm"
                  :disabled="azione[p.id]?.loading"
                  @click="approva(p)"
                >
                  ✅ Approva comunque
                </button>
                <button
                  class="btn btn-outline-danger btn-sm"
                  @click="toggleRifiuto(p.id)"
                >
                  ❌ Rifiuta
                </button>
              </div>
              <div v-if="azione[p.id]?.showRifiuto" class="mt-2">
                <textarea
                  v-model="azione[p.id].motivo"
                  class="form-control form-control-sm mb-1"
                  rows="2"
                  placeholder="Motivo del rifiuto"
                />
                <button
                  class="btn btn-danger btn-sm w-100"
                  :disabled="!azione[p.id].motivo"
                  @click="rifiuta(p)"
                >
                  Conferma rifiuto
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import { getPrenotazioni, approvaRichiesta, rifiutaRichiesta } from '@/api/prenotazioni'
import { formatData, formatOra } from '@/utils/formatters'
import { useCorsi } from '@/composables/useCorsi'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const uiStore = useUiStore()
const loading = ref(false)
const conflitti = ref([])
const azione = reactive({})

const { caricaCorsi, getTitoloCorso } = useCorsi()

onMounted(async () => {
  await caricaCorsi()
  await carica()
})

async function carica() {
  loading.value = true
  try {
    const tutte = await getPrenotazioni({ stato: 'conflitto' })
    conflitti.value = tutte
    tutte.forEach(p => { azione[p.id] = { loading: false, showRifiuto: false, motivo: '' } })
  } finally {
    loading.value = false
  }
}

function toggleRifiuto(id) {
  azione[id].showRifiuto = !azione[id].showRifiuto
  azione[id].motivo = ''
}

async function approva(p) {
  azione[p.id].loading = true
  try {
    await approvaRichiesta(p.id)
    uiStore.successo(`Prenotazione #${p.id} approvata.`)
    await carica()
  } catch (err) {
    uiStore.errore(err.response?.data?.detail ?? 'Errore.')
  } finally {
    azione[p.id].loading = false
  }
}

async function rifiuta(p) {
  azione[p.id].loading = true
  try {
    await rifiutaRichiesta(p.id, azione[p.id].motivo)
    uiStore.successo(`Prenotazione #${p.id} rifiutata.`)
    await carica()
  } catch (err) {
    uiStore.errore(err.response?.data?.detail ?? 'Errore.')
  } finally {
    azione[p.id].loading = false
  }
}
</script>