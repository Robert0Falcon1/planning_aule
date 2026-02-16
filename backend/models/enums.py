"""
Definizione di tutti gli enumerati utilizzati nel sistema.
Centralizzati in un unico file per semplicità di manutenzione.
"""

import enum


class RuoloUtente(str, enum.Enum):
    """Ruoli disponibili nel sistema con permessi differenziati."""
    RESPONSABILE_CORSO    = "responsabile_corso"
    RESPONSABILE_SEDE     = "responsabile_sede"
    SEGRETERIA_SEDE       = "segreteria_sede"
    SEGRETERIA_DIDATTICA  = "segreteria_didattica"
    COORDINAMENTO         = "coordinamento"


class StatoPrenotazione(str, enum.Enum):
    """Ciclo di vita di una prenotazione."""
    IN_ATTESA  = "in_attesa"
    CONFERMATA = "confermata"
    RIFIUTATA  = "rifiutata"
    ANNULLATA  = "annullata"
    CONFLITTO  = "conflitto"


class StatoRichiesta(str, enum.Enum):
    """Stato del processo di validazione di una richiesta."""
    INVIATA      = "inviata"
    IN_REVISIONE = "in_revisione"
    APPROVATA    = "approvata"
    RIFIUTATA    = "rifiutata"


class TipoPrenotazione(str, enum.Enum):
    """Distingue prenotazioni singole da quelle ricorrenti."""
    SINGOLA  = "singola"
    MASSIVA  = "massiva"


class TipoRicorrenza(str, enum.Enum):
    """Pattern di ricorrenza per le prenotazioni massive."""
    GIORNALIERA   = "giornaliera"
    SETTIMANALE   = "settimanale"
    BISETTIMANALE = "bisettimanale"
    MENSILE       = "mensile"


class TipoAttrezzatura(str, enum.Enum):
    """Categorie di attrezzatura richiedibile."""
    PC               = "pc"
    PROIETTORE       = "proiettore"
    LAVAGNA_DIGITALE = "lavagna_digitale"
    MICROFONO        = "microfono"
    WEBCAM           = "webcam"
    STAMPANTE        = "stampante"


class TipoFinanziamento(str, enum.Enum):
    """Modalità di finanziamento dei corsi."""
    FINANZIATO_PUBBLICO = "finanziato_pubblico"
    A_PAGAMENTO         = "a_pagamento"
    MISTO               = "misto"


class TipoConflitto(str, enum.Enum):
    """Tipologie di conflitto rilevabili nel sistema."""
    SOVRAPPOSIZIONE_SLOT         = "sovrapposizione_slot"
    CAPIENZA_SUPERATA            = "capienza_superata"
    ATTREZZATURA_INDISPONIBILE   = "attrezzatura_indisponibile"