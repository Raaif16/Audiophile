import { useState } from 'react'
import { Routes, Route, Navigate, Link } from 'react-router-dom'
import { useCurrentUser } from './hooks/useAuth'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import { LogoutButton } from './components/auth'
import './App.css'

function App() {
  const { data: user, isLoading } = useCurrentUser()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner" />
        <p className="loading-text">Loading...</p>
      </div>
    )
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="navbar-brand">
          <Link to="/" className="brand-link">Audiophile</Link>
          <button
            className="mobile-menu-toggle"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle navigation menu"
            aria-expanded={isMobileMenuOpen}
          >
            <span className={`hamburger-line ${isMobileMenuOpen ? 'open' : ''}`} />
            <span className={`hamburger-line ${isMobileMenuOpen ? 'open' : ''}`} />
            <span className={`hamburger-line ${isMobileMenuOpen ? 'open' : ''}`} />
          </button>
        </div>
        <div className={`navbar-menu ${isMobileMenuOpen ? 'open' : ''}`}>
          <Link to="/" className="nav-link" onClick={() => setIsMobileMenuOpen(false)}>Home</Link>
          {user?.is_admin && (
            <Link to="/admin" className="nav-link nav-link-admin" onClick={() => setIsMobileMenuOpen(false)}>
              Admin
              <span className="admin-nav-badge">A</span>
            </Link>
          )}
          {!user && (
            <>
              <Link to="/login" className="nav-link" onClick={() => setIsMobileMenuOpen(false)}>Login</Link>
              <Link to="/register" className="nav-link" onClick={() => setIsMobileMenuOpen(false)}>Register</Link>
            </>
          )}
          {user && (
            <div className="nav-user-section">
              <span className="user-greeting">Welcome, {user.username}</span>
              <LogoutButton />
            </div>
          )}
        </div>
      </nav>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/login"
            element={!user ? <Login /> : <Navigate to="/" />}
          />
          <Route
            path="/register"
            element={!user ? <Register /> : <Navigate to="/" />}
          />
          <Route
            path="/admin"
            element={<Admin />}
          />
        </Routes>
      </main>
    </div>
  )
}

export default App
