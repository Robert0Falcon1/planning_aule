"""
Smoke test — ICE Planning Aule
Verifica che tutti gli endpoint toccati dal code review rispondano correttamente.

Requisiti:
    pip install httpx pytest

Utilizzo:
    # Con il server già avviato (uvicorn backend.main:app --reload):
    pytest tests/test_smoke.py -v

    # Con credenziali diverse:
    SMOKE_EMAIL=admin@test.it SMOKE_PASSWORD=secret pytest tests/test_smoke.py -v
"""

import os
import pytest
import httpx

# ─── Configurazione ──────────────────────────────────────────────────────────

BASE_URL  = os.getenv("SMOKE_BASE_URL", "http://localhost:8000/api/v1")
EMAIL     = os.getenv("SMOKE_EMAIL",    "coord@test.it")
PASSWORD  = os.getenv("SMOKE_PASSWORD", "test")
SEDE_ID   = int(os.getenv("SMOKE_SEDE_ID", "1"))
AULA_ID   = int(os.getenv("SMOKE_AULA_ID", "1"))


# ─── Fixture: client autenticato ─────────────────────────────────────────────

@pytest.fixture(scope="session")
def client():
    """Client HTTP con token JWT valido, riutilizzato per tutta la sessione."""
    c = httpx.Client(base_url=BASE_URL, timeout=10)

    r = c.post("/auth/login", data={"username": EMAIL, "password": PASSWORD})
    assert r.status_code == 200, (
        f"Login fallito ({r.status_code}): {r.text}\n"
        f"→ Verifica SMOKE_EMAIL e SMOKE_PASSWORD"
    )
    token = r.json()["access_token"]
    c.headers.update({"Authorization": f"Bearer {token}"})
    yield c
    c.close()


# ─── Helper ──────────────────────────────────────────────────────────────────

def ok(r: httpx.Response, label: str):
    """Asserzione con messaggio leggibile."""
    assert r.status_code in (200, 201), (
        f"[{label}] HTTP {r.status_code}: {r.text[:300]}"
    )
    return r.json()


# ─── Auth ─────────────────────────────────────────────────────────────────────

def test_login_restituisce_token():
    """Il login deve restituire un access_token JWT."""
    r = httpx.post(f"{BASE_URL}/auth/login",
                   data={"username": EMAIL, "password": PASSWORD})
    data = ok(r, "login")
    assert "access_token" in data, "Nessun access_token nella risposta"
    assert data.get("token_type") == "bearer"


def test_login_credenziali_errate():
    """Credenziali sbagliate devono restituire 401, non 500."""
    r = httpx.post(f"{BASE_URL}/auth/login",
                   data={"username": "x@x.it", "password": "sbagliata"})
    assert r.status_code == 401, f"Atteso 401, ottenuto {r.status_code}"


# ─── Aule ────────────────────────────────────────────────────────────────────

def test_get_aule(client):
    """GET /aule/ deve restituire una lista."""
    data = ok(client.get("/aule/"), "GET /aule/")
    assert isinstance(data, list), "Risposta non è una lista"


def test_put_aula_esiste(client):
    """PUT /aule/{id} deve esistere (fix: endpoint aggiunto nella sessione precedente)."""
    r = client.put(f"/aule/{AULA_ID}", json={"note": "smoke test"})
    # 200 ok oppure 403 se OPERATIVO — in entrambi i casi l'endpoint esiste
    assert r.status_code in (200, 403), (
        f"PUT /aule/{AULA_ID} → HTTP {r.status_code}: {r.text[:200]}\n"
        f"→ 404 significa che l'endpoint non è registrato"
    )


# ─── Corsi ───────────────────────────────────────────────────────────────────

def test_get_corsi(client):
    """GET /corsi/ non deve più restituire 404 (router era vuoto)."""
    data = ok(client.get("/corsi/"), "GET /corsi/")
    assert isinstance(data, list), "Risposta non è una lista"


def test_get_corsi_filtro_attivo(client):
    """Filtro ?attivo=true deve funzionare senza errore 422."""
    data = ok(client.get("/corsi/?attivo=true"), "GET /corsi/?attivo=true")
    assert isinstance(data, list)


def test_get_corso_inesistente(client):
    """GET /corsi/99999 deve restituire 404, non 500."""
    r = client.get("/corsi/99999")
    assert r.status_code == 404, f"Atteso 404, ottenuto {r.status_code}: {r.text[:200]}"


# ─── Conflitti ───────────────────────────────────────────────────────────────

def test_get_conflitti_prefix(client):
    """
    GET /conflitti/ deve rispondere (fix: prefix /api/v1 mancante in main.py).
    Prima di questo fix restituiva 404.
    """
    r = client.get("/conflitti/")
    assert r.status_code in (200, 403), (
        f"GET /conflitti/ → HTTP {r.status_code}\n"
        f"→ 404 significa che il prefix non è stato aggiunto in main.py"
    )


def test_get_conflitti_url_diretto_non_risponde():
    """
    /conflitti/ senza /api/v1 NON deve rispondere con 200
    (verifica che il frontend non possa più bypassare il prefix).
    """
    r = httpx.get(f"{BASE_URL.replace('/api/v1', '')}/conflitti/")
    assert r.status_code != 200, (
        "Il vecchio URL /conflitti/ risponde ancora — "
        "il router potrebbe essere registrato due volte"
    )


def test_get_conflitti_stats(client):
    """GET /conflitti/stats/summary deve venire prima di /{id} nel router."""
    r = client.get("/conflitti/stats/summary")
    # 200 se COORDINAMENTO, 403 se OPERATIVO — mai 422 (che indicherebbe
    # che FastAPI ha catturato 'stats' come conflitto_id intero)
    assert r.status_code in (200, 403), (
        f"GET /conflitti/stats/summary → HTTP {r.status_code}: {r.text[:200]}\n"
        f"→ 422 significa che la route /{'{id}'} è registrata PRIMA di /stats/summary"
    )


# ─── Sedi ─────────────────────────────────────────────────────────────────────

def test_get_sedi(client):
    """GET /sedi/ deve restituire una lista."""
    data = ok(client.get("/sedi/"), "GET /sedi/")
    assert isinstance(data, list)


# ─── Prenotazioni ─────────────────────────────────────────────────────────────

def test_get_prenotazioni(client):
    """GET /prenotazioni/ deve restituire una lista."""
    data = ok(client.get("/prenotazioni/"), "GET /prenotazioni/")
    assert isinstance(data, list)


def test_get_prenotazioni_filtro_sede(client):
    """Filtro ?sede_id= deve funzionare senza errore."""
    data = ok(client.get(f"/prenotazioni/?sede_id={SEDE_ID}"), "GET /prenotazioni/?sede_id")
    assert isinstance(data, list)