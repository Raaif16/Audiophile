import axios from 'axios'

// Use '/api' prefix for dev server proxy, or full URL for production
const baseURL = import.meta.env.DEV ? '/api' : (import.meta.env.VITE_API_URL || 'http://localhost:8000')

export const api = axios.create({
  baseURL,
  withCredentials: true, // Critical for httpOnly cookies
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for 401 handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - auth state will be handled by query invalidation
      console.log('Unauthorized - session may have expired')
    }
    return Promise.reject(error)
  }
)

export default api
