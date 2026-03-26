import { ref } from 'vue'
import { getConflitti } from '@/api/prenotazioni'

export function useConflittiAlert() {
    const alertConflitti = ref(null)

    /**
     * Verifica se la prenotazione appena creata ha generato conflitti
     * @param {number} prenotazioneId - ID della prenotazione appena creata
     * @param {string} tipo - 'singola' o 'massiva'
     * @returns {Promise<{hasConflitti: boolean, numeroConflitti: number}>}
     */
    async function verificaConflittiNuovaPrenotazione(prenotazioneId, tipo = 'singola') {
        try {
            // Carica tutti i conflitti attivi
            const conflitti = await getConflitti({ solo_attivi: true })
            const listaConflitti = Array.isArray(conflitti) ? conflitti : (conflitti?.items || [])

            // Trova conflitti che coinvolgono questa prenotazione
            const conflittiPrenotazione = listaConflitti.filter(cf =>
                cf.prenotazione_id_1 === prenotazioneId ||
                cf.prenotazione_id_2 === prenotazioneId
            )

            const numeroConflitti = conflittiPrenotazione.length
            const hasConflitti = numeroConflitti > 0

            if (hasConflitti) {
                const msgTipo = tipo === 'massiva' ? 'prenotazioni ricorrenti' : 'prenotazione'
                const conflittoTesto = numeroConflitti > 1
                    ? `sono stati rilevati ${numeroConflitti} conflitti`
                    : 'è stato rilevato 1 conflitto'
                const gestireTesto = numeroConflitti > 1 ? 'gestirli' : 'gestirlo'

                alertConflitti.value = {
                    tipo: 'warning',
                    msg: `Attenzione: la tua ${msgTipo} è stata creata ma ${conflittoTesto} con altre prenotazioni. Vai alla sezione "Mie Prenotazioni" per ${gestireTesto}.`
                }
            }

            return { hasConflitti, numeroConflitti }
        } catch (error) {
            console.warn('Errore verifica conflitti:', error)
            return { hasConflitti: false, numeroConflitti: 0 }
        }
    }

    function resetAlert() {
        alertConflitti.value = null
    }

    return {
        alertConflitti,
        verificaConflittiNuovaPrenotazione,
        resetAlert
    }
}