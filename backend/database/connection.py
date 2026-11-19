
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import settings


# =========================================================
# DATABASE DIRECTORY
# =========================================================

DATABASE_PATH = Path(settings.DATABASE_PATH)

DATABASE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SQLALCHEMY BASE
# =========================================================

class Base(DeclarativeBase):
    pass


# =========================================================
# SQLITE ENGINE
# =========================================================

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    echo=settings.DEBUG
)


# =========================================================
# ENABLE FOREIGN KEY CONSTRAINTS
# =========================================================

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):

    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys=ON")

    cursor.close()


# =========================================================
# SESSION
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    # Import models để SQLAlchemy nhận diện toàn bộ bảng
    from backend.database import models

    Base.metadata.create_all(bind=engine)

    print("SQLite database initialized successfully.")
    print(f"Database location: {DATABASE_PATH}")


# =========================================================
# CHECK DATABASE CONNECTION
# =========================================================

def check_database_connection():

    from sqlalchemy import text

    try:

        with engine.connect() as connection:

            connection.execute(text("SELECT 1"))

        return True

    except Exception as error:

        print(f"Database connection error: {error}")

        return False
