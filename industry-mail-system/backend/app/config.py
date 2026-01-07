"""
Configuration Settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./industry_mailer.db"
    
    # News API
    NEWS_API_KEY: str
    NEWS_API_URL: str = "https://newsapi.org/v2/everything"
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your_email@gmail.com"
    SMTP_PASSWORD: str = "your_app_password"
    EMAIL_FROM: str = "your_email@gmail.com"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI (Optional - for future enhancements)
    GEMINI_API_KEY: str = ""
    # (OAuth removed) any Google OAuth config removed
    
    # Application
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
