
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from backend.config import settings
from backend.database.connection import Base


# =========================================================
# 1. CUSTOMERS
# =========================================================

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    phone: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(Text)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    credentials = relationship(
        "UserCredential",
        back_populates="customer",
        uselist=False
    )

    orders = relationship("Order", back_populates="customer")
    chat_sessions = relationship(
        "ChatSession", back_populates="customer"
    )

    knowledge_documents = relationship(
        "KnowledgeDocument", back_populates="owner"
    )


# =========================================================
# 2. USER_CREDENTIALS
# =========================================================

class UserCredential(Base):
    __tablename__ = "user_credentials"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    customer = relationship(
        "Customer", back_populates="credentials"
    )


# =========================================================
# 3. CATEGORIES
# =========================================================

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )

    description: Mapped[str | None] = mapped_column(Text)

    products = relationship("Product", back_populates="category")


# =========================================================
# 4. PRODUCTS
# =========================================================

class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="SET NULL")
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    price: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    stock_quantity: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_products_price"),
        CheckConstraint(
            "stock_quantity >= 0",
            name="ck_products_stock"
        ),
    )

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


# =========================================================
# 5. ORDERS
# =========================================================

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    order_code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )

    total_amount: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    order_status: Mapped[str] = mapped_column(
        String(30), default="PENDING", nullable=False
    )

    shipping_address: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
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

    customer = relationship("Customer", back_populates="orders")

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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )

    product_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="SET NULL")
    )

    # Snapshot để giữ tên và giá tại thời điểm mua
    product_name_snapshot: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    __table_args__ = (
        CheckConstraint("unit_price >= 0", name="ck_item_price"),
        CheckConstraint("quantity > 0", name="ck_item_quantity"),
    )

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


# =========================================================
# 7. SHIPMENTS
# =========================================================

class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    tracking_code: Mapped[str | None] = mapped_column(
        String(100), unique=True
    )

    carrier: Mapped[str | None] = mapped_column(String(100))

    shipment_status: Mapped[str] = mapped_column(
        String(30), default="PENDING", nullable=False
    )

    shipped_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True)
    )

    estimated_delivery: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True)
    )

    delivered_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True)
    )

    order = relationship("Order", back_populates="shipments")


# =========================================================
# 8. CHAT_SESSIONS
# =========================================================

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    session_title: Mapped[str | None] = mapped_column(String(200))

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    customer = relationship(
        "Customer", back_populates="chat_sessions"
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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    sender: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    metadata_json: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "sender IN ('USER', 'ASSISTANT', 'SYSTEM')",
            name="ck_chat_messages_sender"
        ),
    )

    session = relationship(
        "ChatSession", back_populates="messages"
    )


# =========================================================
# 10. KNOWLEDGE_DOCUMENTS
# =========================================================

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    owner_customer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    source: Mapped[str | None] = mapped_column(String(500))

    visibility: Mapped[str] = mapped_column(
        String(20), default="PUBLIC", nullable=False
    )

    document_type: Mapped[str | None] = mapped_column(String(50))

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
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
        "Customer", back_populates="knowledge_documents"
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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    embedding = mapped_column(
        Vector(settings.EMBEDDING_DIMENSION),
        nullable=True
    )

    metadata_json: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_document_chunk_index"
        ),
        Index(
            "ix_document_chunks_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"}
        ),
    )

    document = relationship(
        "KnowledgeDocument", back_populates="chunks"
    )
