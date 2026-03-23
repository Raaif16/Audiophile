from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db, close_db
from app.routers import auth_router, admin_router
from app.models import User
from app.services import hash_password


async def ensure_admin_user():
    """Ensure admin user exists on startup.
    
    Creates admin@audiophile.com user with admin123 password
    if it doesn't already exist.
    """
    admin_email = "admin@audiophile.com"
    admin_username = "admin"
    admin_password = "admin123"
    
    # Check if admin user exists
    existing_admin = await User.find_one(User.email == admin_email)
    if not existing_admin:
        # Create admin user
        admin_user = User(
            email=admin_email,
            username=admin_username,
            hashed_password=hash_password(admin_password),
            is_active=True,
            is_admin=True
        )
        await admin_user.insert()
        print(f"Admin user created: {admin_email}")
    else:
        # Ensure existing user has admin privileges
        if not existing_admin.is_admin:
            existing_admin.is_admin = True
            await existing_admin.save()
            print(f"Admin privileges granted to: {admin_email}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app.
    
    Handles database initialization on startup and cleanup on shutdown.
    Prevents "Document not initialized" errors by ensuring Beanie is ready.
    """
    # Startup: Initialize database connection
    await init_db()
    
    # Ensure admin user exists
    await ensure_admin_user()
    
    yield
    # Shutdown: Close database connection
    await close_db()


settings = get_settings()

app = FastAPI(
    title="Audiophile API",
    description="Backend API for the Audiophile Headphones Ecommerce platform",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS middleware
# CRITICAL: Use explicit frontend_url, not ["*"], when allow_credentials=True
# This is required for httpOnly cookies to work with cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],  # Explicit origin, not wildcard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Include routers
app.include_router(auth_router)
app.include_router(admin_router)
