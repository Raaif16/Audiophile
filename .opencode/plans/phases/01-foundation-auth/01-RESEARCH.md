# Phase 1: Foundation & Authentication - Research

**Researched:** March 23, 2026
**Domain:** FastAPI + MongoDB/Beanie ODM + JWT Auth + React 19 + Vite + TanStack Query + Zustand
**Confidence:** HIGH

## Summary

Phase 1 establishes the technical foundation for the Audiophile Headphones Ecommerce platform. This phase is critical because decisions made here (database schema design, authentication patterns, project structure) are expensive to change later. The stack combines proven technologies: FastAPI for the async Python backend, MongoDB with Beanie ODM for flexible document storage, JWT with httpOnly cookies for secure authentication, and React 19 with Vite for the modern frontend.

**Primary recommendation:** Use FastAPI's native OAuth2 JWT flow with httpOnly cookies (not localStorage), Beanie ODM for MongoDB with Pydantic v2 models, and React 19's new Actions pattern with TanStack Query for server state. Structure the project with completely separate `backend/` and `frontend/` folders from day one.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| AUTH-01 | User can sign up with email and password | FastAPI OAuth2 + pwdlib Argon2 hashing + Beanie User document |
| AUTH-02 | User can log in and stay logged in across sessions (JWT with httpOnly cookies) | PyJWT with HS256, httpOnly cookie response, 30min expiry |
| AUTH-03 | User can log out from any page | Clear httpOnly cookie endpoint, Zustand auth state reset |
| AUTH-04 | User session expires after 30 minutes of inactivity | JWT `exp` claim with 30min delta, cookie max-age |
| BACK-01 | FastAPI with async/await support | Native async/await, Motor async MongoDB driver |
| BACK-02 | MongoDB with Beanie ODM | Beanie 1.29+ with Pydantic v2, AsyncMongoClient |
| BACK-03 | JWT authentication with 32+ character random secret | `openssl rand -hex 32` generates 64-char secret |
| BACK-04 | Password hashing with Argon2 (pwdlib) | `pwdlib[argon2]` with `PasswordHash.recommended()` |
| BACK-08 | Separate backend and frontend folders | Clear project structure: `backend/` and `frontend/` at root |
| FRNT-03 | React 19 with Vite build tool | Vite 6.2+ with React 19.2+, React Compiler auto-optimization |
| FRNT-04 | TanStack Query for server state management | `@tanstack/react-query` 5.69+ with mutations, caching |
| FRNT-05 | Zustand for client state (auth, UI) | Zustand 5.0+ with persist middleware for auth |

## Standard Stack

### Core Backend
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastAPI | 0.115+ | Async Python API framework | Native async, auto OpenAPI docs, dependency injection |
| PyJWT | 2.10+ | JWT token handling | Official library, supports HS256/RS256, expiration claims |
| pwdlib[argon2] | latest | Password hashing | FastAPI recommended, replaces bcrypt, Argon2 winner of PHC |
| Beanie | 1.29+ | Async MongoDB ODM | Built on Pydantic v2, used by Microsoft/Netflix, Motor-based |
| Motor | 3.6+ | Async MongoDB driver | Official async driver (note: deprecated May 2026, plan PyMongo Async migration) |
| python-multipart | latest | Form data parsing | Required for OAuth2 password flow |
| python-dotenv | latest | Environment variables | 12-factor app config |

### Core Frontend
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 19.2+ | UI library | React Compiler auto-optimization, Actions pattern, `use` API |
| Vite | 6.2+ | Build tool | Official CRA replacement, faster HMR, optimized builds |
| @tanstack/react-query | 5.69+ | Server state management | Caching, refetching, optimistic updates, devtools |
| Zustand | 5.0+ | Client state management | Minimal API, no context providers, excellent TypeScript |
| React Router | 7+ | Client-side routing | Data loading, nested routes, future-proof |

### Installation Commands
```bash
# Backend
pip install fastapi pyjwt "pwdlib[argon2]" beanie motor python-multipart python-dotenv uvicorn

# Frontend
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install @tanstack/react-query zustand react-router-dom
npm install -D @tanstack/react-query-devtools
```

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Beanie | Motor raw | Beanie provides Pydantic validation, migrations, cleaner API |
| Argon2 | bcrypt | Argon2 is PHC winner, more resistant to GPU attacks |
| Zustand | Redux Toolkit | Zustand is simpler, less boilerplate, no context needed |
| TanStack Query | SWR | TanStack Query has better devtools, mutations, caching |

## Architecture Patterns

### Recommended Project Structure
```
project-root/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app instance
│   │   ├── config.py            # Settings with pydantic-settings
│   │   ├── dependencies.py      # FastAPI dependencies (get_db, get_current_user)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py          # Beanie Document models
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Login, register, logout endpoints
│   │   │   └── users.py         # User profile endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── auth_service.py  # Business logic (hashing, JWT)
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── auth.py          # Pydantic request/response models
│   ├── requirements.txt
│   └── .env                     # Secrets (not committed)
├── frontend/
│   ├── src/
│   │   ├── main.tsx             # Vite entry point
│   │   ├── App.tsx              # Root component
│   │   ├── api/
│   │   │   ├── client.ts        # Axios/fetch with base URL
│   │   │   └── auth.ts          # Auth API calls
│   │   ├── stores/
│   │   │   └── authStore.ts     # Zustand auth state
│   │   ├── hooks/
│   │   │   └── useAuth.ts       # TanStack Query auth hooks
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   └── LogoutButton.tsx
│   │   │   └── layout/
│   │   │       └── Header.tsx
│   │   └── pages/
│   │       ├── Login.tsx
│   │       ├── Register.tsx
│   │       └── Home.tsx
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
└── README.md
```

### Pattern 1: FastAPI JWT with httpOnly Cookies
**What:** Store JWT in httpOnly cookie instead of localStorage for XSS protection
**When to use:** Always for web apps - required by AUTH-02
**Example:**
```python
# Source: FastAPI docs + security best practices
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # From env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

app = FastAPI()

@app.post("/auth/login")
async def login(response: Response, email: str, password: str):
    user = await authenticate_user(email, password)  # Your auth logic
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.now(timezone.utc) + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    # httpOnly cookie - not accessible via JavaScript (XSS protection)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite="lax",
        max_age=1800  # 30 minutes
    )
    return {"message": "Login successful"}

@app.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}
```

### Pattern 2: Beanie Document with Pydantic v2
**What:** Define MongoDB documents as Pydantic models with Beanie
**When to use:** All database entities in Phase 1+ - Users now, Products/Reviews later
**Example:**
```python
# Source: Beanie ODM docs
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(Document):
    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "users"  # Collection name

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    is_active: bool
    created_at: datetime
```

### Pattern 3: FastAPI Dependency Injection for Auth
**What:** Reusable dependency to get current user from JWT cookie
**When to use:** All protected endpoints
**Example:**
```python
# Source: FastAPI security docs pattern
from fastapi import Depends, HTTPException, status, Request
from jwt.exceptions import InvalidTokenError

async def get_current_user(request: Request) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = await User.get(user_id)
    if user is None:
        raise credentials_exception
    return user

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### Pattern 4: TanStack Query with FastAPI
**What:** Handle server state with caching, mutations, and automatic refetching
**When to use:** All API communication from React frontend
**Example:**
```typescript
// Source: TanStack Query docs
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,  // Important: send httpOnly cookies
})

// Query hook for current user
export function useCurrentUser() {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: async () => {
      const { data } = await api.get('/users/me')
      return data
    },
    retry: false,  // Don't retry on 401
    staleTime: 5 * 60 * 1000,  // 5 minutes
  })
}

// Mutation hook for login
export function useLogin() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (credentials: { email: string; password: string }) => {
      const { data } = await api.post('/auth/login', credentials)
      return data
    },
    onSuccess: () => {
      // Refetch current user after login
      queryClient.invalidateQueries({ queryKey: ['currentUser'] })
    },
  })
}
```

### Pattern 5: Zustand Auth Store
**What:** Minimal client state for auth UI (loading states, error messages)
**When to use:** UI state that doesn't belong in server state
**Example:**
```typescript
// Source: Zustand docs + patterns
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  // UI state only - actual auth is in httpOnly cookie
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
      partialize: (state) => ({ authMode: state.authMode }),  // Only persist mode preference
    }
  )
)
```

### Anti-Patterns to Avoid
- **Storing JWT in localStorage:** Vulnerable to XSS attacks. Always use httpOnly cookies for web apps.
- **Using bcrypt instead of Argon2:** Argon2 is the Password Hashing Competition winner, more resistant to GPU attacks.
- **Embedding user data in JWT without expiration:** Always include `exp` claim and verify it.
- **Sending credentials in URL params:** Always use request body for sensitive data.
- **Not using timing-safe comparison:** Use pwdlib's verify which is constant-time.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Password hashing | Custom hash + salt | `pwdlib[argon2]` | Argon2 is memory-hard, GPU-resistant, vetted by PHC |
| JWT handling | Custom token format | `PyJWT` | Standard format, signature verification, expiration handling |
| Session management | In-memory dict | httpOnly cookies + JWT | Stateless, scalable, XSS-resistant |
| MongoDB ODM | Raw Motor queries | Beanie | Type safety, migrations, validation, relations |
| Form validation | Manual validation | Pydantic models | Automatic validation, error messages, OpenAPI docs |
| CORS handling | Custom middleware | `CORSMiddleware` | Proper preflight, credential support, security headers |

**Key insight:** Authentication is security-critical. Using well-vetted libraries prevents vulnerabilities that could expose user data or allow account takeover.

## Common Pitfalls

### Pitfall 1: JWT Secret Too Short
**What goes wrong:** Weak secret allows brute-force attacks on JWT signature
**Why it happens:** Developer uses predictable or short secret
**How to avoid:** Generate with `openssl rand -hex 32` (produces 64 chars), store in environment variable
**Warning signs:** Secret is hardcoded in repo, secret is < 32 characters

### Pitfall 2: Missing CORS Credentials
**What goes wrong:** httpOnly cookies not sent with cross-origin requests
**Why it happens:** `allow_credentials=True` but `allow_origins=["*"]` - wildcard not allowed with credentials
**How to avoid:** Explicitly list allowed origins in CORS config, never use wildcard with credentials
**Code check:** `allow_origins=["http://localhost:5173"]` not `["*"]`

### Pitfall 3: Not Using Async MongoDB
**What goes wrong:** Blocking synchronous DB calls in async FastAPI
**Why it happens:** Using PyMongo instead of Motor
**How to avoid:** Use `AsyncMongoClient` from `pymongo` (Motor is now deprecated, PyMongo has native async)
**Note:** Motor is deprecated as of May 2026 - use PyMongo 4.9+ async API

### Pitfall 4: Timing Attack on Login
**What goes wrong:** Different response times for "user not found" vs "wrong password" reveals valid usernames
**Why it happens:** Early return when user not found skips password hash
**How to avoid:** Always run password hash verification even if user not found (use dummy hash)
```python
DUMMY_HASH = password_hash.hash("dummy")
if not user:
    password_hash.verify(password, DUMMY_HASH)  # Constant time
    return False
```

### Pitfall 5: Cookie Not Properly Configured
**What goes wrong:** Session doesn't persist across refreshes or XSS vulnerability
**Why it happens:** Missing `httponly`, `samesite`, or `secure` flags
**How to avoid:** 
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,      # Not accessible via JavaScript
    secure=True,        # HTTPS only in production
    samesite="lax",     # CSRF protection
    max_age=1800        # 30 minutes
)
```

### Pitfall 6: Not Handling Beanie Initialization
**What goes wrong:** "Document not initialized" errors
**Why it happens:** Forgot to call `init_beanie()` before using documents
**How to avoid:** Initialize in lifespan event or startup:
```python
@app.on_event("startup")
async def init_db():
    client = AsyncMongoClient("mongodb://localhost:27017")
    await init_beanie(database=client.audiophile, document_models=[User])
```

## Code Examples

### Complete User Registration Endpoint
```python
# Source: FastAPI + Beanie patterns
from fastapi import APIRouter, HTTPException, status
from beanie import Indexed
from pydantic import BaseModel, EmailStr
import jwt
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    # Check if email exists
    existing = await User.find_one(User.email == user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    existing = await User.find_one(User.username == user_data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=password_hash.hash(user_data.password)
    )
    await user.insert()
    
    return user
```

### Frontend Auth Hook Pattern
```typescript
// Source: TanStack Query + Zustand patterns
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

// Login mutation
export function useLogin() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  
  return useMutation({
    mutationFn: async (credentials: { email: string; password: string }) => {
      const { data } = await api.post('/auth/login', credentials)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['currentUser'] })
      navigate('/')
    },
  })
}

// Get current user query
export function useCurrentUser() {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: async () => {
      try {
        const { data } = await api.get('/users/me')
        return data
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 401) {
          return null  // Not authenticated
        }
        throw error
      }
    },
    retry: false,
    refetchOnWindowFocus: false,
  })
}

// Logout mutation
export function useLogout() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  
  return useMutation({
    mutationFn: async () => {
      const { data } = await api.post('/auth/logout')
      return data
    },
    onSuccess: () => {
      queryClient.setQueryData(['currentUser'], null)
      queryClient.invalidateQueries({ queryKey: ['currentUser'] })
      navigate('/')
    },
  })
}
```

### Environment Configuration
```python
# Source: pydantic-settings pattern for FastAPI
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "audiophile"
    
    # CORS
    frontend_url: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| bcrypt | Argon2 (pwdlib) | 2024-2025 | Better GPU resistance, memory-hard |
| localStorage JWT | httpOnly cookies | Ongoing | XSS protection, automatic handling |
| Motor | PyMongo Async | May 2026 | Motor deprecated, PyMongo native async |
| useContext + useReducer | Zustand | 2023-2024 | Less boilerplate, better performance |
| Redux Thunk | TanStack Query | 2022-2024 | Built-in caching, optimistic updates |
| CRA (Create React App) | Vite | 2023-2024 | Faster HMR, better DX, official replacement |

**Deprecated/outdated:**
- Motor async driver: Deprecated May 2026, migrate to PyMongo Async in v2
- bcrypt alone: Use pwdlib with Argon2
- JWT in localStorage: Use httpOnly cookies
- forwardRef: React 19 supports ref as prop

## Open Questions

1. **Beanie vs Raw PyMongo Async**
   - What we know: Beanie provides Pydantic validation, migrations, relations
   - What's unclear: Performance overhead vs raw queries
   - Recommendation: Use Beanie for all CRUD, raw aggregation for complex queries

2. **React 19 Server Components**
   - What we know: React 19 supports Server Components with "use server"
   - What's unclear: Integration with FastAPI (not Next.js)
   - Recommendation: Stick to Client Components for v1, simpler with FastAPI

3. **PyMongo Async Migration Path**
   - What we know: Motor deprecated May 2026
   - What's unclear: Exact Beanie compatibility timeline
   - Recommendation: Use Beanie now, monitor for PyMongo Async support

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8+ with pytest-asyncio |
| Config file | `backend/pytest.ini` or `pyproject.toml` |
| Quick run command | `pytest backend/tests/ -x -v` |
| Full suite command | `pytest backend/tests/ -v --cov=app` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AUTH-01 | User registration with validation | unit | `pytest tests/test_auth.py::test_register -x` | ❌ Wave 0 |
| AUTH-01 | Email uniqueness check | unit | `pytest tests/test_auth.py::test_register_duplicate_email -x` | ❌ Wave 0 |
| AUTH-02 | Login with valid credentials | unit | `pytest tests/test_auth.py::test_login_success -x` | ❌ Wave 0 |
| AUTH-02 | JWT cookie set with httpOnly | unit | `pytest tests/test_auth.py::test_login_sets_cookie -x` | ❌ Wave 0 |
| AUTH-03 | Logout clears cookie | unit | `pytest tests/test_auth.py::test_logout_clears_cookie -x` | ❌ Wave 0 |
| AUTH-04 | Session expires after 30min | integration | `pytest tests/test_auth.py::test_token_expiration -x` | ❌ Wave 0 |
| BACK-01 | FastAPI async endpoints | unit | `pytest tests/test_main.py -x` | ❌ Wave 0 |
| BACK-02 | MongoDB connection with Beanie | integration | `pytest tests/test_db.py -x` | ❌ Wave 0 |
| FRNT-03 | Vite dev server starts | smoke | `cd frontend && npm run dev` (manual) | ❌ Wave 0 |
| FRNT-04 | TanStack Query hooks work | integration | `npm test` (vitest) | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/test_{module}.py -x -v` (target: < 10s)
- **Per wave merge:** `pytest tests/ -v --cov=app` (target: < 60s)
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/conftest.py` - shared fixtures (async client, test DB)
- [ ] `backend/tests/test_auth.py` - covers AUTH-01, AUTH-02, AUTH-03
- [ ] `backend/tests/test_db.py` - covers BACK-02
- [ ] `frontend/src/test/setup.ts` - vitest configuration
- [ ] Framework install: `pip install pytest pytest-asyncio httpx` (backend), `npm install -D vitest @testing-library/react` (frontend)

## Sources

### Primary (HIGH confidence)
- FastAPI OAuth2 JWT Tutorial (fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) - JWT with password hashing, Bearer tokens
- FastAPI CORS Middleware (fastapi.tiangolo.com/tutorial/cors/) - Credential handling with specific origins
- PyJWT Documentation (pyjwt.readthedocs.io) - Token encoding/decoding, expiration claims
- Beanie ODM (beanie-odm.dev) - Document models, initialization, async patterns
- React 19 Release Notes (react.dev/blog/2024/12/05/react-19) - Actions, use hook, ref as prop
- Vite Documentation (vitejs.dev/guide/) - Project scaffolding, dev server, build
- TanStack Query Quick Start (tanstack.com/query) - useQuery, useMutation patterns
- Zustand GitHub (github.com/pmndrs/zustand) - Store creation, middleware, TypeScript

### Secondary (MEDIUM confidence)
- FastAPI Full Stack Template - Project structure patterns
- MongoDB Schema Design Anti-patterns - Embedding vs referencing (from research/SUMMARY.md)
- pwdlib Documentation - Argon2 recommended settings

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All libraries are production-proven with official documentation
- Architecture: HIGH - Patterns from official docs and community best practices
- Pitfalls: HIGH - From official security guides and common mistakes documentation

**Research date:** March 23, 2026
**Valid until:** 30 days (stable stack, low churn expected)

**Updates needed:**
- Monitor PyMongo Async support in Beanie for Motor deprecation
- React 19 ecosystem maturing (March 2026) - patterns stable
