from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator
import secrets
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "BitPulse"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    SQLITE_DB_PATH: Path = Path("bitpulse.db")
    
    # RSS Settings
    RSS_UPDATE_INTERVAL_MINUTES: int = 30
    RSS_MAX_CONCURRENT_REQUESTS: int = 10
    RSS_REQUEST_TIMEOUT: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
    ]
    
    # Timezone
    DEFAULT_TIMEZONE: str = "Europe/Luxembourg"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 