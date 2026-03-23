from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app.
    
    Handles database initialization on startup and cleanup on shutdown.
    Prevents "Document not initialized" errors by ensuring Beanie is ready.
    """
    # Startup: Initialize database connection
    await init_db()
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


# Future router imports will go here:
# from app.routers import auth, users
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(users.router, prefix="/users", tags=["users"])
