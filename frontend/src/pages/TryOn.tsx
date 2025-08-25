import React, { useEffect, useState } from 'react'
import { createTryOn, listOutfits, listPhotos, getOutfit3D } from '../services/api'
import { Outfit3DViewer } from '../components/Outfit3DViewer'

export default function TryOnPage() {
  const [photos, setPhotos] = useState<any[]>([])
  const [outfits, setOutfits] = useState<any[]>([])
  const [photoId, setPhotoId] = useState<number | undefined>(undefined)
  const [outfitId, setOutfitId] = useState<number | undefined>(undefined)
  const [resultUrl, setResultUrl] = useState<string | null>(null)
  const [modelUrl, setModelUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    listPhotos().then(setPhotos)
    listOutfits().then(setOutfits)
  }, [])

  const runTryOn = async () => {
    if (!photoId || !outfitId) return
    setLoading(true)
    try {
      const session = await createTryOn({ photo_id: photoId, outfit_id: outfitId })
      setResultUrl(session.result_url || null)
    } finally {
      setLoading(false)
    }
  }

  const load3D = async () => {
    if (!outfitId) return
    try {
      const m = await getOutfit3D(outfitId)
      setModelUrl(m.file_url)
    } catch {
      setModelUrl(null)
      alert('No 3D model available')
    }
  }

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-semibold">Virtual Try-On</h1>
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <div className="font-medium">Select Photo</div>
          <select className="input w-full" value={photoId ?? ''} onChange={e=>setPhotoId(Number(e.target.value))}>
            <option value="">--</option>
            {photos.map(p => <option key={p.photo_id} value={p.photo_id}>{p.photo_id}</option>)}
          </select>
        </div>
        <div className="space-y-2">
          <div className="font-medium">Select Outfit</div>
          <select className="input w-full" value={outfitId ?? ''} onChange={e=>setOutfitId(Number(e.target.value))}>
            <option value="">--</option>
            {outfits.map(o => <option key={o.outfit_id} value={o.outfit_id}>{o.name}</option>)}
          </select>
        </div>
      </div>
      <div className="flex gap-2">
        <button className="btn" onClick={runTryOn} disabled={loading || !photoId || !outfitId}>{loading ? 'Processing...' : 'Run Try-On (Image)'}</button>
        <button className="btn" onClick={load3D} disabled={!outfitId}>Load 3D Outfit</button>
      </div>
      {resultUrl && (
        <div className="space-y-2">
          <div className="text-sm text-gray-600">Processed Result</div>
          <img src={resultUrl} className="max-w-full rounded border" />
        </div>
      )}
      {modelUrl && (
        <div className="space-y-2">
          <div className="text-sm text-gray-600">Interactive 3D Viewer</div>
          <Outfit3DViewer modelUrl={modelUrl} />
        </div>
      )}
    </div>
  )
}

