"""
Entry point dell'applicazione FastAPI.
Configura il server, i router e il middleware CORS.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import crea_tabelle

# Import di tutti i router
from backend.routers import auth, utenti, sedi, aule, prenotazioni, conflitti, corsi


# ── Lifespan (sostituisce il deprecato @app.on_event) ────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inizializza il database all'avvio dell'applicazione."""
    crea_tabelle()
    print(f"✅ {settings.app_name} v{settings.app_version} avviato")
    print(f"📚 Documentazione: http://localhost:8000/api/docs")
    yield
    # Cleanup all'arresto (se necessario in futuro)


# ── Creazione dell'app FastAPI ────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API per la gestione delle prenotazioni aule di InforcoopEcipa",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# ── Middleware CORS ───────────────────────────────────────────────────────────
# FIX: rimosso placeholder '192.168.1.YY' non valido.
# Aggiungere qui l'IP LAN reale del frontend (es. http://192.168.1.42:5173)
# oppure caricarlo da variabile d'ambiente in settings.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://192\.168\.1\.\d+:(5173|8501)",  # tutta la LAN
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://10.0.220.184:5173", # Indirizzo IP della rete WiFi da aggiungere
        "http://10.0.5.206:5173",
        *([settings.frontend_origin] if getattr(settings, "frontend_origin", None) else []),
    ],
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
app.include_router(conflitti.router,    prefix=PREFIX)
app.include_router(corsi.router,        prefix=PREFIX)


@app.get("/", summary="Health check")
def root():
    """Endpoint di verifica dello stato del server."""
    return {
        "app":     settings.app_name,
        "version": settings.app_version,
        "status":  "online"
    }