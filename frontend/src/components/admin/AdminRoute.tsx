import { Navigate } from 'react-router-dom'
import { useCurrentUser } from '../../hooks/useAuth'

interface AdminRouteProps {
  children: React.ReactNode
}

export function AdminRoute({ children }: AdminRouteProps) {
  const { data: user, isLoading } = useCurrentUser()

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner" />
        <p className="loading-text">Loading...</p>
      </div>
    )
  }

  // Not logged in - redirect to login
  if (!user) {
    return <Navigate to="/login" replace />
  }

  // Logged in but not admin - redirect to home
  if (!user.is_admin) {
    return <Navigate to="/" replace />
  }

  // Admin - render children
  return <>{children}</>
}