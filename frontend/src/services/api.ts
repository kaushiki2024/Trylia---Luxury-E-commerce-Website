import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({ baseURL: API_BASE })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auth
export async function login(email: string, password: string) {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)
  const { data } = await api.post('/auth/login', form, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
  return data as { access_token: string; token_type: string }
}

export async function signup(payload: { name: string; email: string; password: string }) {
  const { data } = await api.post('/auth/signup', payload)
  return data
}

// Photos
export async function uploadPhoto(imageUrl: string) {
  const { data } = await api.post('/photos', { image_url: imageUrl })
  return data
}

export async function listPhotos() {
  const { data } = await api.get('/photos')
  return data
}

// Outfits
export async function listOutfits() {
  const { data } = await api.get('/outfits')
  return data
}

export async function getOutfit3D(outfitId: number) {
  const { data } = await api.get(`/outfits/${outfitId}/3d-model`)
  return data as { id: number; outfit_id: number; file_url: string; format: string; created_at: string }
}

// Try-on
export async function createTryOn(payload: { photo_id?: number; outfit_id?: number }) {
  const { data } = await api.post('/sessions', payload)
  return data
}

// Recommendations
export async function listRecommendations() {
  const { data } = await api.get('/recommendations')
  return data
}

