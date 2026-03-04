# 📋 REVISIONE COMPLETA BACKEND - SISTEMA 2 RUOLI

Analizziamo ogni sezione di Swagger per verificare coerenza con il nuovo sistema.

---

## ✅ AUTENTICAZIONE - OK

| Endpoint                    | Ruoli       | Note                                              |
| --------------------------- | ----------- | ------------------------------------------------- |
| `POST /api/v1/auth/login` | Tutti       | ✅ Restituisce `ruolo: OPERATIVO/COORDINAMENTO` |
| `GET /api/v1/auth/me`     | Autenticati | ✅ Profilo utente corrente                        |

---

## ✅ UTENTI - OK

| Endpoint                               | Ruoli         | Note                          |
| -------------------------------------- | ------------- | ----------------------------- |
| `GET /api/v1/utenti/`                | COORDINAMENTO | ✅ Lista tutti utenti         |
| `POST /api/v1/utenti/`               | COORDINAMENTO | ✅ Crea nuovo utente          |
| `DELETE /api/v1/utenti/{id}`         | COORDINAMENTO | ✅ Soft-delete (attivo=False) |
| `PATCH /api/v1/utenti/{id}/riattiva` | COORDINAMENTO | ✅ Riattiva utente            |

---

## ⚠️ SEDI - DESCRIZIONE DA AGGIORNARE

| Endpoint                  | Ruoli | Stato                       | Problema                                                                           |
| ------------------------- | ----- | --------------------------- | ---------------------------------------------------------------------------------- |
| `GET /api/v1/sedi/`     | Tutti | ✅ OK                       | -                                                                                  |
| `POST /api/v1/sedi/`    | ?     | ⚠️**DA VERIFICARE** | Descrizione dice: "solo Segreteria Sede e Coordinamento" →**RUOLI VECCHI!** |
| `GET /api/v1/sedi/{id}` | Tutti | ✅ OK                       | -                                                                                  |

**DOMANDA:** Chi può creare sedi nel nuovo sistema?

* **Opzione A:** Solo COORDINAMENTO
* **Opzione B:** Tutti (OPERATIVO + COORDINAMENTO)

---

## ✅ AULE - OK

| Endpoint               | Ruoli         | Note                                  |
| ---------------------- | ------------- | ------------------------------------- |
| `GET /api/v1/aule/`  | Tutti         | ✅ Lista aule (opzionale filtro sede) |
| `POST /api/v1/aule/` | COORDINAMENTO | ✅ Crea aula                          |

---

## ⚠️ PRENOTAZIONI - DESCRIZIONE DA AGGIORNARE

| Endpoint                               | Ruoli     | Stato                             | Problema                                                                             |
| -------------------------------------- | --------- | --------------------------------- | ------------------------------------------------------------------------------------ |
| `POST /prenotazioni/singola`         | OPERATIVO | ✅ OK                             | Auto-approvazione + rilevamento conflitti                                            |
| `POST /prenotazioni/massiva`         | OPERATIVO | ✅ OK                             | Auto-approvazione + rilevamento conflitti                                            |
| `GET /prenotazioni/`                 | Dipende   | ⚠️**DESCRIZIONE VECCHIA** | Menziona: "ResponsabileCorso, SegreteriaSede, ResponsabileSede, SegreteriaDidattica" |
| `GET /prenotazioni/{id}`             | Dipende   | ✅ OK                             | -                                                                                    |
| `GET /prenotazioni/slot-liberi/{id}` | Tutti     | ✅ OK                             | -                                                                                    |

**DESCRIZIONE DA AGGIORNARE per `GET /prenotazioni/`:**

Attuale (SBAGLIATO):

```
ResponsabileCorso: solo le proprie
SegreteriaSede/ResponsabileSede: della propria sede
SegreteriaDidattica: tutte le prenotazioni della propria sede
Coordinamento: tutte
```

Nuovo (CORRETTO):

```
OPERATIVO: prenotazioni della propria sede
COORDINAMENTO: tutte le prenotazioni
```

---

## ✅ CONFLITTI - OK

| Endpoint                         | Ruoli         | Note                                                           |
| -------------------------------- | ------------- | -------------------------------------------------------------- |
| `GET /conflitti/`              | COORDINAMENTO | ✅ Lista conflitti (filtro sede + solo_attivi)                 |
| `GET /conflitti/{id}`          | COORDINAMENTO | ✅ Dettaglio conflitto completo                                |
| `POST /conflitti/{id}/risolvi` | COORDINAMENTO | ✅ 4 azioni: mantieni_1, mantieni_2, elimina_entrambe, manuale |
| `GET /conflitti/stats/summary` | COORDINAMENTO | ✅ Statistiche riepilogative                                   |

---

## ❓ FUNZIONALITÀ MANCANTI

### 1. Eliminazione/Annullamento Prenotazioni

**Non c'è endpoint per:**

* Annullare una prenotazione
* Eliminare una prenotazione

**DOMANDA:** Serve aggiungere:

* `DELETE /prenotazioni/{id}` → Annulla prenotazione?
* Chi può annullare? Solo chi l'ha creata? Anche COORDINAMENTO?

### 2. Modifica Prenotazioni

**Non c'è endpoint per:**

* Modificare orario/data di una prenotazione esistente

**DOMANDA:** Serve `PATCH /prenotazioni/{id}`?

---

## 📊 RIEPILOGO PROBLEMI

| # | Problema                                                | Gravità       | Azione                 |
| - | ------------------------------------------------------- | -------------- | ---------------------- |
| 1 | Descrizione `POST /sedi/`menziona vecchi ruoli        | ⚠️ Media     | Aggiornare descrizione |
| 2 | Descrizione `GET /prenotazioni/`menziona vecchi ruoli | ⚠️ Media     | Aggiornare descrizione |
| 3 | Manca endpoint annullamento prenotazioni                | ❓ Da decidere | Aggiungere se serve    |
| 4 | Manca endpoint modifica prenotazioni                    | ❓ Da decidere | Aggiungere se serve    |

---

## 🎯 DOMANDE PER TE

1. **Creazione sedi:** Chi può creare sedi? Solo COORDINAMENTO o anche OPERATIVO?
2. **Annullamento prenotazioni:** Serve la possibilità di annullare prenotazioni? Chi può farlo?
3. **Modifica prenotazioni:** Serve modificare prenotazioni esistenti o si elimina e ricrea?
4. **Visibilità prenotazioni OPERATIVO:** Deve vedere solo le sue o tutte della sua sede?
