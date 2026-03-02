<template>
  <div>
    <h2 class="h4 fw-bold mb-4">🔍 Verifica Slot Disponibili</h2>

    <div class="row">
      <div class="col-lg-5">
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-body p-4">
            <div class="mb-3">
              <label class="form-label fw-semibold">Sede</label>
              <select v-model="filtri.sede_id" class="form-select" @change="onSedeChange">
                <option value="">— Seleziona sede —</option>
                <option v-for="s in sedi" :key="s.id" :value="s.id">
                  {{ s.nome }} ({{ s.citta }})
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Aula</label>
              <select v-model="filtri.aula_id" class="form-select" :disabled="!filtri.sede_id">
                <option value="">— Seleziona aula —</option>
                <option v-for="a in aule" :key="a.id" :value="a.id">
                  {{ a.nome }} (cap. {{ a.capienza }})
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Data da verificare</label>
              <input v-model="filtri.data" type="date" class="form-control" />
            </div>
            <button
              class="btn btn-primary w-100"
              :disabled="!filtri.aula_id || !filtri.data || loading"
              @click="verifica"
            >
              {{ loading ? 'Verifica…' : '🔍 Verifica disponibilità' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Risultato -->
      <div class="col-lg-7">
        <div v-if="verificato" class="card border-0 shadow-sm">
          <div class="card-header bg-white fw-semibold">
            Disponibilità per il {{ formatData(filtri.data) }}
          </div>
          <div class="card-body">
            <LoadingSpinner v-if="loading" />

            <div v-else-if="slotOccupati.length === 0" class="text-center py-4">
              <div class="text-success h1">✅</div>
              <p class="text-success fw-semibold">Aula completamente libera!</p>
              <router-link :to="{ name: 'NuovaPrenotazione' }" class="btn btn-primary btn-sm">
                Prenota ora
              </router-link>
            </div>

            <div v-else>
              <p class="text-danger fw-semibold mb-3">
                ⚠️ {{ slotOccupati.length }} fascia/e oraria già occupata/e:
              </p>
              <div class="table-responsive">
                <table class="table table-sm">
                  <thead class="table-light">
                    <tr>
                      <th>Ora inizio</th>
                      <th>Ora fine</th>
                      <th>Prenotazione</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="s in slotOccupati" :key="`${s.prenotazione_id}-${s.ora_inizio}`">
                      <td>{{ formatOra(s.ora_inizio) }}</td>
                      <td>{{ formatOra(s.ora_fine) }}</td>
                      <td>#{{ s.prenotazione_id }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-muted text-center py-5">
          <p>Seleziona sede, aula e data per verificare la disponibilità.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getSedi }                   from '@/api/sedi'
import { getAule, getSlotOccupati }  from '@/api/aule'
import { formatData, formatOra }     from '@/utils/formatters'
import LoadingSpinner                from '@/components/ui/LoadingSpinner.vue'

const sedi         = ref([])
const aule         = ref([])
const slotOccupati = ref([])
const loading      = ref(false)
const verificato   = ref(false)

const filtri = reactive({ sede_id: '', aula_id: '', data: '' })

onMounted(async () => { sedi.value = await getSedi() })

async function onSedeChange() {
  filtri.aula_id = ''
  aule.value     = filtri.sede_id ? await getAule(filtri.sede_id) : []
}

async function verifica() {
  loading.value   = true
  verificato.value = true
  try {
    slotOccupati.value = await getSlotOccupati(filtri.aula_id, filtri.data, filtri.data)
  } finally {
    loading.value = false
  }
}
</script>
