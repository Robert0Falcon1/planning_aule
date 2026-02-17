<template>
  <div>
    <h2 class="h4 fw-bold mb-4">📋 Le Mie Prenotazioni</h2>

    <!-- Filtri -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-sm-4">
            <label class="form-label small fw-semibold">Stato</label>
            <select v-model="filtri.stato" class="form-select form-select-sm">
              <option value="">Tutti gli stati</option>
              <option v-for="(cfg, val) in STATI_BADGE" :key="val" :value="val">
                {{ cfg.icon }} {{ cfg.label }}
              </option>
            </select>
          </div>
          <div class="col-sm-3">
            <label class="form-label small fw-semibold">Dal</label>
            <input v-model="filtri.data_dal" type="date" class="form-control form-control-sm" />
          </div>
          <div class="col-sm-3">
            <label class="form-label small fw-semibold">Al</label>
            <input v-model="filtri.data_al" type="date" class="form-control form-control-sm" />
          </div>
          <div class="col-sm-2">
            <button class="btn btn-outline-primary btn-sm w-100" @click="carica">
              🔍 Filtra
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista prenotazioni -->
    <LoadingSpinner v-if="loading" />

    <div v-else-if="prenotazioni.length === 0" class="alert alert-info">
      Nessuna prenotazione trovata con i filtri selezionati.
    </div>

    <div v-else class="accordion" id="accordionPrenotazioni">
      <div
        v-for="p in prenotazioni"
        :key="p.id"
        class="accordion-item border-0 shadow-sm mb-2"
      >
        <!-- Intestazione accordion -->
        <h3 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            :data-bs-target="`#collapse-${p.id}`"
            data-bs-toggle="collapse"
          >
            <div class="d-flex align-items-center gap-3 flex-wrap">
              <BadgeStato :stato="p.stato" />
              <span class="fw-semibold">Prenotazione #{{ p.id }}</span>
              <span class="text-muted small">
                {{ p.tipo === 'singola' ? '📅 Singola' : '🔄 Massiva' }} |
                Aula {{ p.aula_id }} | Corso {{ p.corso_id }}
              </span>
              <span v-if="p.slots?.length" class="text-muted small">
                Dal {{ formatData(p.slots[0]?.data) }}
              </span>
            </div>
          </button>
        </h3>

        <!-- Corpo accordion: lista degli slot -->
        <div :id="`collapse-${p.id}`" class="accordion-collapse collapse">
          <div class="accordion-body bg-light">
            <div class="row g-3">
              <div class="col-md-6">
                <p class="small mb-1"><strong>Tipo:</strong> {{ p.tipo }}</p>
                <p class="small mb-1"><strong>Aula ID:</strong> {{ p.aula_id }}</p>
                <p class="small mb-1"><strong>Corso ID:</strong> {{ p.corso_id }}</p>
                <p v-if="p.note" class="small mb-0"><strong>Note:</strong> {{ p.note }}</p>
              </div>
              <div class="col-md-6">
                <p class="small fw-semibold mb-1">Slot orari ({{ p.slots?.length ?? 0 }}):</p>
                <div
                  v-if="p.slots?.length"
                  class="overflow-auto"
                  style="max-height: 150px;"
                >
                  <div
                    v-for="s in p.slots"
                    :key="`${p.id}-${s.data}-${s.ora_inizio}`"
                    class="small border-bottom py-1"
                  >
                    {{ formatData(s.data) }} — {{ formatOra(s.ora_inizio) }} / {{ formatOra(s.ora_fine) }}
                  </div>
                </div>
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
import { getPrenotazioni }           from '@/api/prenotazioni'
import { formatData, formatOra }     from '@/utils/formatters'
import { STATI_BADGE }               from '@/utils/constants'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import BadgeStato     from '@/components/ui/BadgeStato.vue'

const loading      = ref(false)
const prenotazioni = ref([])

const filtri = reactive({ stato: '', data_dal: '', data_al: '' })

async function carica() {
  loading.value = true
  try {
    prenotazioni.value = await getPrenotazioni({
      stato:    filtri.stato    || undefined,
      data_dal: filtri.data_dal || undefined,
      data_al:  filtri.data_al  || undefined,
    })
  } finally {
    loading.value = false
  }
}

onMounted(carica)
</script>
