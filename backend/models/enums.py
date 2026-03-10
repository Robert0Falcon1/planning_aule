"""
Definizione di tutti gli enumerati utilizzati nel sistema.
Centralizzati in un unico file per semplicità di manutenzione.
"""

import enum
from enum import Enum


# ── Utenti e accesso ──────────────────────────────────────────────────────────

class RuoloUtente(str, Enum):
    OPERATIVO = "OPERATIVO"
    COORDINAMENTO = "COORDINAMENTO"


# ── Prenotazioni ──────────────────────────────────────────────────────────────

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
    PC          = "pc"
    PROIETTORE  = "proiettore"
    LAVAGNA     = "lavagna"
    CASSE_AUDIO = "casse audio"
    MICROFONO   = "microfono"
    WEBCAM      = "webcam"


class TipoConflitto(str, Enum):
    """Tipologie di conflitto rilevabili nel sistema."""
    OVERLAP_ORARIO          = "OVERLAP_ORARIO"
    DOPPIA_PRENOTAZIONE     = "DOPPIA_PRENOTAZIONE"
    ALTRO                   = "ALTRO"


class StatoRisoluzioneConflitto(str, Enum):
    """Stato risoluzione conflitto"""
    NON_RISOLTO                  = "NON_RISOLTO"
    RISOLTO_MANTENUTA_1          = "RISOLTO_MANTENUTA_1"
    RISOLTO_MANTENUTA_2          = "RISOLTO_MANTENUTA_2"
    RISOLTO_ELIMINATE_ENTRAMBE   = "RISOLTO_ELIMINATE_ENTRAMBE"
    RISOLTO_MANUALE              = "RISOLTO_MANUALE"


# ── Corsi ─────────────────────────────────────────────────────────────────────

class TipoFinanziamento(str, enum.Enum):
    """Modalità di finanziamento dei corsi."""
    FINANZIATO_PUBBLICO = "finanziato_pubblico"
    A_PAGAMENTO         = "a_pagamento"
    MISTO               = "misto"


class StatoCorso(str, enum.Enum):
    """
    Stati del ciclo di vita di un corso su Sistema Piemonte.
    Il valore stringa corrisponde al codice numerico del sistema regionale.
    """
    APPROVATO    = "15"
    AVVIATO      = "22"
    IN_CORSO     = "30"
    CONCLUSO     = "35"
    RENDICONTATO = "40"
    SALDATO      = "60"
    RINUNCIA     = "rinuncia"


class OreAccertamento(str, enum.Enum):
    """
    Tipologie di prova di accertamento per allievi stranieri.
    Ogni prova ha durata fissa di 40 minuti su Sistema Piemonte.
    """
    ITALIANO   = "italiano"
    MATEMATICA = "matematica"
    INGLESE    = "inglese"


# ── Lezioni ───────────────────────────────────────────────────────────────────

class TipoLezione(str, enum.Enum):
    """Tipologie di lezione registrabili su Sistema Piemonte."""
    NORMALE                           = "normale"
    RECUPERO_SOLO_DIDATTICO           = "recupero_solo_didattico"
    RECUPERO_AMMINISTRATIVO_DIDATTICO = "recupero_amministrativo_e_didattico"
    FAD                               = "fad"


# ── Docenti ───────────────────────────────────────────────────────────────────

class TipologiaDocente(str, enum.Enum):
    """
    Tipologia di attività svolta dal docente nel corso.
    T = Teoria · P = Pratica · S = Stage
    """
    T = "T"
    P = "P"
    S = "S"


# ── Allievi ───────────────────────────────────────────────────────────────────

class Sesso(str, enum.Enum):
    M = "M"
    F = "F"
    A = "A"   # Non specificato / altro


class Cittadinanza(str, enum.Enum):
    COMUNITARIA       = "comunitaria"
    EXTRA_COMUNITARIA = "extra_comunitaria"


class ResidenzaIn(str, enum.Enum):
    ITALIA = "italia"
    ESTERO = "estero"


class LivelloIstruzione(str, enum.Enum):
    NESSUN_TITOLO             = "nessun_titolo"
    LICENZA_ELEMENTARE        = "licenza_elementare"
    LICENZA_MEDIA             = "licenza_media"
    QUALIFICA_PROFESSIONALE   = "qualifica_professionale"
    DIPLOMA_SUPERIORE         = "diploma_superiore"
    DIPLOMA_TECNICO_SUPERIORE = "diploma_tecnico_superiore"
    LAUREA_TRIENNALE          = "laurea_triennale"
    LAUREA_MAGISTRALE         = "laurea_magistrale"
    DOTTORATO                 = "dottorato"


class CondizioneOccupazionale(str, enum.Enum):
    DISOCCUPATO         = "disoccupato"
    INOCCUPATO          = "inoccupato"
    OCCUPATO_DIPENDENTE = "occupato_dipendente"
    OCCUPATO_AUTONOMO   = "occupato_autonomo"
    OCCUPATO_CIGO       = "occupato_cigo"
    OCCUPATO_CIGS       = "occupato_cigs"
    STUDENTE            = "studente"


class DisabilitaVulnerabilita(str, enum.Enum):
    NESSUNA              = "nessuna"
    DSA                  = "dsa"
    DISABILITA           = "disabilita"
    EES                  = "ees"
    SVANTAGGIO_CULTURALE = "svantaggio_culturale"


class SvantaggioAbitativo(str, enum.Enum):
    """1 = in condizione di svantaggio · 2 = nessuna condizione."""
    SVANTAGGIO = "1"
    NESSUNA    = "2"