<template>
  <!--
    Pagina di login a schermo intero.
    Usa le classi Bootstrap Italia per il layout a due colonne (hero + form).
  -->
  <div class="it-hero-wrapper bg-primary d-flex align-items-center min-vh-100">
    <div class="container">
      <div class="row justify-content-center">

        <!-- Card login -->
        <div class="col-12 col-sm-10 col-md-8 col-lg-5">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">

              <!-- Intestazione -->
              <div class="text-center mb-4">
                <h1 class="h3 fw-bold text-primary">🏫 ICE Planning Aule</h1>
                <p class="text-muted small">Accedi con le tue credenziali aziendali</p>
              </div>

              <!-- Form di login -->
              <form @submit.prevent="handleLogin" novalidate>

                <!-- Email -->
                <div class="mb-3">
                  <label for="email" class="form-label fw-semibold">Email</label>
                  <input
                    id="email"
                    v-model="form.email"
                    type="email"
                    class="form-control"
                    :class="{ 'is-invalid': errori.email }"
                    placeholder="nome@inforcoop.it"
                    autocomplete="username"
                    required
                  />
                  <div v-if="errori.email" class="invalid-feedback">{{ errori.email }}</div>
                </div>

                <!-- Password -->
                <div class="mb-4">
                  <label for="password" class="form-label fw-semibold">Password</label>
                  <input
                    id="password"
                    v-model="form.password"
                    type="password"
                    class="form-control"
                    :class="{ 'is-invalid': errori.password }"
                    placeholder="••••••••"
                    autocomplete="current-password"
                    required
                  />
                  <div v-if="errori.password" class="invalid-feedback">{{ errori.password }}</div>
                </div>

                <!-- Messaggio di errore login -->
                <div v-if="erroreLogin" class="alert alert-danger py-2 small mb-3">
                  {{ erroreLogin }}
                </div>

                <!-- Submit -->
                <button
                  type="submit"
                  class="btn btn-primary w-100"
                  :disabled="loading"
                >
                  <span v-if="loading" class="progress-spinner progress-spinner-sm me-2" role="status" />
                  {{ loading ? 'Accesso in corso…' : 'Entra →' }}
                </button>
              </form>

              <!-- Credenziali di test (solo in sviluppo) -->
              <div v-if="isDev" class="mt-4 p-3 bg-light rounded small">
                <p class="fw-semibold mb-1">🔑 Credenziali di test:</p>
                <div
                  v-for="utente in utentiTest"
                  :key="utente.email"
                  class="d-flex justify-content-between align-items-center py-1 border-bottom cursor-pointer"
                  style="cursor: pointer"
                  @click="compilaTest(utente)"
                >
                  <span>{{ utente.label }}</span>
                  <code class="text-primary small">{{ utente.email }}</code>
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
import { ref, reactive } from 'vue'
import { useRouter }     from 'vue-router'
import { useAuthStore }  from '@/stores/auth'

const authStore  = useAuthStore()
const router     = useRouter()

// ── Stato del form ─────────────────────────────────────────────────────────
const form = reactive({ email: '', password: '' })
const errori     = reactive({ email: '', password: '' })
const erroreLogin = ref('')
const loading     = ref(false)

// Mostra i test users solo in sviluppo (Vite usa import.meta.env)
const isDev = import.meta.env.DEV

/** Utenti di test per compilazione rapida */
const utentiTest = [
  { label: 'Responsabile Corso',   email: 'responsabile@test.it', password: 'Test1234!' },
  { label: 'Segreteria Sede',      email: 'segr.sede@test.it',    password: 'Test1234!' },
  { label: 'Responsabile Sede',    email: 'resp.sede@test.it',    password: 'Test1234!' },
  { label: 'Segreteria Didattica', email: 'segr.did@test.it',     password: 'Test1234!' },
  { label: 'Coordinamento',        email: 'coord@test.it',        password: 'Test1234!' },
]

/** Compila il form con le credenziali di test al click */
function compilaTest(utente) {
  form.email    = utente.email
  form.password = utente.password
}

// ── Validazione client-side ────────────────────────────────────────────────
function valida() {
  errori.email    = form.email    ? '' : 'Inserisci l\'email'
  errori.password = form.password ? '' : 'Inserisci la password'
  return !errori.email && !errori.password
}

// ── Submit ─────────────────────────────────────────────────────────────────
async function handleLogin() {
  erroreLogin.value = ''
  if (!valida()) return

  loading.value = true
  try {
    await authStore.login(form.email, form.password)
    router.push({ name: 'Dashboard' })
  } catch (err) {
    const msg = err.response?.data?.detail ?? 'Errore di accesso. Riprova.'
    erroreLogin.value = msg
  } finally {
    loading.value = false
  }
}
</script>
