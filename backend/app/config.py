from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """Application settings with environment variable validation."""
    
    # MongoDB
    mongo_uri: str
    
    # Application
    environment: str = "development"
    api_version: str = "v1"
    
    # CORS
    allowed_origins: str = "http://localhost:5173"
    
    # API Keys
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""
    
    # Logging
    log_level: str = "INFO"
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()
