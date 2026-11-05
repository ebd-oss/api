from functools import lru_cache
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ENVIRONMENT: Literal["development", "test", "production"] = "development"
    DATABASE_URL: str = "sqlite:///./emergency_bangladesh.db"
    DATABASE_ENCRYPTION_KEY: str | None = None
    JWT_SECRET_KEY: str | None = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    IDENTITY_HASH_PEPPER: str | None = None
    UPLOAD_DIR: str = "./uploads"
    CORS_ORIGINS: str = "http://localhost:3000"

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.ENVIRONMENT == "production":
            missing = []
            if not self.DATABASE_ENCRYPTION_KEY:
                missing.append("DATABASE_ENCRYPTION_KEY")
            if not self.JWT_SECRET_KEY:
                missing.append("JWT_SECRET_KEY")
            if not self.IDENTITY_HASH_PEPPER:
                missing.append("IDENTITY_HASH_PEPPER")
            if missing:
                raise ValueError(f"Missing required secrets in production: {', '.join(missing)}")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
