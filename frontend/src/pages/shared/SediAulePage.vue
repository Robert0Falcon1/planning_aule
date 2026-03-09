<template>
  <div class="page-sedi">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Sedi &amp; Aule</h2>
      <div class="ms-auto d-flex gap-2 align-items-center">
        <input v-model="dataConsulta" type="date" class="form-control form-control-sm" style="width:auto" :min="oggiISO"
          @change="caricaDisponibilita" />
        <span class="text-muted small">Disponibilità per data</span>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else>
      <div v-for="sede in sedi" :key="sede.id" class="mb-4">
        <div class="sede-header d-flex align-items-center gap-2 mb-3">
          <div class="d-flex justify-content-space-between align-items-flex-end w-100">
            <div class="d-flex">


              <svg class="icon icon-primary">
                <use :href="sprites + '#it-map-marker'"></use>
              </svg>
              <h4 class="mb-0 fw-bold">{{ sede.nome }}</h4>
            </div>
            <div class="d-flex">
              <small v-if="sede.citta?.toLowerCase() === 'torino'" class="text-muted ms-1">{{ sede.citta }} |</small>
              <span class="badge bg-primary-subtle text-primary ms-1">
                {{ auleDiSede(sede.id).length }} {{ auleDiSede(sede.id).length === 1 ? 'aula' : 'aule' }}
              </span>
            </div>
          </div>
        </div>

        <div class="row g-3">
          <div v-for="aula in auleDiSede(sede.id)" :key="aula.id" class="col-12 col-md-6 col-xl-4">
            <div class="card border-0 shadow-sm h-100 aula-card">
              <div class="card-header bg-white border-bottom-0 pb-0 d-flex justify-content-between align-items-start">
                <div>
                  <h6 class="fw-bold mb-0">{{ aula.nome }}</h6>
                  <small class="text-muted">Capienza: {{ aula.capienza }} posti</small>
                </div>
                <span class="badge rounded-pill" :class="aulaLibera(aula.id) ? 'bg-success' : 'bg-warning text-dark'">
                  {{ aulaLibera(aula.id) ? 'Libera' : 'Prenotata' }}
                </span>
              </div>

              <div class="card-body pt-2 mx-2">
                <!-- Barra occupazione -->
                <div class="mb-3">
                  <div class="d-flex justify-content-between mb-1">
                    <small class="text-muted">Occupazione {{ dataFormattata }}</small>
                    <small class="fw-semibold">{{ pctAula(aula.id) }}%</small>
                  </div>
                  <div class="progress" style="height:6px">
                    <div class="progress-bar" :class="barraColore(pctAula(aula.id))"
                      :style="{ width: pctAula(aula.id) + '%' }"></div>
                  </div>
                </div>

                <!-- Slot orari 08-18 -->
                <div class="slot-grid mb-3">
                  <div v-for="h in oreGiornata" :key="h" class="slot"
                    :class="slotOccupato(aula.id, h) ? 'slot--occupato' : 'slot--libero'"
                    :title="slotOccupato(aula.id, h) ? `Occupato alle ${h}:00` : `Libero alle ${h}:00`">
                    <span class="slot-label">{{ h }}</span>
                  </div>
                </div>

                <!-- Prenotazioni del giorno -->
                <div v-if="prenotazioniAula(aula.id).length">
                  <small class="text-muted d-block mb-1 fw-semibold">Prenotazioni:</small>
                  <div v-for="item in prenotazioniAula(aula.id)" :key="item.prenId + '-' + item.slotIdx"
                    class="prenotazione-chip">
                    <span class="fw-semibold">{{ item.oraInizio }}–{{ item.oraFine }}</span>
                    <span class="ms-2 text-truncate text-muted small">Corso {{ item.corsoId }}</span>
                  </div>
                </div>
                <div v-else>
                  <small class="text-muted">Nessuna prenotazione per questa data.</small>
                </div>
              </div>

              <!-- Footer: pulsante sempre visibile -->
              <div class="card-footer bg-white border-0 pt-0">
                <RouterLink
                  :to="{ name: 'NuovaPrenotazione', query: { aula_id: aula.id, sede_id: sede.id, data: dataConsulta } }"
                  class="btn btn-sm w-100" :class="aulaLibera(aula.id) ? 'btn-outline-primary' : 'btn-outline-warning'">
                  <svg class="icon icon-sm me-1">
                    <use :href="sprites + '#it-plus-circle'"></use>
                  </svg>
                  Prenota per {{ dataFormattata }}
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!sedi.length" class="text-center text-muted py-5">Nessuna sede trovata.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSedi } from '@/api/sedi'
import { getAule } from '@/api/aule'
import { getPrenotazioni } from '@/api/prenotazioni'
import { oggi } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const loading = ref(false)
const sedi = ref([])
const aule = ref([])
const prenotazioni = ref([])
const oggiISO = oggi()
const dataConsulta = ref(oggiISO)

const oreGiornata = Array.from({ length: 11 }, (_, i) => i + 8) // 08–18

// Data formattata DD/MM/YYYY per la visualizzazione
const dataFormattata = computed(() => {
  if (!dataConsulta.value) return ''
  const [y, m, d] = dataConsulta.value.split('-')
  return `${d}/${m}/${y}`
})

function auleDiSede(sedeId) {
  return aule.value.filter(a => a.sede_id === sedeId)
}

function barraColore(pct) {
  return pct >= 80 ? 'bg-danger' : pct >= 50 ? 'bg-warning' : 'bg-success'
}

const eventiPerAula = computed(() => {
  const map = {}
  for (const p of prenotazioni.value) {
    if (p.stato === 'annullata' || p.stato === 'rifiutata') continue
    for (let si = 0; si < (p.slots?.length || 0); si++) {
      const slot = p.slots[si]
      if (slot?.data !== dataConsulta.value) continue
      const aulaId = p.aula_id
      if (!map[aulaId]) map[aulaId] = []
      map[aulaId].push({

        prenId: p.id,
        slotIdx: si,
        corsoId: p.corso_id,
        oraInizio: slot.ora_inizio?.slice(0, 5) || '',
        oraFine: slot.ora_fine?.slice(0, 5) || '',
        oraH: parseInt(slot.ora_inizio?.slice(0, 2) || '0'),
        oraFineH: parseInt(slot.ora_fine?.slice(0, 2) || '0'),
      })
      map[aulaId].sort((a, b) => a.oraH - b.oraH)
    }
  }
  // Ordina ogni lista per ora di inizio
  for (const id of Object.keys(map)) {
    map[id].sort((a, b) => a.oraH - b.oraH)
  }
  return map
})

function prenotazioniAula(aulaId) { return eventiPerAula.value[aulaId] || [] }
function slotOccupato(aulaId, ora) {
  return (eventiPerAula.value[aulaId] || []).some(e => ora >= e.oraH && ora < e.oraFineH)
}
function aulaLibera(aulaId) { return (eventiPerAula.value[aulaId] || []).length === 0 }
function pctAula(aulaId) {
  const oreOccupate = oreGiornata.filter(h => slotOccupato(aulaId, h)).length
  return Math.round((oreOccupate / oreGiornata.length) * 100)
}

async function caricaDisponibilita() {
  if (!dataConsulta.value) return
  loading.value = true
  try {
    const data = await getPrenotazioni({ data_dal: dataConsulta.value, data_al: dataConsulta.value })
    prenotazioni.value = Array.isArray(data) ? data : (data?.items || [])
  } catch (e) {
    console.warn('Disponibilità:', e.message)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const [dataSedi, dataAule] = await Promise.all([getSedi(), getAule()])
    sedi.value = Array.isArray(dataSedi) ? dataSedi : []
    aule.value = Array.isArray(dataAule) ? dataAule : []
    await caricaDisponibilita()
  } catch (e) {
    console.warn('SediAule:', e.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title {
  font-size: 1.4rem;
  font-weight: 700;
}

.sede-header {
  padding-bottom: .5rem;
  border-bottom: 2px solid #e8eaf0;
}

.aula-card {
  border-radius: 12px;
}

.slot-grid {
  display: flex;
  gap: 3px;
  flex-wrap: wrap;
}

.slot {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: default;
}

.slot-label {
  font-size: .6rem;
  font-weight: 600;
}

.slot--libero {
  background: #d4edda;
  color: #155724;
}

.slot--occupato {
  background: #f8d7da;
  color: #721c24;
}

.prenotazione-chip {
  display: flex;
  align-items: center;
  background: #f0f4ff;
  border-left: 3px solid #0066cc;
  border-radius: 4px;
  padding: 3px 8px;
  font-size: .78rem;
  margin-bottom: 4px;
  overflow: hidden;
}
</style>