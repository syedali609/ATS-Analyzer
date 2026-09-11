from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume ATS Analyzer"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # CORS Configuration — local dev + Render deployed frontend
    CORS_ORIGINS: List[str] = [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://localhost:8000",
        "https://resume-ats-frontend.onrender.com",
        "https://resume-ats-backend.onrender.com",
        "https://ats-analyzer-teal.vercel.app"
    ]
    
    # Scoring Weights
    KEYWORD_SCORE_WEIGHT: float = 0.6
    FORMATTING_SCORE_WEIGHT: float = 0.4
    
    # File limits
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt"]
    
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True)

settings = Settings()