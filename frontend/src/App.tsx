import React from 'react'
import { BrowserRouter, Route, Routes, Link, Navigate } from 'react-router-dom'
import LoginPage from './pages/Login'
import SignupPage from './pages/Signup'
import Dashboard from './pages/Dashboard'
import ProfilePage from './pages/Profile'
import OutfitsPage from './pages/Outfits'
import TryOnPage from './pages/TryOn'
import RecommendationsPage from './pages/Recommendations'
import { AuthProvider, useAuth } from './context/AuthContext'
import './App.css'

function Protected({ children }: { children: React.ReactNode }) {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen flex flex-col">
          <Nav />
          <div className="flex-1">
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
              <Route path="/profile" element={<Protected><ProfilePage /></Protected>} />
              <Route path="/outfits" element={<Protected><OutfitsPage /></Protected>} />
              <Route path="/tryon" element={<Protected><TryOnPage /></Protected>} />
              <Route path="/recommendations" element={<Protected><RecommendationsPage /></Protected>} />
              <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </AuthProvider>
  )
}

function Nav() {
  const { token, logout } = useAuth()
  return (
    <nav className="border-b bg-white/70 backdrop-blur sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/dashboard" className="font-semibold">Trylia</Link>
          {token && (
            <>
              <Link to="/profile" className="text-sm">Profile</Link>
              <Link to="/outfits" className="text-sm">Outfits</Link>
              <Link to="/tryon" className="text-sm">Try-On</Link>
              <Link to="/recommendations" className="text-sm">Recommendations</Link>
            </>
          )}
        </div>
        <div>
          {token ? (
            <button className="btn btn-sm" onClick={logout}>Logout</button>
          ) : (
            <div className="flex gap-2">
              <Link to="/login" className="btn btn-sm">Login</Link>
              <Link to="/signup" className="btn btn-sm">Signup</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
