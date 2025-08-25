import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'

type AuthState = {
  token: string | null
  user: { user_id: number; name: string; email: string } | null
}

type AuthContextType = AuthState & {
  login: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))
  const [user, setUser] = useState<AuthState['user']>(null)

  useEffect(() => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
  }, [token])

  const value = useMemo<AuthContextType>(() => ({
    token,
    user,
    login: (t: string) => setToken(t),
    logout: () => { setToken(null); setUser(null) }
  }), [token, user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

