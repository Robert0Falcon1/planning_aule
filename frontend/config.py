"""
Configurazione del frontend Streamlit.
"""

# URL base del backend FastAPI
API_BASE_URL = "http://localhost:8000/api/v1"

# Timeout delle chiamate HTTP in secondi
REQUEST_TIMEOUT = 10

# Configurazione pagina Streamlit
PAGE_CONFIG = {
    "page_title": "Prenotazione Aule",
    "page_icon": "🏫",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Etichette italiane per i ruoli
RUOLO_LABELS = {
    "responsabile_corso":   "👨‍🏫 Responsabile Corso",
    "responsabile_sede":    "🏢 Responsabile di Sede",
    "segreteria_sede":      "📋 Segreteria di Sede",
    "segreteria_didattica": "📚 Segreteria Didattica",
    "coordinamento":        "🎯 Coordinamento",
}

# Etichette e colori per gli stati delle prenotazioni
STATO_CONFIG = {
    "in_attesa":  {"label": "⏳ In Attesa",  "color": "#FFA500"},
    "confermata": {"label": "✅ Confermata", "color": "#28A745"},
    "rifiutata":  {"label": "❌ Rifiutata",  "color": "#DC3545"},
    "annullata":  {"label": "🚫 Annullata",  "color": "#6C757D"},
    "conflitto":  {"label": "⚠️ Conflitto",  "color": "#FFC107"},
}

# Etichette per i giorni della settimana
GIORNI_SETTIMANA = {
    1: "Lunedì",
    2: "Martedì",
    3: "Mercoledì",
    4: "Giovedì",
    5: "Venerdì",
    6: "Sabato",
    7: "Domenica",
}

# Etichette per i tipi di ricorrenza
RICORRENZA_LABELS = {
    "giornaliera":   "Ogni giorno",
    "settimanale":   "Ogni settimana",
    "bisettimanale": "Ogni due settimane",
    "mensile":       "Ogni mese",
}