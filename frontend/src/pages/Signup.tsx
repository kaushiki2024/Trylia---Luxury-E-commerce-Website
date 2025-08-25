import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { signup, login } from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function SignupPage() {
  const { login: setToken } = useAuth()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await signup({ name, email, password })
      const res = await login(email, password)
      setToken(res.access_token)
      navigate('/dashboard')
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen grid place-items-center p-4">
      <form onSubmit={onSubmit} className="w-full max-w-sm space-y-4 bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-semibold">Sign up</h1>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <input className="input" placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="input" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="btn w-full" disabled={loading}>{loading ? 'Loading...' : 'Create account'}</button>
        <p className="text-sm">Have an account? <Link to="/login" className="text-blue-600">Login</Link></p>
      </form>
    </div>
  )
}

