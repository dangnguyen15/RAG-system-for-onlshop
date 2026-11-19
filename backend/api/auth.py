
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.connection import get_db

from backend.database.models import (
    Customer,
    UserCredential
)

from backend.database.schemas import (
    LoginRequest,
    TokenResponse
)

from backend.security.authentication import (
    verify_password,
    create_access_token
)

from backend.config import settings


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    # Find customer by email
    customer = db.scalar(
        select(Customer).where(
            Customer.email == request.email
        )
    )

    # Use generic error to avoid revealing account existence
    if customer is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Check account status
    if not customer.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer account is inactive."
        )

    # Get credentials
    credentials = db.scalar(
        select(UserCredential).where(
            UserCredential.customer_id == customer.id
        )
    )

    if credentials is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Verify password
    password_valid = verify_password(
        request.password,
        credentials.password_hash
    )

    if not password_valid:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Create JWT
    access_token = create_access_token(
        customer_id=customer.id,
        email=customer.email
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        customer_id=customer.id
    )
