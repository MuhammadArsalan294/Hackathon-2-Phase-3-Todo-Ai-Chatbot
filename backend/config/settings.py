from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    NEON_DATABASE_URL: str

    # JWT settings
    BETTER_AUTH_SECRET: str

    # Auth URL (optional)
    BETTER_AUTH_URL: Optional[str] = None

    # Email settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_SENDER: str = "noreply@todopro.com"
    FRONTEND_URL: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: str = "development"

    # Optional settings for development
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()