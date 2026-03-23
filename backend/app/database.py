"""Database initialization module using Beanie ODM with PyMongo Async."""

from typing import Optional

from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.config import get_settings
from app.models import User

# Global client instance for database connection
client: Optional[AsyncMongoClient] = None


async def init_db() -> None:
    """Initialize database connection and Beanie ODM.
    
    Creates AsyncMongoClient using settings.mongodb_url, then initializes
    Beanie with the database and document models.
    
    This should be called during FastAPI lifespan startup.
    """
    global client
    settings = get_settings()
    
    # Create async MongoDB client using PyMongo 4.9+ native async API
    # Note: Motor is deprecated as of May 2026
    client = AsyncMongoClient(settings.mongodb_url)
    
    # Get database reference
    database = client[settings.database_name]
    
    # Initialize Beanie with document models
    await init_beanie(
        database=database,
        document_models=[User]
    )


async def close_db() -> None:
    """Close database connection.
    
    This should be called during FastAPI lifespan shutdown.
    """
    global client
    if client:
        client.close()
        client = None
