
import base64
import hashlib
import hmac
import secrets

from datetime import datetime, timedelta

from jose import jwt, JWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database.connection import get_db
from backend.database.models import Customer


# =========================================================
# PASSWORD CONFIGURATION
# =========================================================

PASSWORD_ITERATIONS = 600000

bearer_scheme = HTTPBearer(auto_error=False)


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password: str) -> str:
    """
    Hash password using PBKDF2-HMAC-SHA256.

    Format:
    pbkdf2_sha256$iterations$salt$hash
    """

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS
    )

    salt_encoded = base64.b64encode(salt).decode("utf-8")

    hash_encoded = base64.b64encode(
        password_hash
    ).decode("utf-8")

    return (
        "pbkdf2_sha256$"
        + str(PASSWORD_ITERATIONS)
        + "$"
        + salt_encoded
        + "$"
        + hash_encoded
    )


# =========================================================
# VERIFY PASSWORD
# =========================================================

def verify_password(
    plain_password: str,
    stored_hash: str
) -> bool:

    try:

        algorithm, iterations, salt_encoded, hash_encoded = (
            stored_hash.split("$")
        )

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations)

        if iterations < 100000 or iterations > 2000000:
            return False

        salt = base64.b64decode(salt_encoded)

        expected_hash = base64.b64decode(hash_encoded)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt,
            iterations
        )

        return hmac.compare_digest(
            actual_hash,
            expected_hash
        )

    except (ValueError, TypeError):
        return False


# =========================================================
# CREATE ACCESS TOKEN
# =========================================================

def create_access_token(
    customer_id: str,
    email: str
) -> str:

    now = datetime.utcnow()

    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": customer_id,
        "email": email,
        "iat": now,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


# =========================================================
# VERIFY ACCESS TOKEN
# =========================================================

def decode_access_token(token: str) -> dict:

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        customer_id = payload.get("sub")

        if not customer_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token."
            )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"}
        )


# =========================================================
# GET CURRENT CUSTOMER
# =========================================================

def get_current_customer(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):

    if credentials is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = decode_access_token(
        credentials.credentials
    )

    customer_id = payload["sub"]

    customer = db.scalar(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.is_active.is_(True)
        )
    )

    if customer is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Customer account not found or inactive."
        )

    return customer
