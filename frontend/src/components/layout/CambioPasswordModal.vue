<template>
    <teleport to="body">
        <div v-if="aperta" class="modal fade show d-block" tabindex="-1" style="background:rgba(0,0,0,.5)">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">

                    <div class="modal-header">
                        <h5 class="modal-title">Cambia password</h5>
                        <button type="button" class="btn-close" @click="chiudi"></button>
                    </div>

                    <div class="modal-body">
                        <div v-if="esito" class="alert" :class="esito.tipo === 'ok' ? 'alert-success' : 'alert-danger'">
                            {{ esito.msg }}
                        </div>

                        <div class="mb-3">
                            <label class="form-label fw-semibold">Password attuale *</label>
                            <div class="input-group">
                                <input v-model="form.password_attuale" :type="showAttuale ? 'text' : 'password'"
                                    class="form-control" :class="{ 'is-invalid': err.password_attuale }"
                                    autocomplete="current-password" />
                                <button type="button" class="btn" @click="showAttuale = !showAttuale" tabindex="-1">
                                    <svg class="icon icon-sm">
                                        <use
                                            :href="`${sprites}#${showAttuale ? 'it-password-invisible' : 'it-password-visible'}`">
                                        </use>
                                    </svg>
                                </button>
                                <div class="invalid-feedback">{{ err.password_attuale }}</div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label class="form-label fw-semibold">Nuova password *</label>
                            <div class="input-group">
                                <input v-model="form.nuova_password" :type="showNuova ? 'text' : 'password'"
                                    class="form-control" :class="{ 'is-invalid': err.nuova_password }"
                                    autocomplete="new-password" />
                                <button type="button" class="btn" @click="showNuova = !showNuova" tabindex="-1">
                                    <svg class="icon icon-sm">
                                        <use
                                            :href="`${sprites}#${showNuova ? 'it-password-invisible' : 'it-password-visible'}`">
                                        </use>
                                    </svg>
                                </button>
                                <div class="invalid-feedback">{{ err.nuova_password }}</div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label class="form-label fw-semibold">Conferma nuova password *</label>
                            <div class="input-group">
                                <input v-model="form.conferma_password" :type="showConferma ? 'text' : 'password'"
                                    class="form-control" :class="{ 'is-invalid': err.conferma_password }"
                                    autocomplete="new-password" />
                                <button type="button" class="btn" @click="showConferma = !showConferma" tabindex="-1">
                                    <svg class="icon icon-sm">
                                        <use
                                            :href="`${sprites}#${showConferma ? 'it-password-invisible' : 'it-password-visible'}`">
                                        </use>
                                    </svg>
                                </button>
                                <div class="invalid-feedback">{{ err.conferma_password }}</div>
                            </div>
                        </div>
                        
                    </div>

                    <div class="modal-footer">
                        <button class="btn btn-outline-secondary" @click="chiudi" :disabled="loading">Annulla</button>
                        <button class="btn btn-primary" @click="submit" :disabled="loading">
                            <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                            Salva
                        </button>
                    </div>

                </div>
            </div>
        </div>
    </teleport>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { cambiaPassword } from '@/api/utenti'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'


const props = defineProps({ aperta: Boolean })
const emit = defineEmits(['update:aperta'])

const loading = ref(false)
const esito = ref(null)

const form = reactive({ password_attuale: '', nuova_password: '', conferma_password: '' })
const err = reactive({ password_attuale: '', nuova_password: '', conferma_password: '' })

const showAttuale = ref(false)
const showNuova = ref(false)
const showConferma = ref(false)

watch(() => props.aperta, (val) => {
    if (val) reset()
})

function reset() {
    Object.assign(form, { password_attuale: '', nuova_password: '', conferma_password: '' })
    Object.keys(err).forEach(k => err[k] = '')
    esito.value = null
}

function valida() {
    err.password_attuale = form.password_attuale ? '' : 'Obbligatorio'
    err.nuova_password = form.nuova_password ? '' : 'Obbligatorio'
    if (!err.nuova_password && form.nuova_password.length < 8)
        err.nuova_password = 'Minimo 8 caratteri'
    err.conferma_password = form.conferma_password ? '' : 'Obbligatorio'
    if (!err.conferma_password && form.nuova_password !== form.conferma_password)
        err.conferma_password = 'Le password non coincidono'
    return !Object.values(err).some(Boolean)
}

async function submit() {
    if (!valida()) return
    loading.value = true
    esito.value = null
    try {
        await cambiaPassword({ ...form })
        esito.value = { tipo: 'ok', msg: '✓ Password aggiornata con successo.' }
        setTimeout(chiudi, 1500)
    } catch (e) {
        esito.value = { tipo: 'err', msg: e.message || 'Errore durante il salvataggio.' }
    } finally {
        loading.value = false
    }
}

function chiudi() {
    emit('update:aperta', false)
}
</script>