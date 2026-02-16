"""
Sistema RBAC (Role-Based Access Control).
Definisce quali azioni ogni ruolo può eseguire nel sistema.
"""

from backend.models.enums import RuoloUtente

# ── Matrice dei permessi per ruolo ────────────────────────────────────────────
# Ogni chiave è un'azione del sistema; il valore è la lista di ruoli autorizzati

PERMESSI: dict[str, list[RuoloUtente]] = {

    # ── Prenotazioni ──────────────────────────────────────────────────────────
    "prenotazione:richiedere":    [RuoloUtente.RESPONSABILE_CORSO],
    "prenotazione:validare":      [RuoloUtente.SEGRETERIA_SEDE],
    "prenotazione:inserire":      [RuoloUtente.SEGRETERIA_SEDE],
    "prenotazione:rifiutare":     [RuoloUtente.SEGRETERIA_SEDE],
    "prenotazione:annullare":     [RuoloUtente.RESPONSABILE_CORSO,
                                   RuoloUtente.SEGRETERIA_SEDE],
    "prenotazione:vedere_proprie":[RuoloUtente.RESPONSABILE_CORSO],
    "prenotazione:vedere_sede":   [RuoloUtente.RESPONSABILE_SEDE,
                                   RuoloUtente.SEGRETERIA_SEDE],
    "prenotazione:vedere_corsi":  [RuoloUtente.SEGRETERIA_DIDATTICA],
    "prenotazione:vedere_tutte":  [RuoloUtente.COORDINAMENTO],

    # ── Aule e slot ───────────────────────────────────────────────────────────
    "aula:vedere_slot_liberi":    [RuoloUtente.RESPONSABILE_CORSO,
                                   RuoloUtente.SEGRETERIA_SEDE,
                                   RuoloUtente.RESPONSABILE_SEDE,
                                   RuoloUtente.SEGRETERIA_DIDATTICA,
                                   RuoloUtente.COORDINAMENTO],
    "aula:gestire":               [RuoloUtente.SEGRETERIA_SEDE,
                                   RuoloUtente.COORDINAMENTO],

    # ── Corsi ─────────────────────────────────────────────────────────────────
    "corso:creare":               [RuoloUtente.SEGRETERIA_DIDATTICA,
                                   RuoloUtente.COORDINAMENTO],
    "corso:vedere_propri":        [RuoloUtente.RESPONSABILE_CORSO],
    "corso:vedere_tutti":         [RuoloUtente.SEGRETERIA_DIDATTICA,
                                   RuoloUtente.COORDINAMENTO],

    # ── Report e analytics ────────────────────────────────────────────────────
    "report:sede":                [RuoloUtente.RESPONSABILE_SEDE,
                                   RuoloUtente.COORDINAMENTO],
    "report:globale":             [RuoloUtente.COORDINAMENTO],

    # ── Gestione utenti ───────────────────────────────────────────────────────
    "utente:creare":              [RuoloUtente.COORDINAMENTO],
    "utente:vedere_tutti":        [RuoloUtente.COORDINAMENTO],

    # ── Attrezzature ─────────────────────────────────────────────────────────
    "attrezzatura:richiedere":    [RuoloUtente.RESPONSABILE_CORSO],
    "attrezzatura:gestire":       [RuoloUtente.SEGRETERIA_SEDE,
                                   RuoloUtente.COORDINAMENTO],
}


def ha_permesso(ruolo: RuoloUtente, azione: str) -> bool:
    """
    Verifica se un ruolo è autorizzato a eseguire un'azione.

    Args:
        ruolo:  Ruolo dell'utente autenticato
        azione: Stringa dell'azione da verificare (es: "prenotazione:richiedere")

    Returns:
        True se il ruolo ha il permesso, False altrimenti
    """
    ruoli_autorizzati = PERMESSI.get(azione, [])
    return ruolo in ruoli_autorizzati


def richiedi_permesso(azione: str):
    """
    Decoratore/factory per verificare i permessi negli endpoint FastAPI.
    Da usare come dipendenza insieme a get_utente_corrente.
    """
    def _verifica(ruolo: RuoloUtente) -> bool:
        if not ha_permesso(ruolo, azione):
            return False
        return True
    return _verifica