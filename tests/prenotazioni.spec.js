// tests/e2e/prenotazioni.spec.js
// ─────────────────────────────────────────────────────────────────────────────
// Test E2E completi — ICE Planning Aule
// Copre tutti i flussi utente principali.
//
// Prerequisiti:
//   - Backend avviato su http://localhost:8000
//   - Frontend avviato su http://localhost:5173
//
// Utilizzo:
//   npx playwright test tests/e2e/ --reporter=line
// ─────────────────────────────────────────────────────────────────────────────

const { test, expect } = require('@playwright/test')

const BASE        = process.env.FRONTEND_URL    || 'http://localhost:5173'
const COORD_EMAIL = process.env.COORD_EMAIL     || 'dev@inforcoopecipa.it'
const COORD_PASS  = process.env.COORD_PASSWORD  || 'final'
const OP_EMAIL    = process.env.OP_EMAIL        || 'colline@inforcoopecipa.it'
const OP_PASS     = process.env.OP_PASSWORD     || 'colline!'

// Data domani in formato YYYY-MM-DD
const domani = new Date(Date.now() + 86400000).toISOString().slice(0, 10)
const tra7   = new Date(Date.now() + 7 * 86400000).toISOString().slice(0, 10)
const tra14  = new Date(Date.now() + 14 * 86400000).toISOString().slice(0, 10)
const tra21  = new Date(Date.now() + 21 * 86400000).toISOString().slice(0, 10)

// ── Helpers ───────────────────────────────────────────────────────────────────

async function login(page, email, password) {
  await page.goto(`${BASE}/login`)
  await page.locator('#username').fill(email)
  await page.locator('#password').fill(password)
  await page.getByRole('button', { name: 'Accedi' }).click()
  await expect(page).not.toHaveURL(/\/login/, { timeout: 8000 })
}

async function noConsoleErrors(page) {
  const errors = []
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })
  return () => errors.filter(e =>
    !e.includes('favicon') &&
    !e.includes('net::ERR') &&
    !e.includes('404')
  )
}

// ─────────────────────────────────────────────────────────────────────────────
// NUOVA PRENOTAZIONE SINGOLA
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Nuova Prenotazione Singola', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('form si carica con tutti i campi obbligatori', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/nuova`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Prenotazione singola')).toBeVisible()
    await expect(page.getByText('Sede *')).toBeVisible()
    await expect(page.getByText('Aula *')).toBeVisible()
    await expect(page.getByText('ID Corso *')).toBeVisible()
    await expect(page.getByText('Data *')).toBeVisible()
    await expect(page.getByText('Ora inizio *')).toBeVisible()
    await expect(page.getByText('Ora fine *')).toBeVisible()
  })

  test('selezione sede carica le aule corrispondenti', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/nuova`)
    await page.waitForLoadState('networkidle')

    const selectSede = page.locator('select').first()
    await selectSede.selectOption({ index: 1 })
    await page.waitForTimeout(500)

    // Dopo la selezione sede, il select aula non dovrebbe più dire "seleziona sede prima"
    const selectAula = page.locator('select').nth(1)
    await expect(selectAula).not.toBeDisabled()
  })

  test('validazione mostra errori se i campi obbligatori sono vuoti', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/nuova`)
    await page.waitForLoadState('networkidle')

    await page.getByRole('button', { name: 'Conferma prenotazione' }).click()
    await expect(page.getByText('Obbligatorio').first()).toBeVisible()
  })

  test('prenotazione singola creata con successo', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/nuova`)
    await page.waitForLoadState('networkidle')

    // Seleziona prima sede disponibile
    const selectSede = page.locator('select').first()
    await selectSede.selectOption({ index: 1 })
    await page.waitForTimeout(600)

    // Seleziona prima aula disponibile
    const selectAula = page.locator('select').nth(1)
    await selectAula.selectOption({ index: 1 })

    // Corso ID
    await page.locator('input[type="number"]').first().fill('1')

    // Data
    await page.locator('input[type="date"]').first().fill(tra14)

    // Ora inizio
    const selectOraInizio = page.locator('select').nth(2)
    await selectOraInizio.selectOption('09:00')

    // Ora fine
    const selectOraFine = page.locator('select').nth(3)
    await selectOraFine.selectOption('13:00')

    await page.getByRole('button', { name: 'Conferma prenotazione' }).click()
    await expect(page.getByText(/confermata con successo/i)).toBeVisible({ timeout: 8000 })
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// NUOVA PRENOTAZIONE MASSIVA
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Nuova Prenotazione Massiva', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('tab massiva si carica con i campi ricorrenza', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/nuova?tipo=massiva`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Prenotazione massiva')).toBeVisible()
    await expect(page.getByText('Data inizio *')).toBeVisible()
    await expect(page.getByText('Data fine *')).toBeVisible()
    await expect(page.getByText('Tipo ricorrenza *')).toBeVisible()
  })

  test('selezione settimanale mostra i giorni della settimana', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/nuova?tipo=massiva`)
    await page.waitForLoadState('networkidle')

    // Cerca il select tipo ricorrenza e seleziona settimanale
    const tipoSelect = page.getByText('Tipo ricorrenza *').locator('..').locator('select')
    await tipoSelect.selectOption('settimanale')

    await expect(page.getByText('Giorni della settimana *')).toBeVisible()
    await expect(page.getByLabel('Lun')).toBeVisible()
    await expect(page.getByLabel('Mar')).toBeVisible()
    await expect(page.getByLabel('Mer')).toBeVisible()
  })

  test('validazione giorni settimana obbligatoria per ricorrenza settimanale', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/nuova?tipo=massiva`)
    await page.waitForLoadState('networkidle')

    await page.getByRole('button', { name: 'Crea prenotazioni ricorrenti' }).click()
    await expect(page.getByText('Obbligatorio').first()).toBeVisible()
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// MIE PRENOTAZIONI
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Mie Prenotazioni', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('la tabella ha tutte le colonne attese', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    const hasTable = await page.locator('table').isVisible()
    if (!hasTable) {
      console.log('⚠ Nessuna prenotazione nel DB')
      return
    }

    for (const col of ['Data', 'Orario', 'Aula', 'Corso', 'Note', 'Conflitti', 'Azioni']) {
      await expect(page.locator('thead').getByText(col)).toBeVisible()
    }
  })

  test('filtro sede restringe i risultati', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    const selectSede = page.locator('select').first()
    const opzioni = await selectSede.locator('option').count()
    if (opzioni <= 1) return // nessuna sede disponibile

    await selectSede.selectOption({ index: 1 })
    await page.waitForTimeout(400)

    // Il contatore "Risultati filtrati" deve essere visibile
    await expect(page.getByText('Risultati filtrati')).toBeVisible()
  })

  test('pulsante Nuova porta alla pagina nuova prenotazione', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    await page.getByRole('main').getByRole('link', { name: /nuova/i }).click()
    await expect(page).toHaveURL(/nuova/)
  })

  test('bottone modifica apre il modale', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    const hasTable = await page.locator('table').isVisible()
    if (!hasTable) return

    // Clicca il primo bottone matita
    await page.locator('button[title="Modifica slot"]').first().click()
    await expect(page.getByText('Modifica slot')).toBeVisible({ timeout: 3000 })
  })

  test('bottone elimina apre la modale di conferma', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    const hasTable = await page.locator('table').isVisible()
    if (!hasTable) return

    await page.locator('button.btn-outline-danger').first().click()
    await expect(page.getByText('Conferma eliminazione')).toBeVisible({ timeout: 3000 })
  })

  test('reset filtri ripristina tutti i filtri', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    // Imposta un filtro data
    await page.locator('input[type="date"]').first().fill(domani)
    await page.waitForTimeout(300)

    await page.getByRole('button', { name: 'Reset' }).click()
    await expect(page.locator('input[type="date"]').first()).toHaveValue('')
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// MODIFICA SLOT (modale)
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Modale Modifica Slot', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('modale si apre con i dati pre-popolati', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    const hasTable = await page.locator('table').isVisible()
    if (!hasTable) return

    await page.locator('button[title="Modifica slot"]').first().click()
    await page.waitForTimeout(500)

    // Il modale deve avere i campi principali visibili
    await expect(page.getByText('Sede *')).toBeVisible()
    await expect(page.getByText('Aula *')).toBeVisible()
    await expect(page.getByText('ID Corso *')).toBeVisible()
    await expect(page.getByText('Data *')).toBeVisible()
  })

  test('modale si chiude con Annulla', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    const hasTable = await page.locator('table').isVisible()
    if (!hasTable) return

    await page.locator('button[title="Modifica slot"]').first().click()
    await page.waitForTimeout(300)

    await page.getByRole('button', { name: 'Annulla' }).click()
    await expect(page.getByText('Modifica slot')).not.toBeVisible({ timeout: 3000 })
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// CALENDARIO
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Calendario', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('navigazione avanti/indietro funziona', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')

    const labelIniziale = await page.locator('.fw-semibold').filter({
      hasText: /gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic/i
    }).first().textContent()

    // Avanza di un periodo
    await page.locator('button').filter({ has: page.locator('use[href*="chevron-right"]') }).click()
    await page.waitForTimeout(400)

    const labelDopo = await page.locator('.fw-semibold').filter({
      hasText: /gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic/i
    }).first().textContent()

    expect(labelDopo).not.toBe(labelIniziale)
  })

  test('bottone Oggi riporta alla settimana corrente', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')

    // Vai avanti
    await page.locator('button').filter({ has: page.locator('use[href*="chevron-right"]') }).click()
    await page.waitForTimeout(300)

    await page.getByRole('button', { name: 'Oggi' }).click()
    await page.waitForTimeout(300)

    // Dopo "Oggi" deve essere visibile la data odierna nella griglia
    const oggi = new Date().getDate().toString()
    await expect(page.getByText(oggi).first()).toBeVisible()
  })

  test('cambio vista a Mese mostra la griglia mensile', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')

    await page.getByRole('button', { name: 'Mese' }).click()
    await page.waitForTimeout(400)

    // La vista mensile mostra i nomi dei giorni
    await expect(page.getByText('Lun')).toBeVisible()
    await expect(page.getByText('Dom')).toBeVisible()
  })

  test('cambio vista a 4 giorni', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')

    await page.getByRole('button', { name: '4 giorni' }).click()
    await page.waitForTimeout(400)

    // In vista 4 giorni ci devono essere esattamente 4 colonne giorno
    const colonne = await page.locator('.cal-day-head').count()
    expect(colonne).toBe(4)
  })

  test('filtro sede è presente e funzionante', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')

    const selectSede = page.locator('select').filter({ hasText: 'Tutte le sedi' })
    await expect(selectSede).toBeVisible()

    const opzioni = await selectSede.locator('option').count()
    expect(opzioni).toBeGreaterThan(1)
  })

  test('pulsante Nuova nel calendario porta al form', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')

    await page.getByRole('main').getByRole('link', { name: /nuova/i }).click()
    await expect(page).toHaveURL(/nuova/)
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// CONFLITTI
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Conflitti', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('pagina si carica correttamente', async ({ page }) => {
    const getErrors = await noConsoleErrors(page)
    await page.goto(`${BASE}/conflitti`)
    await page.waitForLoadState('networkidle')
    expect(getErrors()).toHaveLength(0)
  })

  test('toggle "Solo attivi" è presente e cliccabile', async ({ page }) => {
    await page.goto(`${BASE}/conflitti`)
    await page.waitForLoadState('networkidle')

    const toggle = page.locator('#soloAttivi')
    await expect(toggle).toBeVisible()
    await toggle.click()
    await page.waitForTimeout(400)
    await toggle.click() // ripristina
  })

  test('filtro sede è presente', async ({ page }) => {
    await page.goto(`${BASE}/conflitti`)
    await page.waitForLoadState('networkidle')

    await expect(page.locator('select').filter({ hasText: 'Tutte le sedi' })).toBeVisible()
  })

    test('se ci sono conflitti mostra i pulsanti di risoluzione', async ({ page }) => {
    await page.goto(`${BASE}/conflitti`)
    await page.waitForLoadState('networkidle')

    const nessunConflitto = await page.locator('.text-success').isVisible().catch(() => false)
    if (nessunConflitto) {
        // Nessun conflitto attivo — test non applicabile
        return
    }

    // Ci sono conflitti — verifica i pulsanti di risoluzione
    await expect(page.getByRole('button', { name: /mantieni/i }).first()).toBeVisible()
    await expect(page.getByRole('button', { name: /annulla/i }).first()).toBeVisible()
    })

  test('badge con numero conflitti è visibile se ci sono conflitti', async ({ page }) => {
    await page.goto(`${BASE}/conflitti`)
    await page.waitForLoadState('networkidle')

    const haConflitti = await page.locator('.conflitto-pill').isVisible().catch(() => false)
    if (!haConflitti) return

    // Il badge con il numero deve essere presente nell'header
    await expect(page.locator('.badge.bg-danger').first()).toBeVisible()
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// CAMBIO PASSWORD (modale dal menu utente)
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Cambio Password', () => {
  test('modale si apre cliccando sul nome utente', async ({ page }) => {
    await login(page, OP_EMAIL, OP_PASS)
    await page.waitForLoadState('networkidle')

    // Clicca sul nome utente nell'header
    await page.locator('.hover-link').filter({ has: page.locator('use[href*="it-user"]') }).click()
    await expect(page.getByText('Cambia password')).toBeVisible({ timeout: 3000 })
  })

  test('validazione modale: conferma diversa da nuova password', async ({ page }) => {
    await login(page, OP_EMAIL, OP_PASS)

    await page.locator('.hover-link').filter({ has: page.locator('use[href*="it-user"]') }).click()
    await page.waitForTimeout(300)

    await page.locator('input[autocomplete="current-password"]').fill('colline!')
    await page.locator('input[autocomplete="new-password"]').first().fill('nuova123')
    await page.locator('input[autocomplete="new-password"]').last().fill('diversa456')

    await page.getByRole('button', { name: 'Salva' }).click()
    await expect(page.getByText(/non coincidono/i)).toBeVisible()
  })

  test('validazione modale: password troppo corta', async ({ page }) => {
    await login(page, OP_EMAIL, OP_PASS)

    await page.locator('.hover-link').filter({ has: page.locator('use[href*="it-user"]') }).click()
    await page.waitForTimeout(300)

    await page.locator('input[autocomplete="current-password"]').fill('colline!')
    await page.locator('input[autocomplete="new-password"]').first().fill('abc')
    await page.locator('input[autocomplete="new-password"]').last().fill('abc')

    await page.getByRole('button', { name: 'Salva' }).click()
    await expect(page.getByText(/8 caratteri/i)).toBeVisible()
  })

  test('icone occhio visibili nei campi password', async ({ page }) => {
    await login(page, OP_EMAIL, OP_PASS)

    await page.locator('.hover-link').filter({ has: page.locator('use[href*="it-user"]') }).click()
    await page.waitForTimeout(300)

    // Deve esserci almeno un bottone con l'icona password-visible/invisible
    await expect(page.locator('use[href*="it-password"]').first()).toBeVisible()
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// DASHBOARD OPERATIVO
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Dashboard Operativo', () => {
  test.beforeEach(async ({ page }) => { await login(page, OP_EMAIL, OP_PASS) })

  test('KPI visibili: slot totali, oggi, conflitti, prossimi 7gg', async ({ page }) => {
    await page.goto(`${BASE}/operativo/dashboard`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Slot totali')).toBeVisible()
    await expect(page.getByText('Slot oggi')).toBeVisible()
    await expect(page.getByText('Conflitti')).toBeVisible()
    await expect(page.getByText('Slot prossimi 7 gg')).toBeVisible()
  })

  test('sezione prossimi 7 giorni è presente', async ({ page }) => {
    await page.goto(`${BASE}/operativo/dashboard`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Prossimi 7 giorni')).toBeVisible()
  })

  test('link Nuova prenotazione funziona', async ({ page }) => {
    await page.goto(`${BASE}/operativo/dashboard`)
    await page.waitForLoadState('networkidle')

    await page.getByRole('main').getByRole('link', { name: /nuova prenotazione/i }).click()
    await expect(page).toHaveURL(/nuova/)
  })

  test('link Calendario funziona', async ({ page }) => {
    await page.goto(`${BASE}/operativo/dashboard`)
    await page.waitForLoadState('networkidle')

    await page.getByRole('main').getByRole('link', { name: /calendario/i }).first().click()
    await expect(page).toHaveURL(/calendario/)
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// DASHBOARD COORDINAMENTO
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Dashboard Coordinamento', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('KPI aule occupate oggi è visibile', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/dashboard`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText(/aule occupate/i)).toBeVisible()
  })

  test('nessun errore JS in console', async ({ page }) => {
    const getErrors = await noConsoleErrors(page)
    await page.goto(`${BASE}/coordinamento/dashboard`)
    await page.waitForLoadState('networkidle')
    expect(getErrors()).toHaveLength(0)
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// SEDI & AULE (pagina pubblica)
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Sedi e Aule', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('le card delle aule mostrano capienza e stato', async ({ page }) => {
    await page.goto(`${BASE}/sedi`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText(/capienza/i).first()).toBeVisible()
    await expect(page.getByText(/libera|prenotata/i).first()).toBeVisible()
  })

  test('il selettore data cambia la disponibilità', async ({ page }) => {
    await page.goto(`${BASE}/sedi`)
    await page.waitForLoadState('networkidle')

    const inputData = page.locator('input[type="date"]').first()
    await inputData.fill(tra7)
    await page.waitForLoadState('networkidle')

    // La pagina non deve crashare
    await expect(page.locator('.aula-card').first()).toBeVisible({ timeout: 5000 })
  })

  test('il pulsante "Prenota per..." porta al form prenotazione', async ({ page }) => {
    await page.goto(`${BASE}/sedi`)
    await page.waitForLoadState('networkidle')

    const btnPrenota = page.getByRole('link', { name: /prenota per/i }).first()
    if (await btnPrenota.isVisible()) {
      await btnPrenota.click()
      await expect(page).toHaveURL(/nuova/)
    }
  })

  test('le ore della slot grid sono visibili (08-18)', async ({ page }) => {
    await page.goto(`${BASE}/sedi`)
    await page.waitForLoadState('networkidle')

    await expect(page.locator('.slot-grid').first()).toBeVisible()
    await expect(page.locator('.slot-label').first()).toBeVisible()
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// GRAFICI (solo COORDINAMENTO)
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Grafici', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('KPI prenotazioni totali/confermate/conflitti visibili', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/grafici`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Prenotazioni totali')).toBeVisible()
    await expect(page.getByText('Confermate')).toBeVisible()
    await expect(page.getByText('Con conflitti')).toBeVisible()
  })

  test('filtro sede è presente', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/grafici`)
    await page.waitForLoadState('networkidle')

    await expect(page.locator('select').filter({ hasText: 'Tutte le sedi' })).toBeVisible()
  })

  test('pulsanti granularità mese/settimana funzionano', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/grafici`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByRole('button', { name: 'Settimana' })).toBeVisible()
    await expect(page.getByRole('button', { name: 'Mese' })).toBeVisible()

    await page.getByRole('button', { name: 'Settimana' }).click()
    await page.waitForTimeout(400)
    await expect(page.getByText(/settimana/i).first()).toBeVisible()
  })

  test('bottone CSV è presente', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/grafici`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByRole('button', { name: /CSV/i })).toBeVisible()
  })

  test('nessun errore JS in console', async ({ page }) => {
    const getErrors = await noConsoleErrors(page)
    await page.goto(`${BASE}/coordinamento/grafici`)
    await page.waitForLoadState('networkidle')
    expect(getErrors()).toHaveLength(0)
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// GESTIONE UTENTI (solo COORDINAMENTO)
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Gestione Utenti', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('pagina lista utenti si carica', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/utenti`)
    await page.waitForLoadState('networkidle')

    await expect(page).toHaveURL(/utenti/)
    await expect(page.locator('h2, .page-title').first()).toBeVisible()
  })

  test('nessun errore JS in console', async ({ page }) => {
    const getErrors = await noConsoleErrors(page)
    await page.goto(`${BASE}/coordinamento/utenti`)
    await page.waitForLoadState('networkidle')
    expect(getErrors()).toHaveLength(0)
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// SITUAZIONE OGGI (solo COORDINAMENTO)
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Situazione Oggi', () => {
  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('pagina si carica con KPI', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/situazione-oggi`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Slot totali')).toBeVisible()
    await expect(page.getByText('Aule occupate')).toBeVisible()
  })

  test('selettore data è presente e modifica la vista', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/situazione-oggi`)
    await page.waitForLoadState('networkidle')

    const inputData = page.locator('input[type="date"]').first()
    await expect(inputData).toBeVisible()

    await inputData.fill(tra7)
    await page.waitForLoadState('networkidle')
    // Non deve crashare
    await expect(page.getByRole('heading', { name: 'Situazione Oggi' })).toBeVisible()
  })

  test('navigazione avanti/indietro tra giorni funziona', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/situazione-oggi`)
    await page.waitForLoadState('networkidle')

    const inputData = page.locator('input[type="date"]').first()
    const valoreIniziale = await inputData.inputValue()

    await page.locator('button').filter({ has: page.locator('use[href*="chevron-right"]') }).click()
    await page.waitForTimeout(300)

    const valoreDopo = await inputData.inputValue()
    expect(valoreDopo).not.toBe(valoreIniziale)
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// SIDEBAR E NAVIGAZIONE
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Sidebar e Navigazione', () => {
  test('sidebar COORDINAMENTO ha le voci attese', async ({ page }) => {
    await login(page, COORD_EMAIL, COORD_PASS)
    await page.waitForLoadState('networkidle')

    await expect(page.locator('nav, aside').getByRole('link', { name: /calendario/i }).first()).toBeVisible()
    await expect(page.locator('[aria-label*="laterale"]').getByRole('link').first()).toBeVisible()
    await expect(page.locator('nav, aside').getByRole('link', { name: /conflitti/i }).first()).toBeVisible()
  })

  test('sidebar OPERATIVO non mostra le voci admin', async ({ page }) => {
    await login(page, OP_EMAIL, OP_PASS)
    await page.waitForLoadState('networkidle')

    // L'OPERATIVO non deve vedere "Gestione Utenti"
    await expect(page.getByText('Gestione Utenti')).not.toBeVisible()
  })

  test('toggle sidebar funziona su desktop', async ({ page }) => {
    await login(page, COORD_EMAIL, COORD_PASS)
    await page.setViewportSize({ width: 1280, height: 800 })
    await page.waitForLoadState('networkidle')

    // Cerca il pulsante toggle sidebar
    const toggle = page.locator('button').filter({ has: page.locator('use[href*="it-burger"]') }).first()
    if (await toggle.isVisible()) {
      await toggle.click()
      await page.waitForTimeout(300)
      await toggle.click() // ripristina
    }
  })
})

// ─────────────────────────────────────────────────────────────────────────────
// RESPONSIVITÀ — test su mobile
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Responsività Mobile', () => {
  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 }) // iPhone SE
    await login(page, COORD_EMAIL, COORD_PASS)
  })

  test('dashboard si carica su mobile', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/dashboard`)
    await page.waitForLoadState('networkidle')
    await expect(page.locator('.page-header')).toBeVisible()
  })

  test('calendario si carica su mobile', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')
    // Il calendario ha uno scroll orizzontale su mobile
    await expect(page.locator('.cal-week, .mes-grid').first()).toBeVisible()
  })

  test('form nuova prenotazione è usabile su mobile', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/nuova`)
    await page.waitForLoadState('networkidle')
    await expect(page.getByRole('heading', { name: 'Nuova Prenotazione' })).toBeVisible()
    await expect(page.locator('.card').first()).toBeVisible()
  })
})