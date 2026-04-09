<template>
  <div
    class="login-bg d-flex align-items-center justify-content-center min-vh-100"
  >
    <div class="login-card card border-0 shadow-lg">
      <div class="card-body px-5 pt-5 pb-5">
        <!-- Logo / Brand -->
        <div class="text-center mb-4">
          <div class="mx-auto">
            <img class="logo-login ms-3" src="/img/logo_ICE.png" />
          </div>
          <p class="text-muted small">v1.0 beta</p>
        </div>

        <!-- Alert errore -->
        <div
          v-if="auth.errore"
          class="alert alert-danger py-2 small mb-3"
          role="alert"
        >
          {{ auth.errore }}
        </div>

        <!-- Form -->
        <form @submit.prevent="doLogin" novalidate>
          <div class="form-group mb-3">
            <label for="username" class="form-label fw-semibold"></label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errori.username }"
              autocomplete="username"
              placeholder="Inserisci username"
            />
            <div class="invalid-feedback">{{ errori.username }}</div>
          </div>

          <div class="form-group mb-4">
            <label for="password" class="form-label fw-semibold"></label>
            <div class="input-group">
              <input
                id="password"
                v-model="form.password"
                :type="showPwd ? 'text' : 'password'"
                class="form-control"
                :class="{ 'is-invalid': errori.password }"
                autocomplete="current-password"
                placeholder="••••••••"
              />
              <button
                type="button"
                class="btn"
                @click="showPwd = !showPwd"
                tabindex="-1"
              >
                <svg class="icon icon-sm">
                  <use
                    :href="`${sprites}#${showPwd ? 'it-password-invisible' : 'it-password-visible'}`"
                  ></use>
                </svg>
              </button>
              <div class="invalid-feedback">{{ errori.password }}</div>
            </div>
          </div>

          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="auth.loading"
          >
            <span
              v-if="auth.loading"
              class="spinner-border spinner-border-sm me-2"
              role="status"
            ></span>
            Accedi
          </button>
        </form>
      </div>
    </div>
  </div>

  <div class="container-fluid position-absolute" style="bottom: 0; z-index:-1">
    <div class="row">
      <div class="col-12">
        <div class="row py-3 mx-auto">
          <small class="text-center text-small">
                © {{ new Date().getFullYear() }} Inforcoop Ecipa Piemonte | Mirai v1.0 beta
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import sprites from "bootstrap-italia/dist/svg/sprites.svg?url";

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const form = reactive({ username: "", password: "" });
const errori = reactive({ username: "", password: "" });
const showPwd = ref(false);

function valida() {
  errori.username = form.username.trim() ? "" : "Username obbligatorio";
  errori.password = form.password ? "" : "Password obbligatoria";
  return !errori.username && !errori.password;
}

async function doLogin() {
  if (!valida()) return;
  const ok = await auth.login(form.username, form.password);
  if (ok) {
    const redirect = route.query.redirect || "/";
    router.push(redirect);
  }
}
</script>

<style scoped>
.login-bg {
  background: linear-gradient(135deg, #0066cc 0%, #004080 100%);
}

.login-card {
  width: 100%;
  max-width: 420px;
  border-radius: 16px;
}

.login-logo {
  width: 64px;
  height: 64px;
  background: #0066cc;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
