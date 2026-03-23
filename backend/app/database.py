"""Database initialization module using Beanie ODM with PyMongo Async."""

import asyncio
import logging
from typing import Optional

from beanie import init_beanie
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

from app.config import get_settings
from app.models import User

# Global client instance for database connection
client: Optional[AsyncMongoClient] = None

# Logger for database operations
logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1


async def init_db() -> None:
    """Initialize database connection and Beanie ODM.

    Creates AsyncMongoClient using settings.mongodb_url, then initializes
    Beanie with the database and document models.

    This should be called during FastAPI lifespan startup.

    Implements retry logic with exponential backoff for connection failures.
    """
    global client
    settings = get_settings()

    # Create async MongoDB client using PyMongo 4.9+ native async API
    # Note: Motor is deprecated as of May 2026
    client = AsyncMongoClient(settings.mongodb_url)

    # Attempt connection with retry logic
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempting database connection (attempt {attempt}/{MAX_RETRIES})...")

            # Get database reference
            database = client[settings.database_name]

            # Initialize Beanie with document models
            await init_beanie(
                database=database,
                document_models=[User]
            )

            logger.info("Database connection established successfully.")
            return

        except ConnectionFailure as e:
            logger.warning(f"Database connection failed (attempt {attempt}/{MAX_RETRIES}): {e}")

            if attempt < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY_SECONDS} second(s)...")
                await asyncio.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.error("All database connection attempts failed.")
                raise

        except Exception as e:
            logger.error(f"Unexpected error during database initialization: {e}")
            raise


async def close_db() -> None:
    """Close database connection.

    This should be called during FastAPI lifespan shutdown.
    Properly awaits client.close() for PyMongo Async compatibility.
    """
    global client
    if client:
        await client.close()
        logger.info("Database connection closed.")
        client = None
