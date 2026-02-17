<template>
  <div>
    <h2 class="h4 fw-bold mb-4">📚 Prenotazioni per Corso</h2>

    <!-- Filtri -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-sm-4">
            <label class="form-label small fw-semibold">ID Corso</label>
            <input
              v-model.number="filtri.corso_id"
              type="number"
              class="form-control form-control-sm"
              placeholder="Es: 1"
            />
          </div>
          <div class="col-sm-3">
            <label class="form-label small fw-semibold">Stato</label>
            <select v-model="filtri.stato" class="form-select form-select-sm">
              <option value="">Tutti</option>
              <option v-for="(cfg, val) in STATI_BADGE" :key="val" :value="val">
                {{ cfg.icon }} {{ cfg.label }}
              </option>
            </select>
          </div>
          <div class="col-sm-3">
            <button class="btn btn-primary btn-sm w-100" @click="carica">
              🔍 Cerca
            </button>
          </div>
        </div>
      </div>
    </div>

    <LoadingSpinner v-if="loading" />

    <div v-else class="card border-0 shadow-sm">
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>ID</th><th>Aula</th><th>Corso</th><th>Stato</th><th>Slot</th><th>Dal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="prenotazioni.length === 0">
              <td colspan="6" class="text-center text-muted py-4">Nessun risultato</td>
            </tr>
            <tr v-for="p in prenotazioni" :key="p.id">
              <td>#{{ p.id }}</td>
              <td>{{ p.aula_id }}</td>
              <td>{{ p.corso_id }}</td>
              <td><BadgeStato :stato="p.stato" /></td>
              <td>{{ p.slots?.length ?? 0 }}</td>
              <td class="text-muted small">
                {{ p.slots?.[0] ? formatData(p.slots[0].data) : '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getPrenotazioni }   from '@/api/prenotazioni'
import { formatData }        from '@/utils/formatters'
import { STATI_BADGE }       from '@/utils/constants'
import LoadingSpinner        from '@/components/ui/LoadingSpinner.vue'
import BadgeStato            from '@/components/ui/BadgeStato.vue'

const loading      = ref(false)
const prenotazioni = ref([])
const filtri       = reactive({ corso_id: '', stato: '' })

onMounted(carica)

async function carica() {
  loading.value = true
  try {
    prenotazioni.value = await getPrenotazioni({
      corso_id: filtri.corso_id || undefined,
      stato:    filtri.stato    || undefined,
    })
  } finally {
    loading.value = false
  }
}
</script>
