"""Configuration management for the Resource Allocation AI System."""
import os
from typing import Any, Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application info
    PROJECT_NAME: str = "Resource Allocation AI System"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database/resource_allocation.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-for-development-only")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "11520"))  # 8 days

    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000", "http://localhost"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create a global settings instance
settings = Settings()
