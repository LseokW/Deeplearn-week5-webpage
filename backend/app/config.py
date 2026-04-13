from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/callback"

    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # polar.sh
    POLAR_ACCESS_TOKEN: str = ""
    POLAR_PRODUCT_ID: str = ""
    POLAR_WEBHOOK_SECRET: str = ""
    POLAR_SUCCESS_URL: str = "http://localhost:8000/api/payment/success"

    # App
    FRONTEND_URL: str = "http://localhost:5173"
    DATABASE_URL: str = "sqlite+aiosqlite:///./deeplearn.db"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
