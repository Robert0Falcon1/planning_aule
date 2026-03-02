<template>
  <!--
    Dashboard Operativa + Supervisione
    Per: Responsabile Corso, Segreteria Didattica, Segreteria di Sede
    Permessi: OPERATIVI (gestione proprie prenotazioni) + SUPERVISIONE (visione globale)
  -->
  <div>
    <div class="mb-4">
      <h2 class="h4 fw-bold">👋 Benvenuto, {{ authStore.nomeCompleto }}</h2>
      <p class="text-muted">Gestisci le tue prenotazioni e monitora lo stato complessivo delle aule.</p>
    </div>

    <!-- Metriche rapide -->
    <div class="row g-3 mb-5">
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Le Mie Prenotazioni" :valore="stats.mie" colore="primary" icon="it-list" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Confermate" :valore="stats.confermate" colore="success" icon="it-check-circle" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Con Conflitto" :valore="stats.conflitti" colore="warning" icon="it-warning-circle" />
      </div>
      <div class="col-sm-6 col-lg-3">
        <StatCard titolo="Oggi" :valore="stats.oggi" colore="info" icon="it-calendar" />
      </div>
    </div>

    <!-- SEZIONE OPERATIVA -->
    <div class="mb-3">
      <h4 class="fw-semibold">⚡ Azioni Rapide</h4>
      <p class="text-muted small">Gestisci le tue prenotazioni</p>
    </div>

    <div class="row g-3 mb-5">
      <div class="col-lg-3 col-md-6">
        <router-link :to="{ name: 'NuovaPrenotazione' }" class="text-decoration-none">
          <div class="card shadow-sm h-100 border-0 hover-card">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <div class="rounded-circle bg-primary bg-opacity-10 p-2 me-2">
                  <svg class="icon icon-primary"><use href="#it-plus-circle"></use></svg>
                </div>
                <h6 class="mb-0">Nuova Prenotazione</h6>
              </div>
              <p class="text-muted small mb-0">Prenota un'aula per una lezione singola</p>
            </div>
          </div>
        </router-link>
      </div>

      <div class="col-lg-3 col-md-6">
        <router-link :to="{ name: 'PrenotazioneMassiva' }" class="text-decoration-none">
          <div class="card shadow-sm h-100 border-0 hover-card">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <div class="rounded-circle bg-primary bg-opacity-10 p-2 me-2">
                  <svg class="icon icon-primary"><use href="#it-refresh"></use></svg>
                </div>
                <h6 class="mb-0">Prenotazione Massiva</h6>
              </div>
              <p class="text-muted small mb-0">Prenota più date ricorrenti</p>
            </div>
          </div>
        </router-link>
      </div>

      <div class="col-lg-3 col-md-6">
        <router-link :to="{ name: 'MiePrenotazioni' }" class="text-decoration-none">
          <div class="card shadow-sm h-100 border-0 hover-card">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <div class="rounded-circle bg-success bg-opacity-10 p-2 me-2">
                  <svg class="icon icon-success"><use href="#it-list"></use></svg>
                </div>
                <h6 class="mb-0">Le Mie Prenotazioni</h6>
              </div>
              <p class="text-muted small mb-0">Visualizza e gestisci le tue prenotazioni</p>
            </div>
          </div>
        </router-link>
      </div>

      <div class="col-lg-3 col-md-6">
        <router-link :to="{ name: 'ConflittiPage' }" class="text-decoration-none">
          <div class="card shadow-sm h-100 border-0 hover-card" :class="stats.conflitti > 0 ? 'border-start border-4 border-warning' : ''">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <div class="rounded-circle bg-warning bg-opacity-10 p-2 me-2">
                  <svg class="icon icon-warning"><use href="#it-warning-circle"></use></svg>
                </div>
                <h6 class="mb-0">Conflitti</h6>
              </div>
              <p class="text-muted small mb-0">
                {{ stats.conflitti > 0 ? `${stats.conflitti} conflitto/i da risolvere` : 'Nessun conflitto' }}
              </p>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- SEZIONE SUPERVISIONE -->
    <div class="mb-3">
      <h4 class="fw-semibold">👁️ Supervisione</h4>
      <p class="text-muted small">Monitora lo stato complessivo delle aule e genera report</p>
    </div>

    <div class="row g-3 mb-5">
      <div class="col-lg-4 col-md-6">
        <router-link :to="{ name: 'VistaGiornaliera' }" class="text-decoration-none">
          <div class="card shadow-sm h-100 border-0 hover-card">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <div class="rounded-circle bg-info bg-opacity-10 p-2 me-2">
                  <svg class="icon icon-info"><use href="#it-calendar"></use></svg>
                </div>
                <h6 class="mb-0">Vista Giornaliera</h6>
              </div>
              <p class="text-muted small mb-0">Stato aule per giorno (default: oggi)</p>
            </div>
          </div>
        </router-link>
      </div>

      <div class="col-lg-4 col-md-6">
        <router-link :to="{ name: 'SaturazioneSpazi' }" class="text-decoration-none">
          <div class="card shadow-sm h-100 border-0 hover-card">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <div class="rounded-circle bg-secondary bg-opacity-10 p-2 me-2">
                  <svg class="icon icon-secondary"><use href="#it-chart-line"></use></svg>
                </div>
                <h6 class="mb-0">Saturazione Aule</h6>
              </div>
              <p class="text-muted small mb-0">Analisi occupazione e capienza</p>
            </div>
          </div>
        </router-link>
      </div>

      <div class="col-lg-4 col-md-6">
        <router-link :to="{ name: 'Report' }" class="text-decoration-none">
          <div class="card shadow-sm h-100 border-0 hover-card">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <div class="rounded-circle bg-secondary bg-opacity-10 p-2 me-2">
                  <svg class="icon icon-secondary"><use href="#it-file"></use></svg>
                </div>
                <h6 class="mb-0">Report & Export</h6>
              </div>
              <p class="text-muted small mb-0">Genera report e esporta in CSV</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Prossime prenotazioni -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold d-flex justify-content-between align-items-center">
        <span>📅 Prossime Prenotazioni Confermate</span>
        <router-link :to="{ name: 'MiePrenotazioni' }" class="btn btn-sm btn-outline-primary">
          Vedi tutte →
        </router-link>
      </div>
      <div class="card-body p-0">
        <LoadingSpinner v-if="loading" />

        <div v-else-if="prossime.length === 0" class="p-4 text-muted text-center">
          Nessuna prenotazione confermata nei prossimi giorni.
        </div>

        <ul v-else class="list-group list-group-flush">
          <li
            v-for="p in prossime"
            :key="p.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <div>
              <div class="fw-semibold">
                Aula {{ p.aula_id }}
                <span v-if="p.stato === 'conflitto'" class="badge bg-warning text-dark ms-2">⚠️ Conflitto</span>
              </div>
              <small class="text-muted">
                {{ p.slots[0] ? formatData(p.slots[0].data) : '—' }}
                {{ p.slots[0] ? formatOra(p.slots[0].ora_inizio) + ' – ' + formatOra(p.slots[0].ora_fine) : '' }}
              </small>
            </div>
            <BadgeStato :stato="p.stato" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore }     from '@/stores/auth'
import { getPrenotazioni }  from '@/api/prenotazioni'
import { formatData, formatOra, oggi } from '@/utils/formatters'
import StatCard      from '@/components/ui/StatCard.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import BadgeStato    from '@/components/ui/BadgeStato.vue'

const authStore = useAuthStore()
const loading   = ref(false)
const prossime  = ref([])

const stats = reactive({ 
  mie: 0, 
  confermate: 0, 
  conflitti: 0,
  oggi: 0
})

const dataOggi = oggi()

onMounted(async () => {
  loading.value = true
  try {
    const tutte = await getPrenotazioni()
    stats.mie        = tutte.length
    stats.confermate = tutte.filter(p => p.stato === 'confermata').length
    stats.conflitti  = tutte.filter(p => p.stato === 'conflitto').length
    
    // Prenotazioni con almeno uno slot oggi
    stats.oggi = tutte.filter(p =>
      p.stato === 'confermata' &&
      p.slots?.some(s => s.data === dataOggi)
    ).length
    
    // Mostra le prossime 5 confermate o con conflitto
    prossime.value = tutte
      .filter(p => p.stato === 'confermata' || p.stato === 'conflitto')
      .slice(0, 5)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.hover-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15) !important;
}
</style>
