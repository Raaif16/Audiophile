import { api } from './client'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
}

export interface User {
  id: string
  email: string
  username: string
  is_active: boolean
  is_admin: boolean
  created_at: string
}

export const login = async (credentials: LoginCredentials): Promise<void> => {
  await api.post('/auth/login', credentials)
}

export const register = async (data: RegisterData): Promise<User> => {
  const response = await api.post('/auth/register', data)
  return response.data
}

export const logout = async (): Promise<void> => {
  await api.post('/auth/logout')
}

export const getCurrentUser = async (): Promise<User | null> => {
  try {
    const response = await api.get('/auth/me')
    return response.data
  } catch {
    return null
  }
}

export interface AdminStats {
  total_users: number
  active_users: number
  admin_users: number
}

export const getAdminStats = async (): Promise<AdminStats> => {
  const response = await api.get('/admin/stats')
  return response.data
}

export const getAdminUsers = async (): Promise<User[]> => {
  const response = await api.get('/admin/users')
  return response.data
}
