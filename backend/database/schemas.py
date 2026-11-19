
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


# =========================================================
# CUSTOMER SCHEMAS
# =========================================================

class CustomerCreate(BaseModel):

    full_name: str = Field(
        min_length=1,
        max_length=150
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        max_length=20
    )

    address: Optional[str] = None


class CustomerRead(BaseModel):

    id: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# PRODUCT SCHEMAS
# =========================================================

class ProductCreate(BaseModel):

    category_id: str

    product_name: str = Field(
        min_length=1,
        max_length=200
    )

    description: Optional[str] = None

    price: Decimal = Field(
        ge=0
    )

    stock_quantity: int = Field(
        ge=0
    )


class ProductRead(BaseModel):

    id: str
    category_id: str
    product_name: str
    description: Optional[str] = None
    price: Decimal
    stock_quantity: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# ORDER SCHEMAS
# =========================================================

class OrderItemRead(BaseModel):

    id: str
    product_id: Optional[str] = None
    product_name_snapshot: str
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class OrderRead(BaseModel):

    id: str
    order_code: str
    customer_id: str
    status: str
    total_amount: Decimal
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# KNOWLEDGE DOCUMENT SCHEMAS
# =========================================================

class KnowledgeDocumentCreate(BaseModel):

    title: str

    content: str

    visibility: str = "PUBLIC"

    owner_customer_id: Optional[str] = None


class KnowledgeDocumentRead(BaseModel):

    id: str
    title: str
    visibility: str
    owner_customer_id: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# CHAT MESSAGE SCHEMAS
# =========================================================

class ChatMessageRead(BaseModel):

    id: str

    session_id: str

    sender: str

    content: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# AUTHENTICATION SCHEMAS
# =========================================================

class LoginRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=128
    )


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"

    expires_in: int

    customer_id: str


# =========================================================
# CHAT SESSION SCHEMAS
# =========================================================

class ChatSessionCreate(BaseModel):

    session_title: Optional[str] = Field(
        default=None,
        max_length=200
    )


class ChatSessionRead(BaseModel):

    id: str

    customer_id: str

    session_title: Optional[str] = None

    is_active: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# CHAT REQUEST SCHEMAS
# =========================================================

class ChatMessageRequest(BaseModel):

    content: str = Field(
        min_length=1,
        max_length=2000
    )


# =========================================================
# CHAT RESPONSE SCHEMAS
# =========================================================

class ChatTurnResponse(BaseModel):

    session_id: str

    user_message: ChatMessageRead

    assistant_message: ChatMessageRead
