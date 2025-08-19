"""Application configuration settings."""

import os
from typing import List, Optional

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LaudatorAI"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: str = ""

    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Get parsed CORS origins as a list."""
        if not self.BACKEND_CORS_ORIGINS:
            return []
        if self.BACKEND_CORS_ORIGINS.startswith("["):
            import json
            return json.loads(self.BACKEND_CORS_ORIGINS)
        else:
            return [i.strip() for i in self.BACKEND_CORS_ORIGINS.split(",") if i.strip()]

    # Database Configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "laudatorai"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        # Check for Railway PostgreSQL URL
        railway_postgres_url = os.getenv("DATABASE_URL")
        if railway_postgres_url:
            return railway_postgres_url
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # File Storage Configuration
    # AWS S3 Configuration (Primary for Railway)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "laudatorai-files"
    S3_ENDPOINT_URL: Optional[str] = None  # For S3-compatible services like R2
    
    # MinIO Configuration (Fallback for local development)
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "laudatorai"
    MINIO_SECURE: bool = False
    
    @property
    def file_storage_type(self) -> str:
        """Determine which file storage to use based on environment."""
        if self.AWS_ACCESS_KEY_ID and self.AWS_SECRET_ACCESS_KEY:
            return "s3"
        return "minio"
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "openai"  # openai, ollama, huggingface
    
    # Sentry Configuration
    SENTRY_DSN: Optional[str] = None
    
    # Environment
    ENVIRONMENT: str = "production"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
