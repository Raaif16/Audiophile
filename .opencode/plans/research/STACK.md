# Technology Stack

**Project:** Audiophile Headphones Ecommerce  
**Researched:** March 23, 2026  
**Confidence:** HIGH

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| React | ^19.2.0 | Frontend UI library | Latest stable with React Compiler support, Activity API for transitions, and performance tracks. React 19 includes automatic memoization via React Compiler (no more manual useMemo/useCallback in most cases). |
| FastAPI | ^0.115.0 | Backend API framework | Modern Python framework with native Pydantic v2 support, automatic OpenAPI docs, async/await native. Standard install includes uvicorn[standard] for production. |
| MongoDB | 8.x | Document database | Flexible schema perfect for product variations (different headphones have different specs). Native JSON storage aligns with JavaScript frontend. |
| Python | 3.11+ | Backend runtime | Required for modern FastAPI features. 3.12+ recommended for latest performance improvements. |

### Database & ODM

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Beanie | ^1.29.0 | MongoDB ODM | Built on Pydantic v2 (matches FastAPI). Async-native via Motor. Type-safe document models. Built-in migrations support. Used by Microsoft, Netflix, Uber in production. |
| Motor | ^3.7.0 | Async MongoDB driver | Official MongoDB async driver. Required by Beanie for non-blocking I/O. |

### Frontend Build & Routing

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Vite | ^6.2.0 | Build tool & dev server | Official replacement for deprecated Create React App (CRA was sunset Feb 14, 2025). Lightning fast HMR, optimized production builds via Rolldown. |
| React Router | ^7.3.0 | Client-side routing | Industry standard. v7 unifies React Router and Remix. Supports data loading, actions, and nested routes. Future-proof for React 19. |

### State Management

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| TanStack Query | ^5.69.0 | Server state management | The standard for API data fetching. Caching, background refetching, optimistic updates, pagination built-in. Eliminates need for Redux for server state. |
| Zustand | ^5.0.3 | Client state management | Minimal boilerplate vs Redux. Perfect for auth state, UI state, wishlist (temporary before persistence). No Context provider wrapper hell. |

### HTTP Client

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Axios | ^1.8.0 | HTTP requests | Request/response interceptors for auth tokens. Automatic JSON parsing. Better error handling than fetch. Request cancellation support. |

### Authentication

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| PyJWT | ^2.10.0 | JWT token handling | FastAPI docs recommend for JWT. Support for HS256/RS256 algorithms. Token expiration handling. |
| pwdlib[argon2] | ^0.2.0 | Password hashing | Modern replacement for passlib. Argon2 is the winner of the Password Hashing Competition. Resistant to GPU/ASIC attacks. FastAPI official docs recommend this over bcrypt for new projects. |
| python-multipart | ^0.0.20 | Form data parsing | Required by FastAPI for OAuth2 password flow form handling. |

### Configuration & Utilities

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pydantic-settings | ^2.8.0 | Environment configuration | Type-safe settings management. Auto-loads from .env files. Validates on startup. Perfect for MongoDB URI, JWT secrets, etc. |
| email-validator | ^2.2.0 | Email validation | Required by FastAPI[standard] for email validation in Pydantic models. |

### File Uploads

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| python-multipart | ^0.0.20 | Multipart form parsing | Required for file uploads (product images). FastAPI UploadFile depends on this. |

### Development & Testing

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pytest | ^8.3.0 | Python testing | Industry standard. Async support via pytest-asyncio. |
| pytest-asyncio | ^0.25.0 | Async test support | Required for testing FastAPI async endpoints. |
| httpx | ^0.28.0 | Async HTTP client for testing | Required by FastAPI TestClient for making requests in tests. |
| @testing-library/react | ^16.2.0 | React component testing | Official testing approach. User-centric queries. |
| Vitest | ^3.0.0 | Vite-native test runner | Jest alternative designed for Vite. Faster, native ESM support. |

## Installation Commands

### Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Core dependencies
pip install "fastapi[standard]" beanie motor

# Authentication
pip install pyjwt "pwdlib[argon2]" python-multipart

# Configuration
pip install pydantic-settings

# Development
pip install pytest pytest-asyncio httpx
```

### Frontend

```bash
# Create Vite project (select React + TypeScript)
npm create vite@latest frontend -- --template react-ts
cd frontend

# Core dependencies
npm install react@^19.2.0 react-dom@^19.2.0
npm install react-router@^7.3.0

# State management
npm install @tanstack/react-query@^5.69.0 zustand@^5.0.3

# HTTP client
npm install axios@^1.8.0

# Development
npm install -D vitest@^3.0.0 @testing-library/react@^16.2.0
```

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Build Tool | Vite | Next.js | Next.js is overkill for this project. We don't need SSR/SSG for an admin panel and catalog. Vite gives faster dev experience and simpler configuration. |
| State Management | TanStack Query + Zustand | Redux Toolkit | Redux is overkill. TanStack Query handles server state better (caching, refetching). Zustand is simpler for client state than Redux. |
| ODM | Beanie | Motor (raw) | Raw Motor requires too much boilerplate. Beanie provides type safety and validation via Pydantic. |
| ODM | Beanie | MongoEngine | MongoEngine is synchronous and doesn't support Pydantic v2. Beanie is async-native and built for FastAPI. |
| Password Hashing | pwdlib[argon2] | bcrypt | Argon2 is more resistant to GPU attacks and is the current recommendation from the Password Hashing Competition. FastAPI docs now recommend pwdlib over passlib. |
| HTTP Client | Axios | fetch() | Axios provides interceptors (essential for auth tokens), better error handling, and request cancellation. |

## What NOT to Use

| Technology | Why Avoid | What to Use Instead |
|------------|-----------|-------------------|
| Create React App (CRA) | **Deprecated February 14, 2025**. React team officially sunset it. No longer maintained. | Vite |
| Redux | Overkill for this scope. Too much boilerplate. Server state better handled by TanStack Query. | TanStack Query + Zustand |
| Flask | Not async. Would block on database operations. Less type safety. | FastAPI |
| Mongoose (Node.js ODM) | We're using Python backend. | Beanie (Python equivalent) |
| class-transformer / class-validator | Not needed. Pydantic handles validation better. | Pydantic v2 |
| Formik | Overkill. React 19 + native validation sufficient for v1. | Native forms + React state |
| Material-UI (MUI) | Heavy bundle size. Design system conflicts with minimal aesthetic. | Tailwind CSS + custom components |

## MongoDB Schema Design Notes

For MongoDB with Beanie:

1. **Products Collection**: Store reviews as embedded documents (not separate collection) for fast reads. Use the "Computed Values" pattern to maintain rating averages.
2. **Users Collection**: Store wishlist as array of ObjectIds referencing products.
3. **Orders Collection**: Separate collection (when payment added in v2).
4. **Indexes**: Create compound indexes on `(category, price)` for filtering, `(name, description)` for text search.

## Confidence Assessment

| Technology | Confidence | Notes |
|------------|------------|-------|
| React 19 | HIGH | Official release, stable, React team endorses. |
| FastAPI | HIGH | Production-proven at Microsoft, Netflix, Uber. Well-documented. |
| Beanie | HIGH | Mature ODM, built on stable Pydantic v2. Microsoft uses it. |
| Vite | HIGH | Official CRA replacement. Industry has migrated. |
| TanStack Query | HIGH | Standard for server state. Used by most React projects. |
| pwdlib | MEDIUM-HIGH | Newer library (replaces passlib), but recommended by FastAPI docs as of late 2025. |

## Sources

- React Blog (react.dev/blog) - React 19.2, React Compiler v1.0, CRA deprecation notice
- FastAPI Documentation (fastapi.tiangolo.com) - Official tutorials, security docs
- Beanie ODM Docs (beanie-odm.dev) - Official documentation
- MongoDB Schema Design Patterns (mongodb.com/docs) - Schema design best practices
- Vite Documentation (vitejs.dev) - Build tool guidance
- TanStack Query (tanstack.com/query) - Server state management
- React Router (reactrouter.com) - Routing documentation
- FastAPI OAuth2 JWT Tutorial - Authentication patterns
