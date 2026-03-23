import { useState } from 'react'
import { useRegister } from '../../hooks/useAuth'

export function RegisterForm() {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const register = useRegister()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    register.mutate({ email, username, password })
  }

  return (
    <form onSubmit={handleSubmit} className="auth-form">
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
        required
        minLength={3}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
        minLength={8}
      />
      <button type="submit" disabled={register.isPending}>
        {register.isPending ? 'Creating account...' : 'Register'}
      </button>
      {register.isError && <p className="error">Error: {register.error?.message || 'Registration failed'}</p>}
      {register.isSuccess && <p className="success">Account created! You can now log in.</p>}
    </form>
  )
}
