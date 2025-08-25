import React, { useEffect, useState } from 'react'
import { listPhotos, uploadPhoto } from '../services/api'

export default function ProfilePage() {
  const [imageUrl, setImageUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [items, setItems] = useState<any[]>([])
  const [error, setError] = useState('')

  const refresh = async () => {
    try {
      const data = await listPhotos()
      setItems(data)
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Failed to load photos')
    }
  }

  useEffect(() => { refresh() }, [])

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      if (!imageUrl) return
      await uploadPhoto(imageUrl)
      setImageUrl('')
      await refresh()
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-semibold">Profile</h1>
      <form onSubmit={onSubmit} className="space-x-2">
        <input className="input w-80" placeholder="Image URL" value={imageUrl} onChange={e=>setImageUrl(e.target.value)} />
        <button className="btn" disabled={loading}>{loading ? 'Uploading...' : 'Upload'}</button>
      </form>
      {error && <div className="text-red-600 text-sm">{error}</div>}
      <div className="grid gap-4 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
        {items.map(p => (
          <div key={p.photo_id} className="border rounded overflow-hidden">
            <img src={p.image_url} className="w-full h-40 object-cover" />
          </div>
        ))}
      </div>
    </div>
  )
}

