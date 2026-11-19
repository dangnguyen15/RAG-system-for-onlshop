
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# -------------------------
# Customer
# -------------------------

class CustomerCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    phone: str | None = None
    address: str | None = None


class CustomerRead(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone: str | None
    address: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Category
# -------------------------

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None


# -------------------------
# Product
# -------------------------

class ProductCreate(BaseModel):
    category_id: UUID | None = None
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    price: Decimal = Field(ge=0)
    stock_quantity: int = Field(ge=0)


class ProductRead(BaseModel):
    id: UUID
    category_id: UUID | None
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Order
# -------------------------

class OrderRead(BaseModel):
    id: UUID
    customer_id: UUID
    order_code: str
    total_amount: Decimal
    order_status: str
    shipping_address: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Chat
# -------------------------

class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1)


class ChatMessageRead(BaseModel):
    id: UUID
    session_id: UUID
    sender: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Knowledge Document
# -------------------------

class KnowledgeDocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    source: str | None = None
    visibility: str = "PUBLIC"
    document_type: str | None = None
    owner_customer_id: UUID | None = None


class KnowledgeDocumentRead(BaseModel):
    id: UUID
    title: str
    source: str | None
    visibility: str
    document_type: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
