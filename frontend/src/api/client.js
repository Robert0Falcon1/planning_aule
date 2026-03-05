const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

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

  const res = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  })

  if (!res.ok) {
    let msg = `Errore ${res.status}`
    try {
      const err = await res.json()
      msg = err.detail || err.message || msg
    } catch (_) {}
    throw new Error(msg)
  }

  // 204 No Content
  if (res.status === 204) return null
  return res.json()
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
  if (!res.ok) throw new Error(`Download fallito (${res.status})`)
  const blob = await res.blob()
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = filename
  a.click()
  URL.revokeObjectURL(a.href)
}
