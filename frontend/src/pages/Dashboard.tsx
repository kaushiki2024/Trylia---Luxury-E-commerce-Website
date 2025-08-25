import React from 'react'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card title="Profile" to="/profile" desc="Upload and view your photos" />
        <Card title="Outfits" to="/outfits" desc="Browse outfit gallery" />
        <Card title="Try-On" to="/tryon" desc="Pick a photo and outfit" />
        <Card title="Recommendations" to="/recommendations" desc="View suggested outfits" />
      </div>
    </div>
  )
}

function Card({ title, desc, to }: { title: string; desc: string; to: string }) {
  return (
    <Link to={to} className="block border rounded p-4 hover:shadow">
      <div className="text-lg font-medium">{title}</div>
      <div className="text-sm text-gray-600">{desc}</div>
    </Link>
  )
}

