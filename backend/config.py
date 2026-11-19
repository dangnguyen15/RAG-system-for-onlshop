
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "onlshop.db"


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "RAG System for Online Shop"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_PATH: str = str(DATABASE_PATH)

    # Authentication / JWT
    JWT_SECRET_KEY: str = "CHANGE_THIS_TO_A_RANDOM_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Qwen
    QWEN_API_KEY: str = ""
    QWEN_BASE_URL: str = ""
    QWEN_MODEL: str = "Qwen3.8-Flash"

    # Embedding
    EMBEDDING_MODEL_NAME: str = "Vietnamese_Embedding_v2"
    EMBEDDING_DIMENSION: int = 768

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()

