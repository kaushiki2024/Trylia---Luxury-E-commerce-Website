import React, { useEffect, useState } from 'react'
import { getOutfit3D, listOutfits } from '../services/api'
import { Outfit3DViewer } from '../components/Outfit3DViewer'

export default function OutfitsPage() {
  const [items, setItems] = useState<any[]>([])
  const [query, setQuery] = useState('')
  const [selectedModelUrl, setSelectedModelUrl] = useState<string | null>(null)

  useEffect(() => {
    listOutfits().then(setItems).catch(() => setItems([]))
  }, [])

  const filtered = items.filter(o => o.name.toLowerCase().includes(query.toLowerCase()))

  const open3D = async (outfitId: number) => {
    try {
      const m = await getOutfit3D(outfitId)
      setSelectedModelUrl(m.file_url)
    } catch {
      setSelectedModelUrl(null)
      alert('No 3D model available for this outfit')
    }
  }

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-semibold">Outfit Gallery</h1>
      <input className="input" placeholder="Filter by name" value={query} onChange={e=>setQuery(e.target.value)} />
      <div className="grid gap-4 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {filtered.map(o => (
          <div key={o.outfit_id} className="border rounded overflow-hidden">
            <img src={o.image_url} className="w-full h-40 object-cover" />
            <div className="p-2 flex items-center justify-between">
              <div>
                <div className="font-medium">{o.name}</div>
                <div className="text-xs text-gray-500">{o.category}</div>
              </div>
              <button className="btn" onClick={() => open3D(o.outfit_id)}>View 3D</button>
            </div>
          </div>
        ))}
      </div>
      {selectedModelUrl && (
        <div className="space-y-2">
          <div className="text-sm text-gray-600">Interactive 3D Viewer</div>
          <Outfit3DViewer modelUrl={selectedModelUrl} />
        </div>
      )}
    </div>
  )
}

