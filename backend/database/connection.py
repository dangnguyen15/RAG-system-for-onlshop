
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import settings


# Base class cho toàn bộ ORM models
class Base(DeclarativeBase):
    pass


# Kết nối PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)


# Session dùng để thực hiện các truy vấn database
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


# Dependency cung cấp database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Kích hoạt extension pgvector
def enable_pgvector():
    with engine.begin() as connection:
        connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector")
        )


# Tạo toàn bộ bảng
def create_tables():
    # Import models để SQLAlchemy nhận diện các bảng
    from backend.database import models

    enable_pgvector()

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully.")
