from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Security settings
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database settings
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "audiophile"
    
    # CORS settings
    frontend_url: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Uses lru_cache to avoid reloading settings on every request.
    """
    return Settings()
