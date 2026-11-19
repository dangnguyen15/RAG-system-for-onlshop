
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "RAG System for Online Shop"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # PostgreSQL
    DATABASE_URL: str = (
        "postgresql+psycopg://postgres:password@localhost:5432/onlshop_db"
    )

    # Qwen LLM
    QWEN_API_KEY: str = ""
    QWEN_BASE_URL: str = ""
    QWEN_MODEL: str = "Qwen3.8-Flash"

    # Embedding
    EMBEDDING_MODEL_NAME: str = "Vietnamese_Embedding_v2"

    # Placeholder: cần xác minh dimension thực tế của model
    EMBEDDING_DIMENSION: int = 768

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
