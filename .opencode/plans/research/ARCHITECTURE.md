# Architecture Research: React + FastAPI + MongoDB Ecommerce

**Project:** Audiophile Headphones Ecommerce  
**Domain:** Ecommerce platform with community reviews  
**Researched:** 2025-03-23  
**Confidence:** HIGH (based on official documentation)

---

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         React Frontend                               │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
│  │  │   Pages      │  │  Components  │  │    Hooks/State           │  │    │
│  │  │  - Product   │  │  - ProductCard│  │  - useAuth               │  │    │
│  │  │  - Catalog   │  │  - ReviewList │  │  - useWishlist           │  │    │
│  │  │  - Admin     │  │  - SearchBar  │  │  - Context Providers     │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │ HTTPS/JSON
                                  ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         FastAPI Backend                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
│  │  │   Routers    │  │  Services    │  │    Dependencies          │  │    │
│  │  │  - products  │  │  - auth      │  │  - get_db                │  │    │
│  │  │  - users     │  │  - reviews   │  │  - get_current_user      │  │    │
│  │  │  - reviews   │  │  - products  │  │  - require_admin         │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │ BSON/Motor Async
                                  ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         MongoDB Database                             │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │    │
│  │  │   users     │  │  products   │  │   reviews   │  │   orders   │  │    │
│  │  │             │  │             │  │             │  │ (future)   │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘  │    │
│  │                                                                      │    │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │    │
│  │  │                    Local File Storage                            │ │    │
│  │  │              (product images - v1 only)                          │ │    │
│  │  └─────────────────────────────────────────────────────────────────┘ │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| **React Frontend** | UI rendering, client-side state, API consumption | Functional components with hooks, Axios/fetch for API |
| **FastAPI Routers** | HTTP routing, request validation, response formatting | APIRouter modules by domain (products, users, etc.) |
| **FastAPI Services** | Business logic, data transformation, external calls | Async service functions called by routers |
| **FastAPI Dependencies** | Authentication, authorization, DB session injection | `Depends()` injectables like `get_current_user` |
| **MongoDB** | Document storage, flexible schema for products/reviews | Collections with indexes for query optimization |
| **Local Storage** | Static file serving for product images | FastAPI `StaticFiles` mount |

---

## Recommended Project Structure

### Frontend (React)

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── api/                    # API client and endpoints
│   │   ├── client.js           # Axios instance with interceptors
│   │   ├── products.js         # Product API calls
│   │   ├── auth.js             # Auth API calls
│   │   ├── reviews.js          # Review API calls
│   │   └── wishlist.js         # Wishlist API calls
│   ├── components/             # Reusable UI components
│   │   ├── common/             # Button, Input, Card, etc.
│   │   ├── products/           # ProductCard, ProductGrid, FilterBar
│   │   ├── reviews/            # ReviewCard, ReviewForm, StarRating
│   │   └── layout/             # Header, Footer, Navigation
│   ├── pages/                  # Route-level components
│   │   ├── Home.jsx
│   │   ├── ProductCatalog.jsx
│   │   ├── ProductDetail.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Wishlist.jsx
│   │   └── admin/              # Admin pages
│   │       ├── Dashboard.jsx
│   │       ├── Products.jsx
│   │       └── Reviews.jsx
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAuth.js          # Authentication state
│   │   ├── useProducts.js      # Product data fetching
│   │   └── useWishlist.js      # Wishlist operations
│   ├── contexts/               # React context providers
│   │   ├── AuthContext.jsx     # User auth state
│   │   └── CartContext.jsx     # Wishlist/cart state
│   ├── utils/                  # Helper functions
│   │   ├── formatters.js       # Price formatting, date formatting
│   │   └── validators.js       # Form validation
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── vite.config.js              # or cra config
```

### Backend (FastAPI + MongoDB)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Settings and environment vars
│   ├── database.py             # MongoDB connection setup
│   ├── dependencies.py         # FastAPI dependencies (auth, db)
│   ├── routers/                # API route modules
│   │   ├── __init__.py
│   │   ├── auth.py             # Login, register, token refresh
│   │   ├── users.py            # User CRUD, profile
│   │   ├── products.py         # Product catalog, search, filters
│   │   ├── reviews.py          # Reviews with verified badges
│   │   ├── wishlist.py         # Wishlist operations
│   │   └── admin.py            # Admin-only operations
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py     # JWT token management
│   │   ├── product_service.py  # Product business logic
│   │   ├── review_service.py   # Review logic + verification
│   │   └── image_service.py    # Local file storage handling
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py             # User schemas
│   │   ├── product.py          # Product schemas
│   │   ├── review.py           # Review schemas
│   │   └── common.py           # Shared types
│   ├── core/                   # Core utilities
│   │   ├── security.py         # Password hashing, JWT
│   │   └── exceptions.py       # Custom exceptions
│   └── uploads/                # Local file storage
│       └── images/             # Product images
├── tests/
├── requirements.txt
├── pyproject.toml
└── .env
```

### Structure Rationale

- **`routers/`**: Separates API concerns by domain. Each router handles one resource type (products, users, etc.). Makes testing and maintenance easier.
- **`services/`**: Business logic isolated from HTTP layer. Allows reuse across routes and easier unit testing without HTTP overhead.
- **`models/`**: Pydantic models provide type safety, validation, and automatic OpenAPI documentation generation.
- **`dependencies.py`**: Centralized authentication and database injection using FastAPI's `Depends()` system.
- **`frontend/pages/`**: Mirrors the URL structure of the application, making navigation predictable.

---

## Architectural Patterns

### Pattern 1: Repository/Service Layer

**What:** Separate data access (repository-like) and business logic (service) from HTTP handlers.

**When to use:** Always recommended for any non-trivial application. Makes testing, refactoring, and scaling easier.

**Trade-offs:**
- **Pros:** Testable business logic, swappable data layer, clear separation
- **Cons:** More files to navigate, slight overhead for simple CRUD

**Example:**
```python
# routers/products.py
from fastapi import APIRouter, Depends
from ..services import product_service
from ..dependencies import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
async def list_products(
    category: str = None,
    db = Depends(get_db)
):
    # Service layer handles business logic
    return await product_service.get_products(db, category=category)

# services/product_service.py
async def get_products(db, category: str = None):
    query = {}
    if category:
        query["category"] = category
    # Direct MongoDB access here
    cursor = db.products.find(query)
    return await cursor.to_list(length=100)
```

### Pattern 2: Dependency Injection for Cross-Cutting Concerns

**What:** Use FastAPI's `Depends()` to inject authentication, database connections, and common parameters.

**When to use:** For auth, DB sessions, pagination, current user - anything needed across multiple endpoints.

**Trade-offs:**
- **Pros:** Clean endpoint signatures, testable via dependency overrides, automatic OpenAPI documentation
- **Cons:** Can create "magic" if overused; dependency chain can become deep

**Example:**
```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return User(**user)

async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Usage in router
@router.post("/admin/products", dependencies=[Depends(require_admin)])
async def create_product(...):
    ...
```

### Pattern 3: MongoDB Data Modeling - Embed vs Reference

**What:** MongoDB offers two ways to model relationships: embedding (nested documents) or referencing (separate collections with IDs).

**When to use:**
- **Embed** when data is accessed together (product with basic specs)
- **Reference** when data grows unbounded (reviews on product) or needs independent querying

**Trade-offs:**
- **Embed:** Single query retrieval, but document size limits (16MB), harder to update independently
- **Reference:** Flexible querying, independent updates, but requires multiple queries or $lookup

**Example - Product with Embedded Category, Referenced Reviews:**
```javascript
// products collection - embedded category (read together)
{
  _id: ObjectId("..."),
  name: "HD 800 S",
  brand: "Sennheiser",
  category: {           // Embedded - always shown with product
    type: "over-ear",
    open_back: true
  },
  specs: {              // Embedded - product details
    impedance: "300 ohm",
    frequency_response: "4-51000 Hz"
  },
  // Reviews stored separately with product_id reference
}

// reviews collection - referenced (unbounded growth, independent queries)
{
  _id: ObjectId("..."),
  product_id: ObjectId("..."),  // Reference to product
  user_id: ObjectId("..."),     // Reference to user
  rating: 5,
  content: "Amazing clarity...",
  verified_purchase: true,      // Computed field
  created_at: ISODate("...")
}
```

---

## Data Flow

### Request Flow (Product Detail Page)

```
User clicks product
       ↓
React ProductDetail component mounts
       ↓
useEffect calls productApi.getProduct(id)
       ↓
Axios GET /api/products/{id}
       ↓
FastAPI router receives request
       ↓
Dependency injection: get_db, get_current_user (optional)
       ↓
Router calls product_service.get_product(db, id)
       ↓
Service queries MongoDB: db.products.find_one({"_id": id})
       ↓
Service queries reviews: db.reviews.find({"product_id": id})
       ↓
Service aggregates data (product + reviews)
       ↓
Pydantic model validates response
       ↓
JSON response returned to frontend
       ↓
React updates state, renders product + reviews
```

### Authentication Flow

```
User submits login form
       ↓
POST /api/auth/token (OAuth2PasswordRequestForm)
       ↓
FastAPI validates credentials
       ↓
Verify password hash (Argon2 via pwdlib)
       ↓
Generate JWT access token (30 min expiry)
       ↓
Return {access_token, token_type: "bearer"}
       ↓
Frontend stores token in localStorage/context
       ↓
Subsequent requests include: Authorization: Bearer <token>
       ↓
FastAPI dependency get_current_user validates JWT
       ↓
Proceed with authenticated operation
```

### Key Data Flows

1. **Product Browsing Flow:**
   - Catalog page → GET /products?category=&search= → MongoDB query with filters → Paginated product list
   - Frontend handles filtering state, backend handles database indexing for performance

2. **Review Submission Flow:**
   - Authenticated user submits review → POST /reviews → Server validates user has product in order history → Create review with `verified_purchase` flag → Insert to reviews collection

3. **Wishlist Flow:**
   - Add to wishlist → POST /wishlist → Check if already exists → Insert user_id + product_id → Return updated wishlist → Frontend updates context

4. **Admin Product Management:**
   - Admin uploads product + images → POST /admin/products → Save images to local storage → Insert product document with image paths → Return created product

---

## Build Order Implications

Based on component dependencies, recommended build sequence:

### Phase 1: Foundation (Week 1)
1. **MongoDB connection** - Database layer required by all services
2. **Pydantic models** - Define data schemas first
3. **Basic FastAPI structure** - Routers and main.py
4. **React project setup** - Vite + routing + basic layout

### Phase 2: Core Features (Weeks 2-3)
5. **Product API** - GET endpoints for catalog (no auth needed)
6. **Product list/detail pages** - Can build UI with mock data
7. **Authentication** - JWT tokens, login/register forms
8. **User context** - Protected routes, auth state management

### Phase 3: Community Features (Week 4)
9. **Reviews API** - CRUD endpoints (requires auth for create)
10. **Review components** - Display and submission forms
11. **Verified purchase logic** - Order checking service

### Phase 4: User Features (Week 5)
12. **Wishlist API** - Add/remove/list endpoints
13. **Wishlist UI** - Page and buttons

### Phase 5: Admin (Week 6)
14. **Admin middleware** - Role-based access control
15. **Product management API** - POST/PUT/DELETE products
16. **Admin panel pages** - Product CRUD interface

### Phase 6: Polish (Week 7)
17. **Image upload handling** - Local file storage
18. **Search and filters** - MongoDB text indexes
19. **Review moderation** - Admin review management

---

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| **0-1k users** | Single FastAPI instance, local MongoDB, local file storage. No changes needed from base architecture. |
| **1k-10k users** | Add MongoDB indexes on frequently queried fields (product.category, reviews.product_id). Consider CDN for images. |
| **10k+ users** | MongoDB replica set for read scaling. Implement caching (Redis) for product catalog. Image storage → S3/cloud. |

### MongoDB Indexes to Add Early

```javascript
// Critical indexes for ecommerce queries
db.products.createIndex({ "category": 1 })
db.products.createIndex({ "brand": 1 })
db.products.createIndex({ "name": "text", "description": "text" })  // Full-text search
db.reviews.createIndex({ "product_id": 1, "created_at": -1 })  // Latest reviews first
db.reviews.createIndex({ "user_id": 1 })
db.wishlist.createIndex({ "user_id": 1, "product_id": 1 }, { unique: true })  // Prevent duplicates
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: N+1 Queries

**What people do:** Loop through products and query reviews for each one separately.

**Why it's wrong:** Database round-trip per product kills performance.

**Do this instead:** Use MongoDB's aggregation with `$lookup` or query reviews once with `$in` operator.

```python
# BAD - N+1 queries
products = await db.products.find().to_list(length=100)
for product in products:
    reviews = await db.reviews.find({"product_id": product["_id"]}).to_list(length=10)
    product["reviews"] = reviews

# GOOD - Single query
product_ids = [p["_id"] for p in products]
reviews = await db.reviews.find({"product_id": {"$in": product_ids}}).to_list(length=1000)
# Map reviews to products in Python
```

### Anti-Pattern 2: Storing Passwords in JWT

**What people do:** Include password hash or sensitive data in JWT payload.

**Why it's wrong:** JWT is signed but not encrypted. Anyone can decode and read the payload.

**Do this instead:** Store only user identifier (user_id or username) in JWT. Look up user details server-side.

```python
# BAD
jwt_payload = {"sub": user.username, "password": user.hashed_password}

# GOOD  
jwt_payload = {"sub": user.username}  # Only store identifier
# Look up user details in get_current_user dependency
```

### Anti-Pattern 3: Large Embedded Arrays

**What people do:** Embed all reviews inside product document.

**Why it's wrong:** Unbounded array growth hits 16MB document limit. Slows down all product queries.

**Do this instead:** Store reviews in separate collection with `product_id` reference.

### Anti-Pattern 4: Synchronous Database Calls

**What people do:** Use synchronous PyMongo in async FastAPI endpoints.

**Why it's wrong:** Blocks the event loop, defeats purpose of async, kills concurrency.

**Do this instead:** Use Motor (async MongoDB driver) or PyMongo Async (new in 2025).

```python
# BAD - Blocks event loop
from pymongo import MongoClient
client = MongoClient("mongodb://localhost")

# GOOD - Async
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient("mongodb://localhost")
```

### Anti-Pattern 5: Client-Side Admin Checks Only

**What people do:** Hide admin buttons in UI but don't protect API endpoints.

**Why it's wrong:** API is public; anyone can call endpoints directly.

**Do this instead:** Always validate permissions server-side with dependencies.

```python
# BAD
@app.post("/admin/products")
async def create_product(product: Product):  # Anyone can call!
    ...

# GOOD
@app.post("/admin/products", dependencies=[Depends(require_admin)])
async def create_product(product: Product):
    ...
```

---

## Integration Points

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| **Frontend ↔ Backend** | HTTPS/JSON REST API | CORS enabled for localhost dev, JWT in Authorization header |
| **Routers ↔ Services** | Direct Python function calls | Services are plain async functions, testable without HTTP |
| **Services ↔ MongoDB** | Motor async driver | Connection pool managed by Motor, inject via dependency |
| **Backend ↔ Local Files** | Python `pathlib` + FastAPI StaticFiles | Store paths in MongoDB, serve via `/uploads` endpoint |

---

## Technology Notes

### MongoDB Driver Choice

**Motor** is currently the standard async MongoDB driver for Python. However, **PyMongo Async** was released in 2025 and Motor is deprecated as of May 2026 (with critical fixes until May 2027).

**Recommendation for v1:** Use Motor for stability. Plan migration to PyMongo Async in v2.

```python
# Motor (current standard)
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient("mongodb://localhost:27017")

# PyMongo Async (future)
from pymongo import AsyncMongoClient
client = AsyncMongoClient("mongodb://localhost:27017")
```

### ODM Consideration: Beanie

**Beanie** is a popular async ODM for MongoDB with Pydantic integration. It provides:
- Type-safe document models
- Migration support
- Query builder

**Recommendation:** For v1, start with raw Motor queries for simplicity. Consider Beanie in v2 if schema complexity grows.

---

## Sources

- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) - Official FastAPI multi-file architecture
- [FastAPI OAuth2 JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) - Authentication patterns
- [MongoDB Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/) - Schema design best practices
- [MongoDB Relationships](https://www.mongodb.com/docs/manual/applications/data-models-relationships/) - Embed vs reference guidance
- [Motor Documentation](https://motor.readthedocs.io/) - Async MongoDB driver
- [React Thinking in React](https://react.dev/learn/thinking-in-react) - Component architecture patterns
- [React State](https://react.dev/learn/state-a-components-memory) - State management fundamentals

---

*Architecture research for: Audiophile Headphones Ecommerce*  
*Researched: 2025-03-23*
