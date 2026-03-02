<template>
  <div>
    <h2 class="h4 fw-bold mb-4">📬 Richieste Pendenti</h2>

    <LoadingSpinner v-if="loading" />

    <div v-else-if="richiestePendenti.length === 0" class="alert alert-success">
      ✅ Nessuna richiesta in attesa. Tutto in ordine!
    </div>

    <div v-else class="d-flex flex-column gap-3">
      <div
        v-for="p in richiestePendenti"
        :key="p.id"
        class="card border-0 shadow-sm"
        :class="{ 'border-start border-4 border-warning': p.stato === 'conflitto' }"
      >
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
            <!-- Info prenotazione -->
            <div>
              <div class="d-flex align-items-center gap-2 mb-1">
                <BadgeStato :stato="p.stato" />
                <span class="fw-semibold">Prenotazione #{{ p.id }}</span>
                <span class="badge bg-light text-dark">{{ p.tipo }}</span>
              </div>
              <div class="text-muted small">
                🏫 Aula {{ p.aula_id }} |
                📚 Corso {{ p.corso_id }} |
                📅 {{ p.slots?.length ?? 0 }} slot
                <span v-if="p.slots?.[0]">
                  — dal {{ formatData(p.slots[0].data) }}
                  {{ formatOra(p.slots[0].ora_inizio) }}–{{ formatOra(p.slots[0].ora_fine) }}
                </span>
              </div>
              <div v-if="p.note" class="small mt-1 text-muted fst-italic">
                Note: {{ p.note }}
              </div>
              <!-- Alert conflitti -->
              <div v-if="p.stato === 'conflitto'" class="alert alert-warning py-1 small mt-2 mb-0">
                ⚠️ Questa richiesta ha conflitti rilevati. Puoi comunque approvarla.
              </div>
            </div>

            <!-- Azioni -->
            <div class="d-flex flex-column gap-2" style="min-width: 200px;">
              <button
                class="btn btn-success btn-sm"
                :disabled="azione[p.id]?.loading"
                @click="approva(p)"
              >
                ✅ Approva
              </button>

              <!-- Form rifiuto inline -->
              <div v-if="azione[p.id]?.showRifiuto">
                <textarea
                  v-model="azione[p.id].motivo"
                  class="form-control form-control-sm mb-1"
                  rows="2"
                  placeholder="Motivo del rifiuto (obbligatorio)"
                />
                <div class="d-flex gap-1">
                  <button
                    class="btn btn-danger btn-sm flex-grow-1"
                    :disabled="!azione[p.id].motivo"
                    @click="rifiuta(p)"
                  >
                    ❌ Conferma rifiuto
                  </button>
                  <button
                    class="btn btn-outline-secondary btn-sm"
                    @click="azione[p.id].showRifiuto = false"
                  >
                    ✕
                  </button>
                </div>
              </div>
              <button
                v-else
                class="btn btn-outline-danger btn-sm"
                @click="azione[p.id] = { ...azione[p.id], showRifiuto: true, motivo: '' }"
              >
                ❌ Rifiuta
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUiStore }               from '@/stores/ui'
import { getPrenotazioni, approvaRichiesta, rifiutaRichiesta } from '@/api/prenotazioni'
import { formatData, formatOra }    from '@/utils/formatters'
import LoadingSpinner               from '@/components/ui/LoadingSpinner.vue'
import BadgeStato                   from '@/components/ui/BadgeStato.vue'

const uiStore          = useUiStore()
const loading          = ref(false)
const richiestePendenti = ref([])

// Stato per le azioni su ogni riga (approvazione/rifiuto)
const azione = reactive({})

onMounted(carica)

async function carica() {
  loading.value = true
  try {
    const tutte = await getPrenotazioni()
    // Mostra solo le prenotazioni in attesa di validazione (in_attesa e conflitto)
    richiestePendenti.value = tutte.filter(
      p => p.stato === 'in_attesa' || p.stato === 'conflitto',
    )
    // Inizializza stato azione per ogni prenotazione
    richiestePendenti.value.forEach(p => {
      azione[p.id] = { loading: false, showRifiuto: false, motivo: '' }
    })
  } finally {
    loading.value = false
  }
}

async function approva(p) {
  azione[p.id].loading = true
  try {
    // Il backend richiede l'id della RichiestaPrenotazione, non della Prenotazione.
    // Per ora usiamo p.id come fallback — da aggiornare quando l'endpoint /richieste sarà esposto.
    await approvaRichiesta(p.id)
    uiStore.successo(`Prenotazione #${p.id} approvata con successo.`)
    await carica()
  } catch (err) {
    uiStore.errore(err.response?.data?.detail ?? 'Errore durante l\'approvazione.')
  } finally {
    azione[p.id].loading = false
  }
}

async function rifiuta(p) {
  if (!azione[p.id].motivo.trim()) return
  azione[p.id].loading = true
  try {
    await rifiutaRichiesta(p.id, azione[p.id].motivo)
    uiStore.successo(`Prenotazione #${p.id} rifiutata.`)
    await carica()
  } catch (err) {
    uiStore.errore(err.response?.data?.detail ?? 'Errore durante il rifiuto.')
  } finally {
    azione[p.id].loading = false
  }
}
</script>
