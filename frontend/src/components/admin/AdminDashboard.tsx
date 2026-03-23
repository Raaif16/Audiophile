import { useEffect, useState } from 'react'
import { useCurrentUser } from '../../hooks/useAuth'
import { getAdminStats, getAdminUsers, type User, type AdminStats } from '../../api/auth'
import './AdminDashboard.css'

export function AdminDashboard() {
  const { data: adminUser } = useCurrentUser()
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        setLoading(true)
        const [statsData, usersData] = await Promise.all([
          getAdminStats(),
          getAdminUsers()
        ])
        setStats(statsData)
        setUsers(usersData)
      } catch (err) {
        setError('Failed to load admin data')
        console.error('Admin data fetch error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchAdminData()
  }, [])

  if (loading) {
    return (
      <div className="admin-loading">
        <div className="loading-spinner" />
        <p>Loading admin dashboard...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="admin-error">
        <p>{error}</p>
      </div>
    )
  }

  return (
    <div className="admin-dashboard">
      <header className="admin-header">
        <h1>Admin Dashboard</h1>
        <div className="admin-user-info">
          <span className="admin-badge">Admin</span>
          <span className="admin-email">{adminUser?.email}</span>
          <span className="admin-username">@{adminUser?.username}</span>
        </div>
      </header>

      {/* Stats Section */}
      <section className="admin-section">
        <h2>Overview</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-value">{stats?.total_users || 0}</span>
            <span className="stat-label">Total Users</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{stats?.active_users || 0}</span>
            <span className="stat-label">Active Users</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{stats?.admin_users || 0}</span>
            <span className="stat-label">Admin Users</span>
          </div>
        </div>
      </section>

      {/* User Management Section */}
      <section className="admin-section">
        <h2>User Management</h2>
        <div className="users-table-container">
          <table className="users-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Status</th>
                <th>Role</th>
                <th>Joined</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>@{user.username}</td>
                  <td>{user.email}</td>
                  <td>
                    <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                      {user.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <span className={`role-badge ${user.is_admin ? 'admin' : 'user'}`}>
                      {user.is_admin ? 'Admin' : 'User'}
                    </span>
                  </td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Product Management Placeholder */}
      <section className="admin-section">
        <h2>Product Management</h2>
        <div className="placeholder-section">
          <p>Product management features coming soon...</p>
          <ul className="feature-list">
            <li>Add new headphones</li>
            <li>Edit product details</li>
            <li>Manage categories</li>
            <li>Upload product images</li>
          </ul>
        </div>
      </section>
    </div>
  )
}