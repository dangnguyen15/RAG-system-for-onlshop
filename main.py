
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings

from backend.database.connection import (
    create_tables
)

from backend.api.auth import router as auth_router
from backend.api.chat import router as chat_router


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Backend API for RAG System for Online Shop"
    ),
    version="1.0.0",
    debug=settings.DEBUG
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# =========================================================
# REGISTER ROUTERS
# =========================================================

app.include_router(auth_router)
app.include_router(chat_router)


# =========================================================
# STARTUP
# =========================================================

@app.on_event("startup")
def startup_event():

    create_tables()


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "application": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "database": "sqlite"
    }
