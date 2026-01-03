"""
Configuration settings for the Job Scam Detection API
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Model Configuration
    MODEL_PATH: str = "models/saved_models/scam_detector.pkl"
    MODEL_TYPE: str = "ensemble"
    
    # Thresholds
    SCAM_THRESHOLD_HIGH: float = 0.7
    SCAM_THRESHOLD_MEDIUM: float = 0.4
    
    # Security
    API_KEY_ENABLED: bool = False
    API_KEY: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
