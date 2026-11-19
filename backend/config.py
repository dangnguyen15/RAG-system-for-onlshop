
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Database directory
DATABASE_DIR = BASE_DIR / "database"

# SQLite database file
DATABASE_PATH = DATABASE_DIR / "onlshop.db"


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "RAG System for Online Shop"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # SQLite
    DATABASE_PATH: str = str(DATABASE_PATH)

    # Qwen LLM
    QWEN_API_KEY: str = ""
    QWEN_BASE_URL: str = ""
    QWEN_MODEL: str = "Qwen3.8-Flash"

    # Embedding
    EMBEDDING_MODEL_NAME: str = "Vietnamese_Embedding_v2"

    # Dimension phải được xác minh từ model thực tế
    EMBEDDING_DIMENSION: int = 768

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()

