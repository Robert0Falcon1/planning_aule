"""
seed_prenotazioni.py
────────────────────
Genera prenotazioni mock via API REST.

Uso:
    python seed_prenotazioni.py --user dev@inforcoopecipa.it --password final
    python seed_prenotazioni.py --url http://localhost:8000 --user X --password Y
"""

import argparse
import random
import sys
from datetime import date, timedelta

import requests

DEFAULT_URL      = "http://localhost:8000"
DEFAULT_USERNAME = "admin@ice.it"
DEFAULT_PASSWORD = "admin"

FASCE_ORARIE = [
    ("08:00", "10:00"),
    ("08:00", "13:00"),
    ("09:00", "12:00"),
    ("09:00", "13:00"),
    ("10:00", "13:00"),
    ("13:00", "16:00"),
    ("14:00", "17:00"),
    ("14:00", "18:00"),
    ("15:00", "18:00"),
]

NOTE = [
    "Corso GOL – modulo base",
    "Corso GOL – modulo avanzato",
    "FSE – formazione obbligatoria",
    "Aula studio autonomo",
    "Corso lingua italiana",
    "Orientamento professionale",
    "Laboratorio informatica",
    "Corso sicurezza sul lavoro",
    None, None, None,
]

GIORNI_LUN_VEN = [0, 1, 2, 3, 4]   # 0=lun … 4=ven (come vuole il backend)


# ── HTTP helpers ───────────────────────────────────────────────────────────────

def login(base_url, username, password):
    r = requests.post(
        f"{base_url}/api/v1/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    r.raise_for_status()
    print(f"✓ Login OK  ({username})")
    return r.json()["access_token"]


def get_json(base_url, path, token):
    r = requests.get(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def post_json(base_url, path, payload, token):
    return requests.post(
        f"{base_url}{path}",
        json=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=15,
    )


# ── Recupera / crea corsi ──────────────────────────────────────────────────────

def ottieni_corso_ids(base_url, token):
    """
    Tenta di leggere i corsi dal backend.
    Se l'endpoint non esiste (404) o la lista è vuota, usa gli ID
    recuperati dalle prenotazioni già esistenti (se ce ne sono),
    altrimenti si arrende e chiede di inserire ID manualmente.
    """
    # 1. prova endpoint corsi
    for path in ("/api/v1/corsi/", "/api/v1/courses/"):
        try:
            corsi = get_json(base_url, path, token)
            if isinstance(corsi, list) and corsi:
                ids = [c["id"] for c in corsi]
                print(f"✓ Corsi trovati via {path}: {ids}")
                return ids
        except Exception:
            pass

    # 2. prova a estrarre corso_id dalle prenotazioni esistenti
    try:
        pren = get_json(base_url, "/api/v1/prenotazioni/", token)
        ids  = list({p["corso_id"] for p in pren if p.get("corso_id")})
        if ids:
            print(f"✓ Corso&nbsp;IDs estratti dalle prenotazioni esistenti: {ids}")
            return ids
    except Exception:
        pass

    # 3. chiedi all'utente
    print("\n⚠  Impossibile determinare i corso_id validi automaticamente.")
    raw = input("   Inserisci una lista di corso_id validi separati da virgola (es: 1,2,3): ").strip()
    if raw:
        ids = [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]
        if ids:
            return ids

    print("✗ Nessun corso_id disponibile. Impossibile procedere.")
    sys.exit(1)


# ── Seed singole ───────────────────────────────────────────────────────────────

def crea_singole(base_url, token, aule, corso_ids, n=70):
    oggi  = date.today()
    date_range = [
        oggi + timedelta(days=i)
        for i in range(-7, 61)
        if (oggi + timedelta(days=i)).isoweekday() <= 5
    ]
    ok = err = 0
    print(f"\n── Prenotazioni singole ({n}) ──────────────────────────────────")

    for i in range(n):
        aula     = random.choice(aule)
        giorno   = random.choice(date_range)
        fascia   = random.choice(FASCE_ORARIE)
        corso_id = random.choice(corso_ids)
        nota     = random.choice(NOTE)

        payload = {
            "aula_id":  aula["id"],
            "corso_id": corso_id,
            "slot": {
                "data":       giorno.isoformat(),
                "ora_inizio": fascia[0],
                "ora_fine":   fascia[1],
            },
        }
        if nota:
            payload["note"] = nota

        r = post_json(base_url, "/api/v1/prenotazioni/singola", payload, token)
        if r.status_code in (200, 201):
            ok += 1
            conflitti = r.json().get("richiesta", {}).get("ha_conflitti", False)
            flag = " ⚠ conflitto" if conflitti else ""
            print(f"  [{i+1:3d}] ✓  Aula {aula['id']:2d} | Corso {corso_id:2d} | {giorno} {fascia[0]}-{fascia[1]}{flag}")
        else:
            err += 1
            try:
                detail = r.json().get("detail", r.text)
            except Exception:
                detail = r.text
            print(f"  [{i+1:3d}] ✗  Aula {aula['id']:2d} | Corso {corso_id:2d} | {giorno} → {r.status_code}: {str(detail)[:120]}")

    print(f"\n  Singole: {ok} OK, {err} errori")
    return ok, err


# ── Seed massive ───────────────────────────────────────────────────────────────

def crea_massive(base_url, token, aule, corso_ids, n=15):
    oggi = date.today()
    ok = err = 0
    print(f"\n── Prenotazioni massive ({n}) ──────────────────────────────────")

    ricorrenze = ["settimanale", "settimanale", "bisettimanale"]  # no giornaliera: richiede giorni_settimana comunque

    for i in range(n):
        aula       = random.choice(aule)
        corso_id   = random.choice(corso_ids)
        fascia     = random.choice(FASCE_ORARIE)
        ricorrenza = random.choice(ricorrenze)
        nota       = random.choice(NOTE)

        offset_inizio = random.randint(1, 30)
        durata_giorni = random.randint(14, 35)
        data_inizio   = oggi + timedelta(days=offset_inizio)
        data_fine     = data_inizio + timedelta(days=durata_giorni)

        # giorni_settimana: sempre obbligatorio secondo il backend
        n_giorni         = random.randint(1, 3)
        giorni_settimana = sorted(random.sample(GIORNI_LUN_VEN, n_giorni))

        payload = {
            "aula_id":          aula["id"],
            "corso_id":         corso_id,
            "data_inizio":      data_inizio.isoformat(),
            "data_fine":        data_fine.isoformat(),
            "ora_inizio":       fascia[0],
            "ora_fine":         fascia[1],
            "tipo_ricorrenza":  ricorrenza,
            "giorni_settimana": giorni_settimana,
        }
        if nota:
            payload["note"] = nota

        r = post_json(base_url, "/api/v1/prenotazioni/massiva", payload, token)
        if r.status_code in (200, 201):
            ok += 1
            slots_n = len(r.json().get("slots", []))
            giorni_str = str(giorni_settimana)
            print(f"  [{i+1:2d}] ✓  Aula {aula['id']:2d} | Corso {corso_id:2d} | {data_inizio}→{data_fine} ({ricorrenza} {giorni_str}, {slots_n} slot)")
        else:
            err += 1
            try:
                detail = r.json().get("detail", r.text)
            except Exception:
                detail = r.text
            print(f"  [{i+1:2d}] ✗  Aula {aula['id']:2d} | Corso {corso_id:2d} | {data_inizio}→{data_fine} → {r.status_code}: {str(detail)[:120]}")

    print(f"\n  Massive: {ok} OK, {err} errori")
    return ok, err


# ── Prenotazione garantita per smoke test Playwright ──────────────────────────

def crea_prenotazione_smoke(base_url, token, aule, corso_ids):
    """
    Crea una prenotazione fissa con nota per coord@test.it.
    Serve a garantire che MiePrenotazioniPage mostri la tabella (non il v-else)
    durante i test Playwright, così la colonna Note è verificabile visivamente.
    """
    print("\n── Prenotazione smoke test ─────────────────────────────────")

    # Usa la prima aula disponibile e il primo corso
    aula     = aule[0]
    corso_id = corso_ids[0]
    # Domani lavorativo (salta weekend)
    domani = date.today() + timedelta(days=1)
    while domani.isoweekday() > 5:
        domani += timedelta(days=1)

    payload = {
        "aula_id":  aula["id"],
        "corso_id": corso_id,
        "slot": {
            "data":       domani.isoformat(),
            "ora_inizio": "09:00",
            "ora_fine":   "12:00",
        },
        "note": "Prenotazione smoke test — non eliminare",
    }

    r = post_json(base_url, "/api/v1/prenotazioni/singola", payload, token)
    if r.status_code in (200, 201):
        print(f"  ✓ Smoke prenotazione creata: Aula {aula['id']} | Corso {corso_id} | {domani} 09:00-12:00")
    else:
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        print(f"  ✗ Smoke prenotazione fallita: {r.status_code}: {str(detail)[:120]}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Seed prenotazioni ICE Planning Aule")
    parser.add_argument("--url",      default=DEFAULT_URL)
    parser.add_argument("--user",     default=DEFAULT_USERNAME)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--singole",  type=int, default=70)
    parser.add_argument("--massive",  type=int, default=15)
    parser.add_argument("--corsi",    default="",
                        help="Lista corso_id separati da virgola (es: 1,2,3). Se omessa, viene rilevata automaticamente.")
    args = parser.parse_args()

    print("=" * 60)
    print("  ICE Planning Aule — Seed Prenotazioni")
    print("=" * 60)

    try:
        token = login(args.url, args.user, args.password)
    except Exception as e:
        print(f"\n✗ Login fallito: {e}"); sys.exit(1)

    # Aule
    try:
        aule = get_json(args.url, "/api/v1/aule/", token)
        print(f"✓ Aule: {len(aule)}")
    except Exception as e:
        print(f"\n✗ Impossibile caricare le aule: {e}"); sys.exit(1)

    if not aule:
        print("\n✗ Nessuna aula trovata."); sys.exit(1)

    # Corsi
    if args.corsi:
        corso_ids = [int(x.strip()) for x in args.corsi.split(",") if x.strip().isdigit()]
        print(f"✓ Corso&nbsp;IDs da argomento: {corso_ids}")
    else:
        corso_ids = ottieni_corso_ids(args.url, token)

    random.seed(42)

    s_ok, s_err = crea_singole(args.url, token, aule, corso_ids, n=args.singole)
    m_ok, m_err = crea_massive(args.url, token, aule, corso_ids, n=args.massive)

    # Prenotazione garantita per smoke test Playwright
    # (assicura che MiePrenotazioni abbia almeno una riga → colonna Note visibile)
    crea_prenotazione_smoke(args.url, token, aule, corso_ids)

    print("\n" + "=" * 60)
    print(f"  TOTALE: {s_ok + m_ok} create, {s_err + m_err} errori")
    print("=" * 60)


if __name__ == "__main__":
    main()