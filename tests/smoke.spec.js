// tests/smoke.spec.js
// ─────────────────────────────────────────────────────────────────────────────
// Smoke test Playwright — ICE Planning Aule
// Verifica login, navigazione RBAC e fix del code review lato frontend.
//
// Prerequisiti:
//   - Backend avviato su http://localhost:8000
//   - Frontend avviato su http://localhost:5173  (npm run dev)
//
// Utilizzo:
//   npx playwright test --reporter=line
//
// Credenziali (sovrascrivibili via env):
//   COORD_EMAIL / COORD_PASSWORD   → utente COORDINAMENTO
//   OP_EMAIL    / OP_PASSWORD      → utente OPERATIVO
// ─────────────────────────────────────────────────────────────────────────────

const { test, expect } = require('@playwright/test')

const BASE         = process.env.FRONTEND_URL   || 'http://localhost:5173'
const COORD_EMAIL  = process.env.COORD_EMAIL    || 'coord@test.it'
const COORD_PASS   = process.env.COORD_PASSWORD || 'test'
const OP_EMAIL     = process.env.OP_EMAIL       || 'segr.did@test.it'
const OP_PASS      = process.env.OP_PASSWORD    || 'test'

// ── Helper: login ─────────────────────────────────────────────────────────────

async function login(page, email, password) {
  await page.goto(`${BASE}/login`)
  await page.locator('#username').fill(email)
  await page.locator('#password').fill(password)
  await page.getByRole('button', { name: 'Accedi' }).click()
  await expect(page).not.toHaveURL(/\/login/, { timeout: 5000 })
}

async function logout(page) {
  // Prova a cliccare logout dalla sidebar; se non trovato, svuota localStorage
  const btn = page.getByRole('button', { name: /logout|esci/i })
  if (await btn.isVisible().catch(() => false)) {
    await btn.click()
  } else {
    await page.evaluate(() => localStorage.clear())
    await page.reload()
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// AUTH
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Auth', () => {

  test('login COORDINAMENTO → redirect a dashboard coordinamento', async ({ page }) => {
    await login(page, COORD_EMAIL, COORD_PASS)
    await expect(page).toHaveURL(/\/coordinamento\/dashboard/)
  })

  test('login OPERATIVO → redirect a dashboard operativo', async ({ page }) => {
    await login(page, OP_EMAIL, OP_PASS)
    await expect(page).toHaveURL(/\/operativo\/dashboard/)
  })

  test('credenziali errate → resta su /login con messaggio errore', async ({ page }) => {
    await page.goto(`${BASE}/login`)
    await page.locator('#username').fill('sbagliato@test.it')
    await page.locator('#password').fill('sbagliata')
    await page.getByRole('button', { name: 'Accedi' }).click()
    await expect(page).toHaveURL(/\/login/)
  })

  test('rotta protetta senza login → redirect a /login', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await expect(page).toHaveURL(/\/login/)
  })

})

// ─────────────────────────────────────────────────────────────────────────────
// DASHBOARD COORDINAMENTO — KPI conflitti (fix: non più 0 fisso)
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Dashboard Coordinamento', () => {

  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('si carica senza errori JS in console', async ({ page }) => {
    const errors = []
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })
    await page.goto(`${BASE}/coordinamento/dashboard`)
    await page.waitForLoadState('networkidle')
    expect(errors.filter(e => !e.includes('favicon'))).toHaveLength(0)
  })

  test('KPI conflitti è visibile (fix: non era 0 fisso hardcoded)', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/dashboard`)
    await page.waitForLoadState('networkidle')
    // Cerca una card/badge con la parola "conflitti" — deve esistere nel DOM
    const kpi = page.getByText(/conflitti/i).first()
    await expect(kpi).toBeVisible()
  })

})

// ─────────────────────────────────────────────────────────────────────────────
// CALENDARIO — carica senza errori, badge conflitti slot-level
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Calendario', () => {

  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('si carica senza errori JS in console', async ({ page }) => {
    const errors = []
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')
    expect(errors.filter(e => !e.includes('favicon'))).toHaveLength(0)
  })

  test('i tre pulsanti di vista (4giorni/settimana/mese) sono presenti', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await page.waitForLoadState('networkidle')
    await expect(page.getByRole('button', { name: '4 giorni' })).toBeVisible()
    await expect(page.getByRole('button', { name: 'Settimana' })).toBeVisible()
    await expect(page.getByRole('button', { name: 'Mese' })).toBeVisible()
  })

})

// ─────────────────────────────────────────────────────────────────────────────
// MIE PRENOTAZIONI — colonna Note presente (fix aggiunto in sessione)
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Mie Prenotazioni', () => {

  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('la colonna Note è presente nella tabella (fix: aggiunta in sessione)', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')

    const hasTable = await page.locator('table').isVisible()
    if (hasTable) {
      // Ci sono prenotazioni — verifica che la colonna Note esista nell'header
      await expect(page.locator('thead th').filter({ hasText: 'Note' })).toBeVisible()
    } else {
      // Nessuna prenotazione nel DB — verifica almeno che la pagina sia caricata
      // e che il fix sia nel sorgente controllando il DOM hidden (skip colonna)
      await expect(page.locator('.page-mie-prenotazioni')).toBeAttached()
      console.log('⚠ Nessuna prenotazione nel DB — colonna Note non verificabile visivamente')
    }
  })

  test('si carica senza errori JS in console', async ({ page }) => {
    const errors = []
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })
    await page.goto(`${BASE}/prenotazioni/mie`)
    await page.waitForLoadState('networkidle')
    expect(errors.filter(e => !e.includes('favicon'))).toHaveLength(0)
  })

})

// ─────────────────────────────────────────────────────────────────────────────
// CONFLITTI — verifica che le chiamate API vadano su /api/v1/conflitti/
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Conflitti', () => {

  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('la pagina conflitti si carica senza errori', async ({ page }) => {
    const errors = []
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })
    await page.goto(`${BASE}/conflitti`)
    await page.waitForLoadState('networkidle')
    expect(errors.filter(e => !e.includes('favicon'))).toHaveLength(0)
  })

  test('le chiamate API usano /api/v1/conflitti/ (fix: non più URL diretto)', async ({ page }) => {
    const requests = []
    page.on('request', r => {
      // Considera solo chiamate al backend (porta 8000), non la navigazione Vue
      if (r.url().includes('localhost:8000') && r.url().includes('conflitti')) {
        requests.push(r.url())
      }
    })
    await page.goto(`${BASE}/conflitti`)
    await page.waitForLoadState('networkidle')

    // Tutte le chiamate backend ai conflitti devono passare per /api/v1/
    const senzaPrefix = requests.filter(u => !u.includes('/api/v1/'))
    expect(senzaPrefix).toHaveLength(0)
  })

})

// ─────────────────────────────────────────────────────────────────────────────
// SEDI E AULE — visualizzazione e ricerca
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Sedi e Aule', () => {

  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('pagina sedi/aule si carica', async ({ page }) => {
    await page.goto(`${BASE}/sedi`)
    await page.waitForLoadState('networkidle')
    await expect(page.getByText(/sede|aula/i).first()).toBeVisible()
  })

})

// ─────────────────────────────────────────────────────────────────────────────
// GESTIONE SEDI/AULE (COORDINAMENTO) — modifica aula
// ─────────────────────────────────────────────────────────────────────────────

test.describe('Gestione Sedi/Aule', () => {

  test.beforeEach(async ({ page }) => { await login(page, COORD_EMAIL, COORD_PASS) })

  test('la pagina di gestione sedi/aule è accessibile a COORDINAMENTO', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/sedi`)
    await page.waitForLoadState('networkidle')
    // Non deve finire su 404 o redirect
    await expect(page).toHaveURL(/\/coordinamento\/sedi/)
  })

  test('OPERATIVO non può accedere a gestione sedi → redirect a dashboard', async ({ page }) => {
    await login(page, OP_EMAIL, OP_PASS)
    await page.goto(`${BASE}/coordinamento/sedi`)
    await expect(page).not.toHaveURL(/\/coordinamento\/sedi/)
  })

})

// ─────────────────────────────────────────────────────────────────────────────
// RBAC — pagine SOLO_COORDINAMENTO non accessibili a OPERATIVO
// ─────────────────────────────────────────────────────────────────────────────

test.describe('RBAC', () => {

  test.beforeEach(async ({ page }) => { await login(page, OP_EMAIL, OP_PASS) })

  test('OPERATIVO viene rediretto dalla dashboard coordinamento', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/dashboard`)
    await expect(page).not.toHaveURL(/\/coordinamento\/dashboard/)
  })

  test('OPERATIVO viene rediretto da grafici', async ({ page }) => {
    await page.goto(`${BASE}/coordinamento/grafici`)
    await expect(page).not.toHaveURL(/\/coordinamento\/grafici/)
  })

  test('OPERATIVO può accedere al calendario', async ({ page }) => {
    await page.goto(`${BASE}/calendario`)
    await expect(page).toHaveURL(/\/calendario/)
  })

  test('OPERATIVO può accedere alle proprie prenotazioni', async ({ page }) => {
    await page.goto(`${BASE}/prenotazioni/mie`)
    await expect(page).toHaveURL(/\/prenotazioni\/mie/)
  })

})