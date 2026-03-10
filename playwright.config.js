// playwright.config.js
const { defineConfig, devices } = require('@playwright/test')

module.exports = defineConfig({
  testDir: './tests',
  timeout: 15000,
  retries: 0,
  reporter: 'line',

  use: {
    baseURL: process.env.FRONTEND_URL || 'http://localhost:5173',
    headless: true,
    screenshot: 'only-on-failure',
    video: 'off',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // Se vuoi che Playwright avvii il frontend automaticamente:
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:5173',
  //   reuseExistingServer: true,
  // },
})