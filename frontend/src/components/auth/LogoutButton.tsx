import { useLogout } from '../../hooks/useAuth'

export function LogoutButton() {
  const logout = useLogout()

  return (
    <button onClick={() => logout.mutate()} disabled={logout.isPending}>
      {logout.isPending ? 'Logging out...' : 'Logout'}
    </button>
  )
}
