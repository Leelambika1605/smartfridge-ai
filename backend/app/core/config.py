import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings loaded from environment variables or .env file.
    Follows 12-factor application design principles for seamless cloud deployment.
    """
    PROJECT_NAME: str = "SmartFridge AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = "smartfridge_ai_super_secret_jwt_key_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/smartfridge_db"
    SQLITE_FALLBACK_URL: str = "sqlite:///./smartfridge_dev.db"
    USE_SQLITE_FALLBACK_IF_PG_UNAVAILABLE: bool = True

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str) -> str:
        """
        Normalize database URLs from cloud providers like Render, Supabase, and Railway.
        Converts 'postgres://' or 'postgresql://' to 'postgresql+psycopg2://'.
        """
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+psycopg2://", 1)
            elif v.startswith("postgresql://") and not v.startswith("postgresql+"):
                return v.replace("postgresql://", "postgresql+psycopg2://", 1)
        return v

    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://*.vercel.app",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.strip() == "*":
                return ["*"]
            if not v.startswith("["):
                return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    # Storage
    UPLOAD_DIR: str = "./uploads"

    # Simulation Modes
    SIMULATION_MODE: bool = True
    PAYMENT_PROVIDER: str = "razorpay_simulation"
    SHOPPING_PROVIDER: str = "internal_simulation"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
