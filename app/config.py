import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ollama 설정
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    # DEFAULT_MODEL: str = "llama3"
    DEFAULT_MODEL: str = "gemma3:4b-it-qat"
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # GPU 설정
    USE_MPS: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()