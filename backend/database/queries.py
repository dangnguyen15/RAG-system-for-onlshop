
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models import (
    Customer,
    Order,
    Product,
)


# =========================================================
# PRODUCT SEARCH
# =========================================================

def search_products(
    db: Session,
    product_name: str,
    limit: int = 10
):
    """
    Tìm kiếm sản phẩm theo tên.
    """

    statement = (
        select(Product)
        .where(
            Product.is_active.is_(True),
            Product.name.ilike(f"%{product_name}%")
        )
        .limit(limit)
    )

    return db.scalars(statement).all()


# =========================================================
# CUSTOMER ORDER LOOKUP
# =========================================================

def get_customer_order(
    db: Session,
    customer_id: UUID,
    order_code: str
):
    """
    Chỉ trả về đơn hàng thuộc customer_id được truyền vào.

    customer_id phải được lấy từ phiên đăng nhập đã xác thực,
    không lấy trực tiếp từ nội dung người dùng chat.
    """

    statement = (
        select(Order)
        .where(
            Order.customer_id == customer_id,
            Order.order_code == order_code
        )
    )

    return db.scalar(statement)


# =========================================================
# CUSTOMER LOOKUP
# =========================================================

def get_customer_by_email(
    db: Session,
    email: str
):
    statement = select(Customer).where(
        Customer.email == email
    )

    return db.scalar(statement)
