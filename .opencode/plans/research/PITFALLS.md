# Ecommerce Domain Pitfalls

**Project:** Audiophile Headphones Ecommerce  
**Stack:** React (frontend) + FastAPI (backend) + MongoDB (database)  
**Researched:** March 23, 2025  
**Confidence:** HIGH (based on MongoDB official docs, FastAPI docs, React docs)

---

## Critical Pitfalls

Mistakes that cause data corruption, security vulnerabilities, or require major rewrites.

### Pitfall 1: Embedding Reviews Inside Product Documents

**What goes wrong:** Product documents grow unbounded as more reviews are added. MongoDB documents have a 16MB hard limit. Index performance degrades, and product queries slow down.

**Why it happens:** The "data that's accessed together should be stored together" principle is misapplied. Product pages do show reviews, but reviews are write-heavy and grow indefinitely.

**Consequences:**
- Document size limit exceeded (16MB hard limit)
- Query performance degrades as array grows
- Index bloat on product collection
- Cannot paginate reviews efficiently
- Difficult to query reviews by user or sort by date

**Prevention:**
```python
# WRONG: Embedding reviews in product
collection: products
{
  "_id": ObjectId,
  "name": "Headphones",
  "reviews": [  # This array grows forever!
    { "user_id": ..., "rating": 5, "text": "..." },
    # ... thousands more
  ]
}

# CORRECT: Separate reviews collection with reference
collection: products
{ "_id": ObjectId, "name": "Headphones", ... }

collection: reviews
{
  "_id": ObjectId,
  "product_id": ObjectId,  # Reference to product
  "user_id": ObjectId,
  "rating": 5,
  "text": "...",
  "created_at": ISODate,
  "verified_purchase": true
}
```

**Phase to address:** Database Schema Design (Phase 1)

**Warning signs:**
- Product documents exceeding 1MB
- Query response times increasing over time
- Need to use `$slice` to limit review array size

---

### Pitfall 2: Missing Multi-Document Transactions for Wishlist Operations

**What goes wrong:** When adding to wishlist, if the product is deleted between check and insert, or when moving items from wishlist to cart, data inconsistencies occur (orphaned references, invalid states).

**Why it happens:** MongoDB single-document operations are atomic, but operations across multiple documents are not. Without transactions, concurrent operations create race conditions.

**Consequences:**
- User has wishlist items referencing deleted products
- Wishlist count doesn't match actual items
- Duplicate items in wishlist if user double-clicks
- Inconsistent state when moving items to cart

**Prevention:**
```python
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReadConcern, WriteConcern

# Use transactions for multi-document operations
async def add_to_wishlist(user_id: str, product_id: str):
    async with await client.start_session() as session:
        async with session.start_transaction(
            read_concern=ReadConcern("snapshot"),
            write_concern=WriteConcern("majority")
        ):
            # Check product exists
            product = await db.products.find_one(
                {"_id": ObjectId(product_id)},
                session=session
            )
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            # Check not already in wishlist
            existing = await db.wishlists.find_one(
                {"user_id": user_id, "product_id": product_id},
                session=session
            )
            if existing:
                return existing
            
            # Add to wishlist
            result = await db.wishlists.insert_one(
                {
                    "user_id": user_id,
                    "product_id": product_id,
                    "added_at": datetime.utcnow()
                },
                session=session
            )
            return result
```

**Phase to address:** Wishlist Implementation (Phase 3)

**Warning signs:**
- Duplicate entries appearing in wishlists
- 404 errors when viewing wishlist items
- Count mismatches between displayed count and actual items

---

### Pitfall 3: Storing Passwords Without Proper Hashing

**What goes wrong:** Plaintext passwords or weak hashing (MD5/SHA1) expose user credentials if database is compromised.

**Why it happens:** Rolling your own auth instead of using established patterns. FastAPI makes security easy but you still need to use the right tools.

**Consequences:**
- Complete account takeover if DB leaks
- Regulatory compliance violations (GDPR, etc.)
- Reputational damage
- Credential stuffing attacks on other sites

**Prevention:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password on signup
hashed_password = pwd_context.hash(plain_password)

# Verify on login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# NEVER store plaintext or use MD5/SHA1 for passwords
```

**Phase to address:** Authentication (Phase 1)

**Warning signs:**
- Can see user passwords in database queries
- Passwords stored in predictable format
- No salt visible in password field

---

### Pitfall 4: JWT Token Security Issues

**What goes wrong:** JWT tokens with weak secrets, no expiration, or stored insecurely allow attackers to forge authentication or hijack sessions.

**Why it happens:** Copy-pasting JWT examples without understanding security requirements. Using short secrets, no token expiry, or storing tokens in localStorage.

**Consequences:**
- Session hijacking
- Privilege escalation
- Inability to revoke tokens
- XSS attacks if tokens in localStorage

**Prevention:**
```python
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Min 32 chars, from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Short-lived tokens

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Frontend: Store in httpOnly cookie, NOT localStorage
# Backend: Validate expiration and signature on every request
```

**Phase to address:** Authentication (Phase 1)

**Warning signs:**
- Tokens still work after password change
- No expiration date in token payload
- Secret key committed to git
- Using localStorage for tokens

---

### Pitfall 5: File Upload Vulnerabilities

**What goes wrong:** Malicious users upload executable files (PHP, JS) instead of images. Local file storage becomes an attack vector.

**Why it happens:** Accepting any file type, trusting filename extensions, not validating MIME types, serving files with wrong content-type.

**Consequences:**
- Remote code execution on server
- Stored XSS via SVG files
- Path traversal attacks
- Storage exhaustion (DoS)

**Prevention:**
```python
from fastapi import UploadFile, HTTPException
import magic
import uuid
from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

async def validate_and_save_image(file: UploadFile) -> str:
    # Check extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file type")
    
    # Read content
    content = await file.read()
    
    # Check size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")
    
    # Verify MIME type matches extension (magic library)
    mime = magic.from_buffer(content, mime=True)
    if mime not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(400, "File content doesn't match extension")
    
    # Generate safe filename (no user input in path)
    safe_filename = f"{uuid.uuid4()}{ext}"
    filepath = UPLOAD_DIR / safe_filename
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(content)
    
    return safe_filename

# Serve files with proper content-type and disposition
```

**Phase to address:** Product Management (Phase 2)

**Warning signs:**
- Uploaded files execute when accessed
- Can upload `.php`, `.exe`, `.js` files
- Filename contains path traversal (`../`)
- Files served with wrong MIME type

---

### Pitfall 6: Cart State Desynchronization

**What goes wrong:** Cart in React state gets out of sync with backend. User sees items in cart that don't exist, or prices that don't match.

**Why it happens:** Optimistic UI updates without proper error handling, no revalidation after backend operations, race conditions in async updates.

**Consequences:**
- User thinks they bought items that were out of stock
- Price discrepancies at checkout
- Cart persistence issues across page reloads
- Duplicate items from rapid clicks

**Prevention:**
```typescript
// React pattern: Optimistic update with rollback
const addToCart = async (productId: string) => {
  const previousCart = queryClient.getQueryData(['cart']);
  
  // Optimistic update
  queryClient.setQueryData(['cart'], (old: any) => ({
    ...old,
    items: [...old.items, { productId, quantity: 1 }]
  }));
  
  try {
    const result = await api.post('/cart/items', { productId });
    // Server response is source of truth
    queryClient.setQueryData(['cart'], result.data);
  } catch (error) {
    // Rollback on error
    queryClient.setQueryData(['cart'], previousCart);
    toast.error('Failed to add to cart');
  }
};

// Debounce rapid clicks
import { useDebounceCallback } from 'usehooks-ts';
const debouncedAdd = useDebounceCallback(addToCart, 300);
```

**Phase to address:** Shopping Cart (Phase 3)

**Warning signs:**
- Cart shows different items after refresh
- Multiple identical items from double-clicking
- "Add to cart" appears to succeed but item not saved

---

### Pitfall 7: Missing Indexes on Query Fields

**What goes wrong:** Product search, filtering, and sorting queries become slow as catalog grows. MongoDB performs collection scans instead of index lookups.

**Why it happens:** Not creating indexes on fields used in queries (search text, category, price, brand). MongoDB's flexible schema doesn't mean you don't need indexes.

**Consequences:**
- Query timeouts with large catalogs
- High CPU usage on database
- Poor user experience (slow page loads)
- Server resource exhaustion

**Prevention:**
```python
from motor.motor_asyncio import AsyncIOMotorClient

# Create indexes on startup
async def setup_indexes():
    # Text search on name and description
    await db.products.create_index([
        ("name", "text"),
        ("description", "text")
    ], name="product_text_search")
    
    # Filter fields
    await db.products.create_index("category")
    await db.products.create_index("brand")
    await db.products.create_index("price")
    await db.products.create_index([("category", 1), ("price", 1)])
    
    # Wishlist lookups
    await db.wishlists.create_index("user_id")
    await db.wishlists.create_index([("user_id", 1), ("product_id", 1)], unique=True)
    
    # Reviews
    await db.reviews.create_index("product_id")
    await db.reviews.create_index([("product_id", 1), ("created_at", -1)])
    
    # Compound index for common query patterns
    await db.products.create_index([
        ("category", 1),
        ("price", 1),
        ("rating", -1)
    ])

# Use explain() to verify index usage
# db.products.find({"category": "headphones"}).explain()
```

**Phase to address:** Product Catalog (Phase 1)

**Warning signs:**
- Queries taking >500ms with moderate data
- High CPU usage on MongoDB process
- Collection scans in explain output
- Slow page load times on product listing

---

### Pitfall 8: N+1 Query Problem in Product Listings

**What goes wrong:** Fetching product list, then making individual queries for each product's reviews, wishlist status, etc. 100 products = 100+ queries.

**Why it happens:** ORM/ODM lazy loading in loops. Not using aggregation pipeline with $lookup or not structuring data for batch fetching.

**Consequences:**
- Linear performance degradation with product count
- Database connection pool exhaustion
- Request timeouts
- Poor scalability

**Prevention:**
```python
# WRONG: N+1 queries
products = await db.products.find().to_list(100)
for product in products:
    # This makes 100 separate queries!
    reviews = await db.reviews.find({"product_id": product["_id"]}).to_list(5)
    product["reviews"] = reviews

# CORRECT: Aggregation pipeline with $lookup
pipeline = [
    {"$match": {"category": "headphones"}},
    {"$limit": 100},
    {
        "$lookup": {
            "from": "reviews",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "reviews",
            "pipeline": [
                {"$sort": {"created_at": -1}},
                {"$limit": 5}
            ]
        }
    },
    {
        "$lookup": {
            "from": "wishlists",
            "let": {"product_id": "$_id"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                {"$eq": ["$product_id", "$$product_id"]},
                                {"$eq": ["$user_id", user_id]}
                            ]
                        }
                    }
                }
            ],
            "as": "in_wishlist"
        }
    },
    {
        "$addFields": {
            "in_wishlist": {"$gt": [{"$size": "$in_wishlist"}, 0]}
        }
    }
]

products = await db.products.aggregate(pipeline).to_list(100)
```

**Phase to address:** Product Catalog (Phase 1)

**Warning signs:**
- Number of queries increases with product count
- Request time proportional to items displayed
- Connection pool exhaustion under load

---

### Pitfall 9: Missing Data Validation at API Boundary

**What goes wrong:** Invalid data reaches database because FastAPI's automatic validation is bypassed or not strict enough. Invalid ObjectIds, malformed emails, oversized text fields.

**Why it happens:** Relying only on frontend validation, not using Pydantic properly, accepting raw dicts instead of validated models.

**Consequences:**
- Database corruption
- Application crashes from unexpected data types
- Security vulnerabilities (NoSQL injection)
- Inconsistent data state

**Prevention:**
```python
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional
import re

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class ReviewCreate(BaseModel):
    product_id: PyObjectId
    rating: int = Field(..., ge=1, le=5)
    text: str = Field(..., min_length=10, max_length=2000)
    
    @validator('text')
    def validate_text(cls, v):
        # Sanitize HTML to prevent XSS
        v = re.sub(r'<[^>]+>', '', v)
        return v.strip()

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    price: float = Field(..., gt=0, le=100000)
    category: str = Field(..., regex="^(over-ear|in-ear|open-back|closed-back)$")
    brand: str = Field(..., min_length=1, max_length=100)
    
    class Config:
        json_encoders = {ObjectId: str}

# Use validated models, not raw dicts
@app.post("/reviews")
async def create_review(review: ReviewCreate, current_user: User = Depends(get_current_user)):
    # review is guaranteed to be valid here
    review_dict = review.dict()
    review_dict["user_id"] = current_user.id
    review_dict["created_at"] = datetime.utcnow()
    result = await db.reviews.insert_one(review_dict)
    return result
```

**Phase to address:** API Design (Phase 1)

**Warning signs:**
- 500 errors from database type mismatches
- Invalid ObjectIds causing crashes
- Data with missing required fields
- XSS in displayed content

---

### Pitfall 10: Race Conditions in Verified Purchase Badge

**What goes wrong:** Users can submit verified purchase reviews without actually purchasing, or the verification status is calculated incorrectly due to race conditions.

**Why it happens:** Checking order history separately from review submission creates a window for race conditions. No atomic check-and-set operation.

**Consequences:**
- Fake verified reviews
- Loss of user trust
- Gamification of review system
- Inaccurate product ratings

**Prevention:**
```python
async def create_review_with_verification(
    user_id: str,
    product_id: str,
    review_data: dict
):
    async with await client.start_session() as session:
        async with session.start_transaction():
            # Atomically check for purchase
            order = await db.orders.find_one(
                {
                    "user_id": user_id,
                    "items.product_id": product_id,
                    "status": {"$in": ["completed", "shipped", "delivered"]}
                },
                session=session
            )
            
            # Check if review already exists (prevent duplicates)
            existing = await db.reviews.find_one(
                {"user_id": user_id, "product_id": product_id},
                session=session
            )
            if existing:
                raise HTTPException(400, "Review already exists")
            
            # Create review with verified status
            review_doc = {
                "user_id": user_id,
                "product_id": product_id,
                "rating": review_data["rating"],
                "text": review_data["text"],
                "verified_purchase": order is not None,
                "created_at": datetime.utcnow()
            }
            
            result = await db.reviews.insert_one(review_doc, session=session)
            
            # Update product average rating atomically
            if order:  # Only update stats for verified purchases
                await update_product_rating(product_id, session=session)
            
            return result
```

**Phase to address:** Reviews System (Phase 2)

**Warning signs:**
- Reviews marked verified from users with no orders
- Duplicate reviews from same user
- Rating calculation discrepancies

---

## Moderate Pitfalls

### Pitfall 11: Unbounded Wishlist Growth

**What goes wrong:** Users can add unlimited items to wishlist, causing performance issues and storage bloat.

**Prevention:**
```python
MAX_WISHLIST_ITEMS = 100

async def add_to_wishlist(user_id: str, product_id: str):
    count = await db.wishlists.count_documents({"user_id": user_id})
    if count >= MAX_WISHLIST_ITEMS:
        raise HTTPException(400, "Wishlist full")
    # ... rest of logic
```

**Phase to address:** Wishlist (Phase 3)

---

### Pitfall 12: Missing Rate Limiting on Auth Endpoints

**What goes wrong:** Brute force attacks on login and password reset endpoints.

**Prevention:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginCredentials):
    # ...

@app.post("/auth/password-reset")
@limiter.limit("3/hour")
async def password_reset(request: Request, data: PasswordReset):
    # ...
```

**Phase to address:** Authentication (Phase 1)

---

### Pitfall 13: Client-Side Price Calculation

**What goes wrong:** Trusting prices sent from frontend allows users to manipulate order totals.

**Prevention:**
```python
# WRONG: Trusting client price
total = sum(item["price"] * item["quantity"] for item in request.items)

# CORRECT: Server-side price lookup
async def calculate_order_total(items: list[CartItem]):
    total = 0
    for item in items:
        product = await db.products.find_one({"_id": item.product_id})
        if not product:
            raise HTTPException(404, f"Product {item.product_id} not found")
        total += product["price"] * item.quantity  # Use DB price, not client
    return total
```

**Phase to address:** Order Management (Phase 4)

---

### Pitfall 14: No Data Pagination

**What goes wrong:** Loading all products, reviews, or orders at once causes memory and performance issues.

**Prevention:**
```python
@app.get("/products")
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None
):
    skip = (page - 1) * limit
    query = {"category": category} if category else {}
    
    products = await db.products.find(query).skip(skip).limit(limit).to_list(limit)
    total = await db.products.count_documents(query)
    
    return {
        "items": products,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }
```

**Phase to address:** API Design (Phase 1)

---

### Pitfall 15: Missing CORS Configuration

**What goes wrong:** API accepts requests from any origin, enabling CSRF attacks.

**Prevention:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# NEVER use allow_origins=["*"] with allow_credentials=True
```

**Phase to address:** API Setup (Phase 1)

---

## Phase-Specific Warnings

| Phase | Topic | Likely Pitfall | Mitigation |
|-------|-------|----------------|------------|
| Phase 1 | Auth | Weak JWT secrets | Use 32+ char random secret from env |
| Phase 1 | Auth | Tokens in localStorage | Use httpOnly cookies |
| Phase 1 | Product Schema | Embedding reviews | Separate collection with references |
| Phase 1 | Product Schema | No indexes | Create indexes on query fields |
| Phase 2 | Reviews | XSS in review text | Sanitize HTML, validate length |
| Phase 2 | Reviews | No purchase verification | Atomic transaction with orders |
| Phase 2 | Admin | No role-based access | Check admin role on admin endpoints |
| Phase 3 | Wishlist | Race conditions | Use transactions, unique index |
| Phase 3 | Wishlist | Unbounded growth | Enforce max items limit |
| Phase 4 | Images | Path traversal | Use UUID filenames, no user input |
| Phase 4 | Images | Executable uploads | Validate MIME type with magic |
| Phase 4 | Orders | Client-side pricing | Always lookup prices from DB |

---

## Detection Checklist

Before shipping each phase, verify:

- [ ] No passwords in plaintext or weak hash
- [ ] JWT tokens have expiration
- [ ] File uploads validate MIME types
- [ ] Database queries use indexes (explain())
- [ ] No N+1 query patterns
- [ ] Multi-document operations use transactions
- [ ] CORS not wildcard with credentials
- [ ] Rate limiting on auth endpoints
- [ ] Input validation on all API endpoints
- [ ] Prices calculated server-side only

---

## Sources

1. **MongoDB Schema Design Anti-Patterns** - https://www.mongodb.com/docs/manual/data-modeling/design-antipatterns/
2. **MongoDB Transactions** - https://www.mongodb.com/docs/manual/core/transactions/
3. **FastAPI Security** - https://fastapi.tiangolo.com/tutorial/security/
4. **React State Management** - https://react.dev/learn/state-a-components-memory
5. **FastAPI SQL Tutorial (patterns applicable to MongoDB)** - https://fastapi.tiangolo.com/tutorial/sql-databases/

**Confidence Notes:**
- Schema anti-patterns: HIGH (official MongoDB docs)
- Transaction usage: HIGH (official MongoDB docs)
- FastAPI security: HIGH (official FastAPI docs)
- React state: HIGH (official React docs)
- Ecommerce-specific patterns: MEDIUM (inferred from common practices, should validate with real-world testing)
