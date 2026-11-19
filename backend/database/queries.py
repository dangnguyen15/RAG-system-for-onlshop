
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.database.models import (
    Customer,
    Order,
    Product,
)


# =========================================================
# 1. PRODUCT SEARCH
# =========================================================

def search_products(
    db: Session,
    product_name: str,
    limit: int = 10
):
    """
    Tìm sản phẩm theo tên.

    Chỉ lấy sản phẩm đang hoạt động.
    """

    if limit < 1:
        return []

    statement = (
        select(Product)
        .where(
            Product.is_active.is_(True),
            Product.name.ilike(f"%{product_name}%")
        )
        .order_by(Product.name)
        .limit(limit)
    )

    return db.scalars(statement).all()


# =========================================================
# 2. CUSTOMER ORDER LOOKUP
# =========================================================

def get_customer_order(
    db: Session,
    customer_id: str,
    order_code: str
):
    """
    Lấy đơn hàng thuộc một khách hàng cụ thể.

    customer_id phải được lấy từ phiên đăng nhập
    đã xác thực, không lấy từ nội dung chat.
    """

    statement = (
        select(Order)
        .options(
            selectinload(Order.items),
            selectinload(Order.shipments)
        )
        .where(
            Order.customer_id == customer_id,
            Order.order_code == order_code
        )
    )

    return db.scalar(statement)


# =========================================================
# 3. CUSTOMER LOOKUP
# =========================================================

def get_customer_by_email(
    db: Session,
    email: str
):
    statement = (
        select(Customer)
        .where(Customer.email == email)
    )

    return db.scalar(statement)


# =========================================================
# 4. CUSTOMER ORDER LIST
# =========================================================

def get_customer_orders(
    db: Session,
    customer_id: str,
    limit: int = 20
):
    """
    Lấy danh sách đơn hàng của một khách hàng.
    Không lấy đơn hàng của khách hàng khác.
    """

    if limit < 1:
        return []

    statement = (
        select(Order)
        .where(Order.customer_id == customer_id)
        .order_by(Order.created_at.desc())
        .limit(limit)
    )

    return db.scalars(statement).all()


# =========================================================
# 5. PRODUCT DETAIL
# =========================================================

def get_product_by_id(
    db: Session,
    product_id: str
):
    statement = (
        select(Product)
        .where(
            Product.id == product_id,
            Product.is_active.is_(True)
        )
    )

    return db.scalar(statement)
