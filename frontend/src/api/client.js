import { formatErrorMessage } from '@/utils/errorHandler'

export const BASE_URL = import.meta.env.VITE_API_URL || `${window.location.protocol}//${window.location.hostname}:8000/api/v1`

function getToken() {
  return localStorage.getItem('ice_token')
}

async function request(method, path, body = null, params = null) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) headers['Authorization'] = `Bearer ${token}`

  let url = `${BASE_URL}${path}`
  if (params) {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v != null))
    )
    if (qs.toString()) url += `?${qs}`
  }

  try {
    const res = await fetch(url, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    })

    if (!res.ok) {
      let errorData = null
      try {
        errorData = await res.json()
      } catch (_) {
        errorData = { detail: `Errore ${res.status}` }
      }

      // Crea errore strutturato
      const error = new Error(formatErrorMessage({ status: res.status, data: errorData }))
      error.status = res.status
      error.data = errorData
      throw error
    }

    // 204 No Content
    if (res.status === 204) return null
    return res.json()

  } catch (error) {
    // Errore di rete (fetch fallito, CORS, timeout)
    if (error instanceof TypeError) {
      const formattedError = new Error(formatErrorMessage(error))
      formattedError.isNetworkError = true
      throw formattedError
    }
    // Rilancia l'errore già formattato
    throw error
  }
}

export const apiGet    = (path, params)       => request('GET',    path, null, params)
export const apiPost   = (path, body)          => request('POST',   path, body)
export const apiPut    = (path, body)          => request('PUT',    path, body)
export const apiPatch  = (path, body)          => request('PATCH',  path, body)
export const apiDelete = (path)                => request('DELETE', path)

/** Scarica un blob (CSV, PDF) */
export async function apiDownload(path, filename, params = null) {
  const headers = {}
  const token = getToken()
  if (token) headers['Authorization'] = `Bearer ${token}`

  let url = `${BASE_URL}${path}`
  if (params) {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v != null))
    )
    if (qs.toString()) url += `?${qs}`
  }

  const res = await fetch(url, { headers })
  if (!res.ok) {
    const error = new Error(`Download fallito: ${formatErrorMessage({ status: res.status, data: {} })}`)
    throw error
  }
  const blob = await res.blob()
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = filename
  a.click()
  URL.revokeObjectURL(a.href)
}