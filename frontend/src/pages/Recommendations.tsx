import React, { useEffect, useState } from 'react'
import { listRecommendations } from '../services/api'

export default function RecommendationsPage() {
  const [items, setItems] = useState<any[]>([])
  useEffect(() => { listRecommendations().then(setItems).catch(() => setItems([])) }, [])
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-semibold">Recommendations</h1>
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {items.map(r => (
          <div key={r.rec_id} className="border rounded p-4">
            <div className="font-medium">Outfit #{r.outfit_id}</div>
            <div className="text-sm text-gray-600">Score: {r.score}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

