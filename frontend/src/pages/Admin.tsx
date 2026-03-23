import { AdminRoute } from '../components/admin/AdminRoute'
import { AdminDashboard } from '../components/admin/AdminDashboard'

export default function Admin() {
  return (
    <AdminRoute>
      <AdminDashboard />
    </AdminRoute>
  )
}