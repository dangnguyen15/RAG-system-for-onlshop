
from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


# =========================================================
# CUSTOMER
# =========================================================

class CustomerCreate(BaseModel):

    full_name: str = Field(
        min_length=1,
        max_length=150
    )

    email: EmailStr
    phone: str | None = None
    address: str | None = None


class CustomerRead(BaseModel):

    id: str
    full_name: str
    email: EmailStr
    phone: str | None
    address: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# CATEGORY
# =========================================================

class CategoryCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=120
    )

    description: str | None = None


# =========================================================
# PRODUCT
# =========================================================

class ProductCreate(BaseModel):

    category_id: str | None = None

    name: str = Field(
        min_length=1,
        max_length=200
    )

    description: str | None = None

    price: Decimal = Field(ge=0)

    stock_quantity: int = Field(ge=0)


class ProductRead(BaseModel):

    id: str
    category_id: str | None
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# ORDER
# =========================================================

class OrderRead(BaseModel):

    id: str
    customer_id: str
    order_code: str
    total_amount: Decimal
    order_status: str
    shipping_address: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# CHAT
# =========================================================

class ChatMessageCreate(BaseModel):

    content: str = Field(min_length=1)


class ChatMessageRead(BaseModel):

    id: str
    session_id: str
    sender: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# KNOWLEDGE DOCUMENT
# =========================================================

class KnowledgeDocumentCreate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=255
    )

    source: str | None = None

    visibility: str = "PUBLIC"

    document_type: str | None = None

    owner_customer_id: str | None = None


class KnowledgeDocumentRead(BaseModel):

    id: str
    title: str
    source: str | None
    visibility: str
    document_type: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
