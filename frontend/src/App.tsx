import { Routes, Route, Navigate, Link } from 'react-router-dom'
import { useCurrentUser } from './hooks/useAuth'
import Login from './pages/Login'
import Register from './pages/Register'
import { LogoutButton } from './components/auth'
import './App.css'

function App() {
  const { data: user, isLoading } = useCurrentUser()

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="app">
      <nav className="navbar">
        <Link to="/">Home</Link>
        {!user && (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
        {user && (
          <>
            <span>Welcome, {user.username}</span>
            <LogoutButton />
          </>
        )}
      </nav>
      <Routes>
        <Route path="/" element={<div className="home-page"><h1>Home Page</h1><p>Welcome to Audiophile Headphones!</p></div>} />
        <Route
          path="/login"
          element={!user ? <Login /> : <Navigate to="/" />}
        />
        <Route
          path="/register"
          element={!user ? <Register /> : <Navigate to="/" />}
        />
      </Routes>
    </div>
  )
}

export default App
