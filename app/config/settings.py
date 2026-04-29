import os
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Gymly"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:8000",
        "https://localhost:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://localhost:5173",
        "http://localhost",
        "https://localhost",
    ]
    PROJECT_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    DB_URI: str = "sqlite:///africa-excel.db"
    EXPIRY_WARNING_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env.local", extra="ignore", case_sensitive=True
    )


settings = Settings()
