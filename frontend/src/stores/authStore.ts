import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  isAuthModalOpen: boolean
  authMode: 'login' | 'register'
  setAuthModalOpen: (open: boolean) => void
  setAuthMode: (mode: 'login' | 'register') => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthModalOpen: false,
      authMode: 'login',
      setAuthModalOpen: (open) => set({ isAuthModalOpen: open }),
      setAuthMode: (mode) => set({ authMode: mode }),
    }),
    {
      name: 'auth-ui-storage',
      partialize: (state) => ({ authMode: state.authMode }),
    }
  )
)
