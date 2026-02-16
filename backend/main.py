"""
Entry point dell'applicazione FastAPI.
Configura il server, i router e il middleware CORS.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import crea_tabelle

# Import di tutti i router
from backend.routers import auth, utenti, sedi, aule, prenotazioni

# ── Creazione dell'app FastAPI ────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API per la gestione delle prenotazioni aule di InforcoopEcipa",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── Middleware CORS (necessario per Streamlit su porta diversa) ────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Registrazione dei router con prefisso API versioned ───────────────────────
PREFIX = "/api/v1"
app.include_router(auth.router,         prefix=PREFIX)
app.include_router(utenti.router,       prefix=PREFIX)
app.include_router(sedi.router,         prefix=PREFIX)
app.include_router(aule.router,         prefix=PREFIX)
app.include_router(prenotazioni.router, prefix=PREFIX)


# ── Evento di avvio: crea le tabelle se non esistono ─────────────────────────
@app.on_event("startup")
def startup():
    """Inizializza il database all'avvio dell'applicazione."""
    crea_tabelle()
    print(f"✅ {settings.app_name} v{settings.app_version} avviato")
    print(f"📚 Documentazione: http://localhost:8000/api/docs")


@app.get("/", summary="Health check")
def root():
    """Endpoint di verifica dello stato del server."""
    return {
        "app":     settings.app_name,
        "version": settings.app_version,
        "status":  "online"
    }