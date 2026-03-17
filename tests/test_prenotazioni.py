"""
Test suite — ICE Planning Aule
Copre i flussi critici: creazione, conflitti, modifica slot, annullamento.

Utilizzo:
    pytest tests/test_prenotazioni.py -v

Requisiti: server uvicorn attivo su localhost:8000
"""

import os
import pytest
import httpx
from datetime import date, timedelta

BASE_URL  = os.getenv("SMOKE_BASE_URL", "http://localhost:8000/api/v1")
EMAIL_COORD = os.getenv("SMOKE_EMAIL",    "coord@test.it")
EMAIL_OP       = os.getenv("SMOKE_EMAIL_OP",       "op@test.it")
PASSWORD       = os.getenv("SMOKE_PASSWORD",       "test")
PASSWORD_OP    = os.getenv("SMOKE_PASSWORD_OP",    PASSWORD)

# Aula e sede esistenti nel DB di test — aggiusta se necessario
AULA_ID_A = int(os.getenv("TEST_AULA_A", "1"))
AULA_ID_B = int(os.getenv("TEST_AULA_B", "2"))
CORSO_ID  = int(os.getenv("TEST_CORSO_ID", "1"))

DOMANI = (date.today() + timedelta(days=1)).isoformat()
TRA_2  = (date.today() + timedelta(days=2)).isoformat()
TRA_3  = (date.today() + timedelta(days=3)).isoformat()
TRA_7  = (date.today() + timedelta(days=7)).isoformat()
TRA_14 = (date.today() + timedelta(days=14)).isoformat()


# ─── Fixtures ────────────────────────────────────────────────────────────────

def _login(email: str, password: str) -> httpx.Client:
    c = httpx.Client(base_url=BASE_URL, timeout=10)
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


def ok(r: httpx.Response, label: str):
    assert r.status_code in (200, 201), f"[{label}] HTTP {r.status_code}: {r.text[:400]}"
    return r.json()


def crea_singola(client, aula_id, data, ora_inizio="08:00", ora_fine="13:00", note=""):
    return client.post("/prenotazioni/singola", json={
        "aula_id":  aula_id,
        "corso_id": CORSO_ID,
        "slot": {
            "data":       data,
            "ora_inizio": ora_inizio,
            "ora_fine":   ora_fine,
        },
        "note": note or None,
    })


def crea_massiva(client, aula_id, data_inizio, data_fine,
                 ora_inizio="08:00", ora_fine="13:00",
                 tipo="settimanale", giorni=None):
    return client.post("/prenotazioni/massiva", json={
        "aula_id":          aula_id,
        "corso_id":         CORSO_ID,
        "data_inizio":      data_inizio,
        "data_fine":        data_fine,
        "ora_inizio":       ora_inizio,
        "ora_fine":         ora_fine,
        "tipo_ricorrenza":  tipo,
        "giorni_settimana": giorni or [1, 2, 3, 4, 5],
    })


# ─── Auth ─────────────────────────────────────────────────────────────────────

class TestAuth:
    def test_login_valido(self):
        r = httpx.post(f"{BASE_URL}/auth/login",
                       data={"username": EMAIL_COORD, "password": PASSWORD})
        data = ok(r, "login")
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_errato_401(self):
        r = httpx.post(f"{BASE_URL}/auth/login",
                       data={"username": "x@x.it", "password": "sbagliata"})
        assert r.status_code == 401

    def test_endpoint_protetto_senza_token_401(self):
        r = httpx.get(f"{BASE_URL}/prenotazioni/")
        assert r.status_code == 401


# ─── Prenotazione singola ─────────────────────────────────────────────────────

class TestPrenotazioneSingola:
    def test_crea_singola_201(self, coord):
        r = crea_singola(coord, AULA_ID_A, DOMANI, note="Test singola")
        data = ok(r, "crea singola")
        assert data["tipo"].lower() == "singola"
        assert len(data["slots"]) == 1
        assert data["slots"][0]["aula_id"] == AULA_ID_A
        assert data["slots"][0]["corso_id"] == CORSO_ID
        # Cleanup
        coord.delete(f"/prenotazioni/{data['id']}")

    def test_crea_singola_campi_slot(self, coord):
        r = crea_singola(coord, AULA_ID_A, TRA_2, "09:00", "12:00", note="Nota test")
        data = ok(r, "crea singola campi")
        slot = data["slots"][0]
        assert slot["note"] == "Nota test"
        assert slot["ora_inizio"].startswith("09:00")
        assert slot["ora_fine"].startswith("12:00")
        coord.delete(f"/prenotazioni/{data['id']}")

    def test_crea_singola_payload_errato_422(self, coord):
        r = coord.post("/prenotazioni/singola", json={"aula_id": AULA_ID_A})
        assert r.status_code == 422

    def test_elimina_prenotazione(self, coord):
        r = crea_singola(coord, AULA_ID_A, TRA_3)
        pren_id = ok(r, "crea per elimina")["id"]
        r_del = coord.delete(f"/prenotazioni/{pren_id}")
        assert r_del.status_code == 200
        # Verifica che non esista più
        r_get = coord.get(f"/prenotazioni/{pren_id}")
        assert r_get.status_code == 404


# ─── Prenotazione massiva ─────────────────────────────────────────────────────

class TestPrenotazioneMassiva:
    def test_crea_massiva_201(self, coord):
        r = crea_massiva(coord, AULA_ID_A, DOMANI, TRA_7)
        data = ok(r, "crea massiva")
        assert data["tipo"].lower() == "massiva"
        assert len(data["slots"]) >= 1
        assert data["slots"][0]["aula_id"] == AULA_ID_A
        coord.delete(f"/prenotazioni/{data['id']}")

    def test_crea_massiva_giornaliera(self, coord):
        r = crea_massiva(coord, AULA_ID_A, DOMANI, TRA_3,
                        tipo="giornaliera", giorni=[1,2,3,4,5])
        data = ok(r, "crea massiva giornaliera")
        assert len(data["slots"]) >= 2
        coord.delete(f"/prenotazioni/{data['id']}")

    def test_annulla_slot_singolo(self, coord):
        r = crea_massiva(coord, AULA_ID_A, DOMANI, TRA_7)
        data = ok(r, "crea per annulla slot")
        pren_id = data["id"]
        slot_id = data["slots"][0]["id"]

        r_del = coord.delete(f"/prenotazioni/{pren_id}/slots/{slot_id}")
        assert r_del.status_code == 200
        assert r_del.json()["prenotazione_eliminata"] == False

        # Verifica che lo slot risulti annullato
        r_get = coord.get(f"/prenotazioni/{pren_id}")
        pren = r_get.json()
        slot_annullato = next(s for s in pren["slots"] if s["id"] == slot_id)
        assert slot_annullato["annullato"] == True
        coord.delete(f"/prenotazioni/{pren_id}")

    def test_annulla_ultimo_slot_elimina_prenotazione(self, coord):
        """Se annullo l'unico slot attivo, la prenotazione viene eliminata."""
        r = crea_singola(coord, AULA_ID_A, DOMANI)
        data = ok(r, "crea singola per annulla")
        pren_id = data["id"]
        slot_id = data["slots"][0]["id"]

        r_del = coord.delete(f"/prenotazioni/{pren_id}/slots/{slot_id}")
        assert r_del.status_code == 200
        assert r_del.json()["prenotazione_eliminata"] == True

        r_get = coord.get(f"/prenotazioni/{pren_id}")
        assert r_get.status_code == 404


# ─── Modifica slot ────────────────────────────────────────────────────────────

class TestModificaSlot:
    def test_modifica_orario(self, coord):
        r = crea_singola(coord, AULA_ID_A, DOMANI, "08:00", "13:00")
        data = ok(r, "crea per modifica")
        pren_id = data["id"]
        slot_id = data["slots"][0]["id"]

        r_patch = coord.patch(f"/prenotazioni/{pren_id}/slots/{slot_id}", json={
            "ora_inizio": "14:00",
            "ora_fine":   "18:00",
        })
        patched = ok(r_patch, "modifica orario")
        slot = patched["slots"][0]
        assert slot["ora_inizio"].startswith("14:00")
        assert slot["ora_fine"].startswith("18:00")
        coord.delete(f"/prenotazioni/{pren_id}")

    def test_modifica_aula(self, coord):
        r = crea_singola(coord, AULA_ID_A, TRA_2)
        data = ok(r, "crea per modifica aula")
        pren_id = data["id"]
        slot_id = data["slots"][0]["id"]

        r_patch = coord.patch(f"/prenotazioni/{pren_id}/slots/{slot_id}", json={
            "aula_id": AULA_ID_B,
        })
        patched = ok(r_patch, "modifica aula")
        assert patched["slots"][0]["aula_id"] == AULA_ID_B
        coord.delete(f"/prenotazioni/{pren_id}")

    def test_modifica_note(self, coord):
        r = crea_singola(coord, AULA_ID_A, TRA_3)
        data = ok(r, "crea per modifica note")
        pren_id = data["id"]
        slot_id = data["slots"][0]["id"]

        r_patch = coord.patch(f"/prenotazioni/{pren_id}/slots/{slot_id}", json={
            "note": "Nota aggiornata",
        })
        patched = ok(r_patch, "modifica note")
        assert patched["slots"][0]["note"] == "Nota aggiornata"
        coord.delete(f"/prenotazioni/{pren_id}")

    def test_modifica_slot_annullato_400(self, coord):
        r = crea_singola(coord, AULA_ID_A, DOMANI)
        data = ok(r, "crea per modifica annullato")
        pren_id = data["id"]
        slot_id = data["slots"][0]["id"]

        coord.delete(f"/prenotazioni/{pren_id}/slots/{slot_id}")
        r_patch = coord.patch(f"/prenotazioni/{pren_id}/slots/{slot_id}", json={
            "ora_inizio": "10:00",
        })
        assert r_patch.status_code in (400, 404)


# ─── Conflitti ────────────────────────────────────────────────────────────────

class TestConflitti:
    def test_crea_conflitto(self, coord):
        """Due prenotazioni sulla stessa aula nello stesso orario generano un conflitto."""
        r1 = crea_singola(coord, AULA_ID_A, DOMANI, "08:00", "13:00")
        r2 = crea_singola(coord, AULA_ID_A, DOMANI, "10:00", "15:00")
        p1 = ok(r1, "crea p1 conflitto")
        p2 = ok(r2, "crea p2 conflitto")

        r_cf = coord.get("/conflitti/?solo_attivi=true")
        conflitti = ok(r_cf, "get conflitti")
        pren_ids = {p1["id"], p2["id"]}
        conflitto = next(
            (c for c in conflitti
             if c["prenotazione_id_1"] in pren_ids or c["prenotazione_id_2"] in pren_ids),
            None
        )
        assert conflitto is not None, "Conflitto non rilevato"
        assert conflitto["stato_risoluzione"] is None

        # Cleanup
        coord.delete(f"/prenotazioni/{p1['id']}")
        coord.delete(f"/prenotazioni/{p2['id']}")

    def test_modifica_slot_chiude_conflitto(self, coord):
        """Dopo modifica dello slot in orario diverso, il conflitto deve chiudersi."""
        r1 = crea_singola(coord, AULA_ID_A, TRA_2, "08:00", "13:00")
        r2 = crea_singola(coord, AULA_ID_A, TRA_2, "10:00", "15:00")
        p1 = ok(r1, "crea p1 mod")
        p2 = ok(r2, "crea p2 mod")

        # Sposta p2 su orario non sovrapposto
        slot_id = p2["slots"][0]["id"]
        coord.patch(f"/prenotazioni/{p2['id']}/slots/{slot_id}", json={
            "ora_inizio": "16:00",
            "ora_fine":   "19:00",
        })

        r_cf = coord.get("/conflitti/?solo_attivi=true")
        conflitti_attivi = ok(r_cf, "get conflitti dopo modifica")
        pren_ids = {p1["id"], p2["id"]}
        conflitto_ancora_attivo = next(
            (c for c in conflitti_attivi
             if c["prenotazione_id_1"] in pren_ids or c["prenotazione_id_2"] in pren_ids),
            None
        )
        assert conflitto_ancora_attivo is None, "Il conflitto non è stato chiuso dopo la modifica"

        coord.delete(f"/prenotazioni/{p1['id']}")
        coord.delete(f"/prenotazioni/{p2['id']}")

    def test_risolvi_conflitto_mantieni_1(self, coord):
        r1 = crea_singola(coord, AULA_ID_A, TRA_3, "08:00", "13:00")
        r2 = crea_singola(coord, AULA_ID_A, TRA_3, "10:00", "15:00")
        p1 = ok(r1, "crea p1 risolvi")
        p2 = ok(r2, "crea p2 risolvi")

        r_cf = coord.get("/conflitti/?solo_attivi=true")
        conflitti = ok(r_cf, "get conflitti risolvi")
        pren_ids = {p1["id"], p2["id"]}
        conflitto = next(
            (c for c in conflitti
             if c["prenotazione_id_1"] in pren_ids or c["prenotazione_id_2"] in pren_ids),
            None
        )
        assert conflitto is not None

        r_risolvi = coord.post(
            f"/conflitti/{conflitto['id']}/risolvi?azione=mantieni_1"
        )
        assert r_risolvi.status_code == 200
        assert r_risolvi.json()["ok"] == True

        # Verifica che il conflitto sia chiuso
        r_cf2 = coord.get("/conflitti/?solo_attivi=true")
        conflitti_dopo = ok(r_cf2, "conflitti dopo risoluzione")
        ancora = next(
            (c for c in conflitti_dopo
             if c["prenotazione_id_1"] in pren_ids or c["prenotazione_id_2"] in pren_ids),
            None
        )
        assert ancora is None, "Conflitto ancora attivo dopo risoluzione"

        # Cleanup — p1 potrebbe essere già eliminata se era lo slot annullato
        for pid in [p1["id"], p2["id"]]:
            coord.delete(f"/prenotazioni/{pid}")


# ─── Filtri API ───────────────────────────────────────────────────────────────

class TestFiltri:
    def test_filtro_sede(self, coord):
        r = coord.get("/prenotazioni/?sede_id=1")
        data = ok(r, "filtro sede")
        assert isinstance(data, list)

    def test_filtro_date(self, coord):
        r = coord.get(f"/prenotazioni/?data_dal={DOMANI}&data_al={TRA_7}")
        data = ok(r, "filtro date")
        assert isinstance(data, list)

    def test_filtro_conflitti_sede(self, coord):
        r = coord.get("/conflitti/?sede_id=1&solo_attivi=true")
        assert r.status_code in (200, 403)

    def test_prenotazione_inesistente_404(self, coord):
        r = coord.get("/prenotazioni/99999999")
        assert r.status_code == 404


# ─── Permessi OPERATIVO ───────────────────────────────────────────────────────

class TestPermessi:
    def test_operativo_non_vede_utenti(self, operativo):
        r = operativo.get("/utenti/")
        assert r.status_code == 403

    def test_operativo_puo_prenotare(self, operativo):
        r = crea_singola(operativo, AULA_ID_A, TRA_7)
        data = ok(r, "operativo crea prenotazione")
        assert data["tipo"].lower() == "singola"
        # Cleanup — operativo può eliminare solo le sue
        operativo.delete(f"/prenotazioni/{data['id']}")

    def test_operativo_non_elimina_altrui(self, operativo, coord):
        r = crea_singola(coord, AULA_ID_A, TRA_14)
        pren_id = ok(r, "coord crea per test permessi")["id"]

        r_del = operativo.delete(f"/prenotazioni/{pren_id}")
        assert r_del.status_code == 403

        coord.delete(f"/prenotazioni/{pren_id}")