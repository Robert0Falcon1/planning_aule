<template>
  <div class="page-conflitti">
    <div class="page-header d-flex flex-wrap gap-3 align-items-center mb-4">
      <h2 class="page-title mb-0">Conflitti</h2>

      <!-- Conflitti + numero -->
      <span v-if="numeroConflitti" class="badge bg-danger fs-6 ms-1">{{ numeroConflitti }}</span>


      <div class="ms-auto d-flex gap-2 align-items-center">



        <!-- Solo attivi -->
        <div class="form-check form-switch mb-0 ps-0 me-3">
          <input class="form-check-input" type="checkbox" id="soloAttivi" v-model="soloAttivi" @change="carica" />
          <label class="form-check-label small" for="soloAttivi">Solo attivi</label>
        </div>

        <!-- Filtro Sedi -->
        <select v-model="filtroSede" class="form-select form-select-sm" style="width:auto" @change="carica">
          <option value="">Tutte le sedi</option>
          <option v-for="s in sedi" :key="s.id" :value="s.id">{{ s.nome }}</option>
        </select>

        <!-- Filtro utenti multi-selezione (max 2) -->
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown"
            style="min-width: 180px">
            <span v-if="!filtroUtenti.length">Filtra per utente</span>
            <span v-else-if="filtroUtenti.length === 1">1 utente</span>
            <span v-else>2 utenti</span>
          </button>
          <div class="dropdown-menu p-2" style="max-height: 300px; overflow-y: auto; min-width: 250px">
            <div class="small text-muted mb-2 px-2">Seleziona max 2 utenti</div>
            <div v-for="u in opzioniUtenti" :key="u.value" class="form-check">
              <input :id="`user-${u.value}`" v-model="filtroUtenti" :value="u.value" type="checkbox"
                class="form-check-input" :disabled="filtroUtenti.length >= 2 && !filtroUtenti.includes(u.value)" />
              <label :for="`user-${u.value}`" class="form-check-label small">
                {{ u.label }}
              </label>
            </div>
            <div v-if="filtroUtenti.length > 0" class="border-top mt-2 pt-2">
              <button class="btn btn-sm btn-outline-secondary w-100" @click.stop="filtroUtenti = []">
                Cancella selezione
              </button>
            </div>
          </div>
        </div>

        <!-- Aggiorna -->
        <button class="btn btn-sm btn-outline-secondary" @click="carica">
          <svg class="icon icon-sm me-1">
            <use :href="sprites + '#it-refresh'"></use>
          </svg>
          Aggiorna
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="!conflitti.length" class="card border-0 shadow-sm">
      <div class="card-body text-center py-5">
        <svg class="icon icon-xl text-success mb-3">
          <use :href="sprites + '#it-check-circle'"></use>
        </svg>
        <h5 class="text-success">Nessun conflitto rilevato</h5>
        <p class="text-muted mb-0">Tutte le prenotazioni sono coerenti.</p>
      </div>
    </div>

    <div v-else>
      <div class="d-flex flex-column gap-3">
        <div v-for="gruppo in conflittiRaggruppati" :key="gruppo.chiave" class="card border-0 shadow-sm">

          <!-- Header: Dati comuni -->
          <div class="card-header bg-white">
            <div class="d-flex gap-3 align-items-center flex-wrap">
              <span class="badge bg-danger">
                {{ gruppo.slots.length }} prenotazion{{ gruppo.slots.length > 1 ? 'i' : 'e' }} in conflitto
              </span>
              <div class="d-flex align-items-center gap-1">
                <svg class="icon icon-sm text-primary">
                  <use :href="sprites + '#it-map-marker'"></use>
                </svg>
                <strong class="small">Sede:</strong>
                <span class="small">{{ sedeDiAulaFn(gruppo.aula) }}</span>
              </div>
              <div class="d-flex align-items-center gap-1">
                <i class="bi bi-door-open"></i>
                <strong class="small pe-1">Aula:</strong>
                <span :style="getAulaBadgeStyle(nomeAulaFn(gruppo.aula))"></span>
                <span class="small">{{ nomeAulaFn(gruppo.aula) }}</span>
              </div>
              <div class="d-flex align-items-center gap-1">
                <svg class="icon icon-sm text-primary">
                  <use :href="sprites + '#it-calendar'"></use>
                </svg>
                <strong class="small">Data:</strong>
                <span class="small">{{ formatData(gruppo.data) }}</span>
              </div>
              <small class="ms-auto text-muted">Rilevato il {{ formatData(gruppo.rilevato_il) }}</small>
            </div>
          </div>

          <!-- Corpo: Lista slot in conflitto -->
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-sm align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th style="width: 40px;"></th>
                    <!-- <th>Utente</th> -->
                    <th>Corso</th>
                    <th>Orario</th>
                    <th>Data Prenotazione</th>
                    <th>Note</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="slot in gruppo.slots" :key="slot.slotId" :class="{
                    'table-success': gruppoRisolto(gruppo)
                      ? slot.slotId === slotVincitore(gruppo)
                      : slotSelezionati[gruppo.chiave] === slot.slotId,
                    'table-danger': gruppoRisolto(gruppo) && slot.slotId !== slotVincitore(gruppo)
                  }">
                    <td class="text-center">
                      <!-- Mostra radio solo se NON risolto -->
                      <input v-if="!gruppoRisolto(gruppo)" type="radio" :name="`gruppo-${gruppo.chiave}`"
                        :value="slot.slotId" v-model="slotSelezionati[gruppo.chiave]" class="form-check-input" />
                      <!-- Mostra check verde se vincitore -->
                      <svg v-else-if="slot.slotId === slotVincitore(gruppo)" class="icon icon-sm text-success">
                        <use :href="sprites + '#it-check-circle'"></use>
                      </svg>
                      <!-- Mostra X rossa per tutti i perdenti -->
                      <svg v-else class="icon icon-sm text-danger">
                        <use :href="sprites + '#it-close-circle'"></use>
                      </svg>
                    </td>
                    <!-- <td>
                      <svg class="icon icon-xs me-1">
                        <use :href="sprites + '#it-user'"></use>
                      </svg>
                      <span class="small">{{ nomeUtente(slot.richiedenteId) }}</span>
                    </td> -->
                    <td>
                      <svg class="icon icon-xs me-1">
                        <use :href="sprites + '#it-bookmark'"></use>
                      </svg>
                      <code class="small">{{ slot.corsoId }}</code>
                    </td>
                    <td>
                      <svg class="icon icon-xs me-1">
                        <use :href="sprites + '#it-clock'"></use>
                      </svg>
                      <span class="small fw-semibold">{{ slot.oraInizio }} – {{ slot.oraFine }}</span>
                    </td>
                    <td>
                      <svg class="icon icon-xs me-1">
                        <use :href="sprites + '#it-calendar'"></use>
                      </svg>
                      <span class="small text-muted">{{ formatData(slot.dataCreazione) }}</span>
                    </td>
                    <td>
                      <svg class="icon icon-xs me-1">
                        <use :href="sprites + '#it-comment'"></use>
                      </svg>
                      <span v-if="slot.note" class="small text-muted fst-italic">{{ slot.note }}</span>
                      <span v-else class="text-muted small">—</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Footer: Azioni -->
          <div class="card-footer bg-white">
            <!-- Se risolto: mostra badge -->
            <div v-if="gruppoRisolto(gruppo)" class="d-flex align-items-center gap-2 justify-content-space-between">
              <span class="badge bg-success">
                <svg class="icon icon-xs me-1 filter-invert">
                  <use :href="sprites + '#it-check'"></use>
                </svg>
                Conflitto risolto
              </span>
              <small class="text-muted ms-2">
                Risolto il {{formatData(gruppo.conflittiIds.map(id => conflitti.find(c => c.id ===
                  id)?.risolto_il).filter(Boolean)[0])}}
              </small>
            </div>
            <!-- Altrimenti: mostra form risoluzione -->
            <div v-else class="d-flex align-items-center gap-2">
              <small class="text-muted">
                <svg class="icon icon-xs me-1">
                  <use :href="sprites + '#it-info-circle'"></use>
                </svg>
                Seleziona quale prenotazione mantenere. Le altre verranno annullate.
              </small>
              <button class="btn btn-sm btn-success ms-auto" @click="risolviGruppo(gruppo)"
                :disabled="!slotSelezionati[gruppo.chiave] || risolvendo === gruppo.chiave">
                <span v-if="risolvendo === gruppo.chiave" class="spinner-border spinner-border-sm me-1"></span>
                Risolvi conflitto
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import { getConflitti, getPrenotazione, annullaSlot } from '@/api/prenotazioni'
import { getSedi } from '@/api/sedi'
import { useAule } from '@/composables/useAule'
import { useAulaColor } from '@/composables/useAulaColor'
import { formatData } from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
import { getUtenti } from '@/api/utenti'
import { useSedePerFiltro } from '@/composables/useSedePerFiltro'

const { nomeAula: nomeAulaFn, sedeDiAula: sedeDiAulaFn, carica: caricaAule } = useAule()
const { getAulaBadgeStyle } = useAulaColor()
const uiStore = useUiStore()
const utenti = ref([])
const loading = ref(false)
const conflitti = ref([])
const prenotazioni = ref([])
const sedi = ref([])
const filtroSede = ref('')
const filtroUtenti = ref([])
const soloAttivi = ref(true)
const risolvendo = ref(null)
const { sedeDefaultFiltro } = useSedePerFiltro()

// Per ogni gruppo, memorizza lo slot selezionato
const slotSelezionati = ref({})

const mappaPrenotazioni = computed(() =>
  Object.fromEntries(prenotazioni.value.map(p => [p.id, p]))
)
function prenById(id) { return mappaPrenotazioni.value[id] || null }

const mappaUtenti = computed(() =>
  Object.fromEntries(utenti.value.map(u => [u.id, u]))
)

const opzioniUtenti = computed(() =>
  utenti.value
    .map(u => ({
      value: u.id,
      label: `${u.nome} ${u.cognome}`
    }))
    .sort((a, b) => a.label.localeCompare(b.label))
)

// Raggruppa conflitti per aula + data (indipendentemente dagli utenti)
const conflittiRaggruppati = computed(() => {
  let lista = conflitti.value

  // Filtra per utenti selezionati
  if (filtroUtenti.value.length >= 1) {
    lista = lista.filter(c => {
      const richA = prenById(c.prenotazione_id_1)?.richiedente_id
      const richB = prenById(c.prenotazione_id_2)?.richiedente_id
      return filtroUtenti.value.includes(richA) || filtroUtenti.value.includes(richB)
    })
  }

  // Raggruppa per: aula + data
  const gruppi = new Map()

  for (const c of lista) {
    const slot1 = infoSlot(c, 1)
    const slot2 = infoSlot(c, 2)
    const aula = slot1?.aula_id || slot2?.aula_id
    const data = slot1?.data || slot2?.data

    if (!aula || !data) continue

    const chiave = `${aula}_${data}`

    if (!gruppi.has(chiave)) {
      gruppi.set(chiave, {
        chiave,
        aula,
        data,
        slotsInConflitto: new Map(), // Map<slotId, slotInfo>
        conflittiIds: [],
        rilevato_il: c.rilevato_il,
      })
    }

    const gruppo = gruppi.get(chiave)
    gruppo.conflittiIds.push(c.id)

    // Aggiungi entrambi gli slot al gruppo (se non già presenti) - INCLUSI quelli annullati
    if (slot1 && !gruppo.slotsInConflitto.has(slot1.id)) {
      const pren1 = prenById(c.prenotazione_id_1)
      gruppo.slotsInConflitto.set(slot1.id, {
        slotId: slot1.id,
        prenId: c.prenotazione_id_1,
        richiedenteId: pren1?.richiedente_id,
        corsoId: slot1.corso_id,
        oraInizio: slot1.ora_inizio?.slice(0, 5),
        oraFine: slot1.ora_fine?.slice(0, 5),
        note: slot1.note || '',
        dataCreazione: pren1?.data_creazione,
        annullato: slot1.annullato,  // ← AGGIUNTO per sapere se è annullato
      })
    }

    if (slot2 && !gruppo.slotsInConflitto.has(slot2.id)) {
      const pren2 = prenById(c.prenotazione_id_2)
      gruppo.slotsInConflitto.set(slot2.id, {
        slotId: slot2.id,
        prenId: c.prenotazione_id_2,
        richiedenteId: pren2?.richiedente_id,
        corsoId: slot2.corso_id,
        oraInizio: slot2.ora_inizio?.slice(0, 5),
        oraFine: slot2.ora_fine?.slice(0, 5),
        note: slot2.note || '',
        dataCreazione: pren2?.data_creazione,
        annullato: slot2.annullato,  // ← AGGIUNTO per sapere se è annullato
      })
    }
  }

  // Converti Map in array e ordina cronologicamente
  return Array.from(gruppi.values())
    .map(g => ({
      ...g,
      slots: Array.from(g.slotsInConflitto.values())
        .sort((a, b) => a.oraInizio.localeCompare(b.oraInizio))
    }))
    .sort((a, b) => a.data.localeCompare(b.data))
})

const numeroConflitti = computed(() => conflittiRaggruppati.value.length)

// ← Verifica se un gruppo di conflitti è già risolto
function gruppoRisolto(gruppo) {
  // Un gruppo è risolto se TUTTI i suoi conflitti sono risolti
  return gruppo.conflittiIds.every(id => {
    const c = conflitti.value.find(cf => cf.id === id)
    return c && c.stato_risoluzione
  })
}

// ← Trova lo slot "vincitore" (quello mantenuto) in un gruppo risolto
function slotVincitore(gruppo) {
  console.log('🔍 Cerco vincitore per gruppo:', gruppo.chiave)
  console.log('   Conflitti IDs:', gruppo.conflittiIds)

  // STRATEGIA 1: Conta quanti slot NON sono annullati
  const slotsNonAnnullati = gruppo.slots.filter(s => !s.annullato)
  console.log('   📊 Slot non annullati:', slotsNonAnnullati.length, 'su', gruppo.slots.length)

  // Se c'è UN SOLO slot non annullato → è il vincitore (caso comune N-way)
  if (slotsNonAnnullati.length === 1) {
    console.log('   ✅ VINCITORE UNICO (slot non annullato):', slotsNonAnnullati[0].slotId)
    return slotsNonAnnullati[0].slotId
  }

  // Se TUTTI annullati → nessun vincitore (ELIMINATE_ENTRAMBE puro)
  if (slotsNonAnnullati.length === 0) {
    console.log('   ❌ Tutti slot annullati - nessun vincitore')
    return null
  }

  // STRATEGIA 2: Usa stato_risoluzione (caso 2-way classico con più slot attivi)
  for (const id of gruppo.conflittiIds) {
    const c = conflitti.value.find(cf => cf.id === id)
    if (!c || !c.stato_risoluzione) continue

    console.log(`   📋 Conflitto ${id}:`, {
      trovato: true,
      stato_risoluzione: c.stato_risoluzione,
      slot_id_1: c.slot_id_1,
      slot_id_2: c.slot_id_2
    })

    const stato = String(c.stato_risoluzione).toLowerCase()

    // MANTENUTA_1 → slot_id_1 vince
    if (stato.includes('mantenuta_1')) {
      console.log('   ✅ Vincitore da stato: slot_id_1 =', c.slot_id_1)
      return c.slot_id_1
    }
    // MANTENUTA_2 → slot_id_2 vince
    if (stato.includes('mantenuta_2')) {
      console.log('   ✅ Vincitore da stato: slot_id_2 =', c.slot_id_2)
      return c.slot_id_2
    }
    // ELIMINATE_ENTRAMBE → continua a cercare (potrebbero esserci altri conflitti)
  }

  console.log('   ❌ Nessun vincitore trovato')
  return null
}

function infoSlot(c, quale) {
  const prenId = quale === 1 ? c.prenotazione_id_1 : c.prenotazione_id_2
  const slotId = quale === 1 ? c.slot_id_1 : c.slot_id_2
  const pren = prenById(prenId)
  if (!pren) return null

  if (slotId) {
    const slot = pren.slots?.find(s => s.id === slotId)
    if (slot) return slot
  }
  return pren.slots?.find(s => !s.annullato) || pren.slots?.[0] || null
}

async function carica() {
  loading.value = true
  try {
    const params = { solo_attivi: soloAttivi.value }
    if (filtroSede.value) params.sede_id = filtroSede.value

    const dataConflitti = await getConflitti(params)

    if (Array.isArray(dataConflitti)) conflitti.value = dataConflitti
    else if (dataConflitti?.items) conflitti.value = dataConflitti.items
    else conflitti.value = []

    const prenIds = [...new Set(
      conflitti.value.flatMap(c => [c.prenotazione_id_1, c.prenotazione_id_2])
    )]

    try {
      const dataPren = prenIds.length
        ? await Promise.all(prenIds.map(id => getPrenotazione(id)))
        : []
      prenotazioni.value = dataPren.filter(Boolean)
    } catch (e) {
      console.warn('Errore caricamento prenotazioni per conflitti:', e.message)
      prenotazioni.value = []
    }

    // Reset selezioni
    slotSelezionati.value = {}

  } catch (e) {
    console.warn('Conflitti:', e.message)
    conflitti.value = []
  } finally {
    loading.value = false
  }
}

async function risolviGruppo(gruppo) {
  const slotDaMantenere = slotSelezionati.value[gruppo.chiave]

  if (!slotDaMantenere) {
    uiStore.errore('Seleziona quale slot mantenere')
    return
  }

  risolvendo.value = gruppo.chiave

  try {
    // Annulla tutti gli altri slot
    const slotsAnnullare = gruppo.slots.filter(s => s.slotId !== slotDaMantenere)

    // Annulla gli slot uno alla volta e gestisci errori
    for (const slot of slotsAnnullare) {
      try {
        await annullaSlot(slot.prenId, slot.slotId)
      } catch (e) {
        console.warn(`Slot ${slot.slotId} già annullato o errore:`, e.message)
        // Continua comunque con gli altri slot
      }
    }

    // ← NON chiamare risolviConflitto - il backend gestisce automaticamente
    //   la risoluzione quando annulli gli slot (vedi prenotazioni.py annulla_slot)

    const slotMantenuto = gruppo.slots.find(s => s.slotId === slotDaMantenere)
    const utente = mappaUtenti.value[slotMantenuto?.richiedenteId]
    const nomeCompleto = utente ? `${utente.nome} ${utente.cognome}` : 'utente'

    // uiStore.successo(`✓ Conflitto risolto: mantenuto slot di ${nomeCompleto}`)
    uiStore.successo(`✓ Conflitto risolto`)

    // ← REFRESH COMPLETO IMMEDIATO
    risolvendo.value = null

    // Svuota completamente i dati
    conflitti.value = []
    prenotazioni.value = []
    slotSelezionati.value = {}

    // Ricarica tutto da zero
    await carica()

  } catch (e) {
    uiStore.errore(e.message)
    risolvendo.value = null
  }
}

onMounted(async () => {
  await caricaAule()
  filtroSede.value = sedeDefaultFiltro.value
  const [dataSedi, dataUtenti] = await Promise.all([
    getSedi(),
    getUtenti()
  ])
  sedi.value = Array.isArray(dataSedi) ? dataSedi : []
  utenti.value = Array.isArray(dataUtenti) ? dataUtenti : (dataUtenti?.items || [])
  carica()
})

function nomeUtente(id) {
  const u = mappaUtenti.value[id]
  return u ? `${u.nome} ${u.cognome}` : `#${id}`
}
</script>

<style scoped>
.page-title {
  font-size: 1.4rem;
  font-weight: 700;
}

.conflitto-pill {
  padding: 12px 14px;
  border-radius: 8px;
  font-size: .82rem;
  line-height: 1.5;
}

.pill-a {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
}

.pill-b {
  background: #f8d7da;
  border-left: 4px solid #dc3545;
}
</style>