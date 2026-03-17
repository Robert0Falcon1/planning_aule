"""
Test suite completa — ICE Planning Aule
Copre tutti gli endpoint dello Swagger.

Utilizzo:
    pytest tests/test_api_completo.py -v
"""

import os
import pytest
import httpx
from datetime import date, timedelta

BASE_URL    = os.getenv("SMOKE_BASE_URL",    "http://localhost:8000/api/v1")
EMAIL_COORD = os.getenv("SMOKE_EMAIL",       "dev@inforcoopecipa.it")
EMAIL_OP    = os.getenv("SMOKE_EMAIL_OP",    "colline@inforcoopecipa.it")
PASSWORD    = os.getenv("SMOKE_PASSWORD",    "final")
PASSWORD_OP = os.getenv("SMOOTH_PASSWORD_OP", os.getenv("SMOKE_PASSWORD_OP", PASSWORD))
AULA_ID_A   = int(os.getenv("TEST_AULA_A",  "1"))
AULA_ID_B   = int(os.getenv("TEST_AULA_B",  "2"))
CORSO_ID    = int(os.getenv("TEST_CORSO_ID", "1"))
SEDE_ID     = int(os.getenv("TEST_SEDE_ID",  "1"))

DOMANI = (date.today() + timedelta(days=1)).isoformat()
TRA_7  = (date.today() + timedelta(days=7)).isoformat()
TRA_14 = (date.today() + timedelta(days=14)).isoformat()


# ─── Fixtures ────────────────────────────────────────────────────────────────

def _login(email, password):
    c = httpx.Client(base_url=BASE_URL, timeout=15)
    r = c.post("/auth/login", data={"username": email, "password": password})
    assert r.status_code == 200, f"Login fallito per {email}: {r.text}"
    c.headers.update({"Authorization": f"Bearer {r.json()['access_token']}"})
    return c

@pytest.fixture(scope="session")
def coord():
    c = _login(EMAIL_COORD, PASSWORD)
    yield c
    c.close()

@pytest.fixture(scope="session")
def operativo():
    c = _login(EMAIL_OP, PASSWORD_OP)
    yield c
    c.close()

def ok(r, label):
    assert r.status_code in (200, 201), f"[{label}] HTTP {r.status_code}: {r.text[:400]}"
    return r.json()


# ─── Auth ─────────────────────────────────────────────────────────────────────

class TestAuth:
    def test_me_coord(self, coord):
        data = ok(coord.get("/auth/me"), "GET /auth/me coord")
        assert "email" in data
        assert data["ruolo"].lower() == "coordinamento"

    def test_me_operativo(self, operativo):
        data = ok(operativo.get("/auth/me"), "GET /auth/me operativo")
        assert data["ruolo"].lower() == "operativo"


# ─── Utenti ───────────────────────────────────────────────────────────────────

class TestUtenti:
    def test_lista_utenti_coord(self, coord):
        data = ok(coord.get("/utenti/"), "GET /utenti/ coord")
        assert isinstance(data, list)
        assert len(data) > 0

    def test_lista_utenti_operativo_403(self, operativo):
        r = operativo.get("/utenti/")
        assert r.status_code == 403

    def test_crea_modifica_disattiva_riattiva_utente(self, coord):
        # Crea
        r = coord.post("/utenti/", json={
            "nome":     "Test",
            "cognome":  "Automatico",
            "email":    "test.automatico.suite@test.it",
            "password": "password123",
            "ruolo":    "OPERATIVO",
            "sede_id":  SEDE_ID,
        })
        # Potrebbe già esistere da run precedente
        if r.status_code == 409:
            pytest.skip("Utente test già esistente nel DB")
        data = ok(r, "POST /utenti/")
        uid = data["id"]
        assert data["email"] == "test.automatico.suite@test.it"
        assert data["attivo"] == True

        # Modifica
        r2 = coord.patch(f"/utenti/{uid}", json={"nome": "TestModificato"})
        data2 = ok(r2, f"PATCH /utenti/{uid}")
        assert data2["nome"] == "TestModificato"

        # Disattiva
        r3 = coord.delete(f"/utenti/{uid}")
        assert r3.status_code == 200
        assert "disattivato" in r3.json().get("detail", "").lower()

        # Riattiva
        r4 = coord.patch(f"/utenti/{uid}/riattiva")
        assert r4.status_code == 200
        assert "riattivato" in r4.json().get("detail", "").lower()

        # Cleanup — disattiva di nuovo
        coord.delete(f"/utenti/{uid}")

    def test_cambio_password_operativo(self, operativo):
        """L'operativo può cambiare la propria password."""
        r = operativo.patch("/utenti/me/password", json={
            "password_attuale":  "colline!",
            "nuova_password":    "colline!",   # stessa password — test di round-trip
            "conferma_password": "colline!",
        })
        assert r.status_code == 200

    def test_cambio_password_errata_400(self, operativo):
        r = operativo.patch("/utenti/me/password", json={
            "password_attuale":  "passwordsbagliata",
            "nuova_password":    "nuova123",
            "conferma_password": "nuova123",
        })
        assert r.status_code == 400

    def test_cambio_password_conferma_diversa_400(self, operativo):
        r = operativo.patch("/utenti/me/password", json={
            "password_attuale":  "colline!",
            "nuova_password":    "nuova123",
            "conferma_password": "diversa456",
        })
        assert r.status_code == 400

    def test_operativo_non_puo_creare_utenti(self, operativo):
        r = operativo.post("/utenti/", json={
            "nome": "X", "cognome": "Y",
            "email": "x@y.it", "password": "pass123",
            "ruolo": "OPERATIVO", "sede_id": SEDE_ID,
        })
        assert r.status_code == 403


# ─── Sedi ─────────────────────────────────────────────────────────────────────

class TestSedi:
    def test_lista_sedi(self, coord):
        data = ok(coord.get("/sedi/"), "GET /sedi/")
        assert isinstance(data, list)
        assert len(data) > 0

    def test_dettaglio_sede(self, coord):
        data = ok(coord.get(f"/sedi/{SEDE_ID}"), f"GET /sedi/{SEDE_ID}")
        assert data["id"] == SEDE_ID

    def test_sede_inesistente_404(self, coord):
        r = coord.get("/sedi/99999")
        assert r.status_code == 404

    def test_crea_modifica_sede(self, coord):
        r = coord.post("/sedi/", json={
            "nome":    "Sede Test Automatico",
            "citta":   "Torino",
            "indirizzo": "Via Test 1",
        })
        if r.status_code == 409:
            pytest.skip("Sede test già esistente")
        data = ok(r, "POST /sedi/")
        sid = data["id"]
        assert data["nome"] == "Sede Test Automatico"

        # Modifica
        r2 = coord.patch(f"/sedi/{sid}", json={"nome": "Sede Test Modificata"})
        data2 = ok(r2, f"PATCH /sedi/{sid}")
        assert data2["nome"] == "Sede Test Modificata"

        # Cleanup — non c'è DELETE sedi, lasciamo la sede nel DB
        # (sede inattiva se possibile, altrimenti la lasciamo)

    def test_lista_sedi_operativo(self, operativo):
        """Le sedi sono visibili a tutti."""
        data = ok(operativo.get("/sedi/"), "GET /sedi/ operativo")
        assert isinstance(data, list)


# ─── Aule ─────────────────────────────────────────────────────────────────────

class TestAule:
    def test_lista_aule(self, coord):
        data = ok(coord.get("/aule/"), "GET /aule/")
        assert isinstance(data, list)
        assert len(data) > 0

    def test_lista_aule_filtro_sede(self, coord):
        data = ok(coord.get(f"/aule/?sede_id={SEDE_ID}"), "GET /aule/?sede_id")
        assert isinstance(data, list)
        assert all(a["sede_id"] == SEDE_ID for a in data)

    def test_crea_aggiorna_aula(self, coord):
        r = coord.post("/aule/", json={
            "nome":     "Aula Test Automatico",
            "capienza": 10,
            "sede_id":  SEDE_ID,
        })
        data = ok(r, "POST /aule/")
        aid = data["id"]
        assert data["nome"] == "Aula Test Automatico"

        # Aggiorna
        r2 = coord.put(f"/aule/{aid}", json={
            "nome":     "Aula Test Modificata",
            "capienza": 15,
            "sede_id":  SEDE_ID,
        })
        data2 = ok(r2, f"PUT /aule/{aid}")
        assert data2["nome"] == "Aula Test Modificata"
        assert data2["capienza"] == 15

    def test_aula_operativo_visibile(self, operativo):
        data = ok(operativo.get("/aule/"), "GET /aule/ operativo")
        assert isinstance(data, list)


# ─── Slot liberi ──────────────────────────────────────────────────────────────

class TestSlotLiberi:
    def test_slot_liberi_aula(self, coord):
        r = coord.get(f"/prenotazioni/slot-liberi/{AULA_ID_A}",
                      params={"data_dal": DOMANI, "data_al": TRA_7})
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

    def test_slot_liberi_aula_inesistente(self, coord):
        r = coord.get("/prenotazioni/slot-liberi/99999",
                      params={"data_dal": DOMANI, "data_al": TRA_7})
        # 200 con lista vuota o 404 — entrambi accettabili
        assert r.status_code in (200, 404)


# ─── Prenotazioni — filtri avanzati ───────────────────────────────────────────

class TestPrenotazioniFiltri:
    def test_filtro_stato(self, coord):
        data = ok(coord.get("/prenotazioni/?stato=confermata"), "filtro stato")
        assert isinstance(data, list)

    def test_filtro_corso(self, coord):
        data = ok(coord.get(f"/prenotazioni/?corso_id={CORSO_ID}"), "filtro corso")
        assert isinstance(data, list)

    def test_filtro_combinato(self, coord):
        data = ok(coord.get(
            f"/prenotazioni/?sede_id={SEDE_ID}&data_dal={DOMANI}&data_al={TRA_14}"
        ), "filtro combinato")
        assert isinstance(data, list)

    def test_dettaglio_prenotazione(self, coord):
        # Crea una prenotazione e verifica il dettaglio
        r = coord.post("/prenotazioni/singola", json={
            "aula_id":  AULA_ID_A,
            "corso_id": CORSO_ID,
            "slot": {"data": TRA_14, "ora_inizio": "10:00", "ora_fine": "12:00"},
        })
        pren_id = ok(r, "crea per dettaglio")["id"]

        data = ok(coord.get(f"/prenotazioni/{pren_id}"), "GET /prenotazioni/{id}")
        assert data["id"] == pren_id
        assert len(data["slots"]) == 1

        coord.delete(f"/prenotazioni/{pren_id}")


# ─── Conflitti — copertura completa ───────────────────────────────────────────

class TestConflittiCompleto:
    def test_lista_conflitti(self, coord):
        data = ok(coord.get("/conflitti/"), "GET /conflitti/")
        assert isinstance(data, list)

    def test_lista_conflitti_solo_attivi(self, coord):
        data = ok(coord.get("/conflitti/?solo_attivi=true"), "GET /conflitti/ solo_attivi")
        assert isinstance(data, list)
        assert all(c["stato_risoluzione"] is None for c in data)

    def test_lista_conflitti_tutti(self, coord):
        data = ok(coord.get("/conflitti/?solo_attivi=false"), "GET /conflitti/ tutti")
        assert isinstance(data, list)

    def test_statistiche_conflitti(self, coord):
        data = ok(coord.get("/conflitti/stats/summary"), "GET /conflitti/stats/summary")
        assert "totali" in data
        assert "attivi" in data
        assert "risolti" in data
        assert "percentuale_risolti" in data

    def test_statistiche_conflitti_filtro_sede(self, coord):
        data = ok(coord.get(f"/conflitti/stats/summary?sede_id={SEDE_ID}"),
                  "GET /conflitti/stats/summary?sede_id")
        assert "totali" in data

    def test_statistiche_operativo_403(self, operativo):
        r = operativo.get("/conflitti/stats/summary")
        assert r.status_code == 403

    def test_conflitto_inesistente_404(self, coord):
        r = coord.get("/conflitti/99999999")
        assert r.status_code in (403, 404)

    def test_tutti_i_tipi_risoluzione(self, coord):
        """Testa mantieni_1, mantieni_2, elimina_entrambe."""
        for azione, ora_a, ora_b in [
            ("mantieni_1",       "08:00", "10:00"),
            ("mantieni_2",       "09:00", "11:00"),
            ("elimina_entrambe", "10:00", "12:00"),
        ]:
            data_test = (date.today() + timedelta(days=20)).isoformat()
            r1 = coord.post("/prenotazioni/singola", json={
                "aula_id": AULA_ID_A, "corso_id": CORSO_ID,
                "slot": {"data": data_test, "ora_inizio": ora_a,
                         "ora_fine": str(int(ora_a[:2]) + 3).zfill(2) + ":00"},
            })
            r2 = coord.post("/prenotazioni/singola", json={
                "aula_id": AULA_ID_A, "corso_id": CORSO_ID,
                "slot": {"data": data_test, "ora_inizio": ora_b,
                         "ora_fine": str(int(ora_b[:2]) + 3).zfill(2) + ":00"},
            })
            p1 = ok(r1, f"crea p1 {azione}")
            p2 = ok(r2, f"crea p2 {azione}")
            pren_ids = {p1["id"], p2["id"]}

            conflitti = ok(coord.get("/conflitti/?solo_attivi=true"), "conflitti")
            cf = next((c for c in conflitti
                       if c["prenotazione_id_1"] in pren_ids
                       or c["prenotazione_id_2"] in pren_ids), None)

            if cf:
                r_risolvi = coord.post(f"/conflitti/{cf['id']}/risolvi?azione={azione}")
                assert r_risolvi.status_code == 200, \
                    f"Risoluzione {azione} fallita: {r_risolvi.text}"

            # Cleanup
            for pid in pren_ids:
                coord.delete(f"/prenotazioni/{pid}")


# ─── Corsi ────────────────────────────────────────────────────────────────────

class TestCorsi:
    def test_lista_corsi(self, coord):
        data = ok(coord.get("/corsi/"), "GET /corsi/")
        assert isinstance(data, list)

    def test_lista_corsi_filtro_attivo(self, coord):
        data = ok(coord.get("/corsi/?attivo=true"), "GET /corsi/?attivo=true")
        assert isinstance(data, list)

    def test_dettaglio_corso(self, coord):
        data = ok(coord.get(f"/corsi/{CORSO_ID}"), f"GET /corsi/{CORSO_ID}")
        assert data["id"] == CORSO_ID

    def test_corso_inesistente_404(self, coord):
        r = coord.get("/corsi/99999999")
        assert r.status_code == 404

    def test_corsi_visibili_operativo(self, operativo):
        data = ok(operativo.get("/corsi/"), "GET /corsi/ operativo")
        assert isinstance(data, list)


# ─── Health check ─────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_check(self):
        r = httpx.get("http://localhost:8000/")
        assert r.status_code == 200