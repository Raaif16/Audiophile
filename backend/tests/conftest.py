"""Test fixtures for pytest."""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from app.main import app


@pytest_asyncio.fixture
async def client():
    """Create async test client for FastAPI app.
    
    Uses LifespanManager to ensure FastAPI lifespan (startup/shutdown) runs.
    This is required for Beanie database initialization.
    """
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
