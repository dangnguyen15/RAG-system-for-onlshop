
import uuid

from typing import Optional, List

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    JSON,
    func,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.database.connection import Base


# =========================================================
# UUID HELPER
# =========================================================

def generate_uuid():
    return str(uuid.uuid4())


# =========================================================
# 1. CUSTOMERS
# =========================================================

class Customer(Base):

    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )

    address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    # Relationships

    credentials = relationship(
        "UserCredential",
        back_populates="customer",
        uselist=False
    )

    orders = relationship(
        "Order",
        back_populates="customer"
    )

    chat_sessions = relationship(
        "ChatSession",
        back_populates="customer"
    )

    knowledge_documents = relationship(
        "KnowledgeDocument",
        back_populates="owner"
    )


# =========================================================
# 2. USER_CREDENTIALS
# =========================================================

class UserCredential(Base):

    __tablename__ = "user_credentials"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    customer_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "customers.id",
            ondelete="CASCADE"
        ),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    customer = relationship(
        "Customer",
        back_populates="credentials"
    )


# =========================================================
# 3. CATEGORIES
# =========================================================

class Category(Base):

    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    name: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    products = relationship(
        "Product",
        back_populates="category"
    )


# =========================================================
# 4. PRODUCTS
# =========================================================

class Product(Base):

    __tablename__ = "products"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    category_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey(
            "categories.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    stock_quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="ck_products_price"
        ),
        CheckConstraint(
            "stock_quantity >= 0",
            name="ck_products_stock"
        ),
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )


# =========================================================
# 5. ORDERS
# =========================================================

class Order(Base):

    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    customer_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "customers.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    order_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    total_amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    order_status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
        nullable=False
    )

    shipping_address: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "total_amount >= 0",
            name="ck_orders_total_amount"
        ),
        CheckConstraint(
            "order_status IN "
            "('PENDING', 'CONFIRMED', 'PROCESSING', "
            "'SHIPPING', 'DELIVERED', 'CANCELLED')",
            name="ck_orders_status"
        ),
    )

    customer = relationship(
        "Customer",
        back_populates="orders"
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    shipments = relationship(
        "Shipment",
        back_populates="order",
        cascade="all, delete-orphan"
    )


# =========================================================
# 6. ORDER_ITEMS
# =========================================================

class OrderItem(Base):

    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    order_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "orders.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    product_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey(
            "products.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    product_name_snapshot: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "unit_price >= 0",
            name="ck_item_price"
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_item_quantity"
        ),
    )

    order = relationship(
        "Order",
        back_populates="items"
    )

    product = relationship(
        "Product",
        back_populates="order_items"
    )


# =========================================================
# 7. SHIPMENTS
# =========================================================

class Shipment(Base):

    __tablename__ = "shipments"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    order_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "orders.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    tracking_code: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    carrier: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    shipment_status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
        nullable=False
    )

    shipped_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        nullable=True
    )

    estimated_delivery: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        nullable=True
    )

    delivered_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        nullable=True
    )

    order = relationship(
        "Order",
        back_populates="shipments"
    )


# =========================================================
# 8. CHAT_SESSIONS
# =========================================================

class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    customer_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "customers.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    session_title: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    customer = relationship(
        "Customer",
        back_populates="chat_sessions"
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan"
    )


# =========================================================
# 9. CHAT_MESSAGES
# =========================================================

class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "chat_sessions.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    sender: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    metadata_json: Mapped[Optional[dict]] = mapped_column(
        "metadata",
        JSON,
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "sender IN ('USER', 'ASSISTANT', 'SYSTEM')",
            name="ck_chat_messages_sender"
        ),
    )

    session = relationship(
        "ChatSession",
        back_populates="messages"
    )


# =========================================================
# 10. KNOWLEDGE_DOCUMENTS
# =========================================================

class KnowledgeDocument(Base):

    __tablename__ = "knowledge_documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    owner_customer_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey(
            "customers.id",
            ondelete="CASCADE"
        ),
        nullable=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    source: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )

    visibility: Mapped[str] = mapped_column(
        String(20),
        default="PUBLIC",
        nullable=False
    )

    document_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "visibility IN ('PUBLIC', 'PRIVATE')",
            name="ck_documents_visibility"
        ),
        CheckConstraint(
            "(visibility = 'PUBLIC' AND owner_customer_id IS NULL) "
            "OR "
            "(visibility = 'PRIVATE' AND owner_customer_id IS NOT NULL)",
            name="ck_documents_owner_visibility"
        ),
    )

    owner = relationship(
        "Customer",
        back_populates="knowledge_documents"
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )


# =========================================================
# 11. DOCUMENT_CHUNKS
# =========================================================

class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    document_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "knowledge_documents.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[Optional[List[float]]] = mapped_column(
        JSON,
        nullable=True
    )

    metadata_json: Mapped[Optional[dict]] = mapped_column(
        "metadata",
        JSON,
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_document_chunk_index"
        ),
    )

    document = relationship(
        "KnowledgeDocument",
        back_populates="chunks"
    )
