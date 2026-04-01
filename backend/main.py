"""
Entry point dell'applicazione FastAPI.
Configura il server, i router e il middleware CORS.
"""
from contextlib import asynccontextmanager
from datetime import datetime, timezone
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
# Carica origini dalla variabile d'ambiente CORS_ORIGINS
cors_origins = []
if hasattr(settings, 'cors_origins') and settings.cors_origins:
    cors_origins = [o.strip() for o in settings.cors_origins.split(',') if o.strip()]
# Fallback per sviluppo locale
if not cors_origins:
    cors_origins = [
        "http://localhost:5173",
        "http://localhost",
        "http://127.0.0.1:5173",
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
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

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint per Docker healthcheck.
    Ritorna 200 OK se il servizio è attivo e funzionante.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }