
from decimal import Decimal

from sqlalchemy import select

from backend.database.connection import (
    SessionLocal,
    create_tables
)

from backend.database.models import (
    Customer,
    UserCredential,
    Category,
    Product,
    Order,
    OrderItem,
    Shipment,
    KnowledgeDocument,
)

from backend.security.authentication import hash_password

# =========================================================
# SEED DATABASE
# =========================================================

def seed_database():

    # Tạo database và 11 bảng nếu chưa tồn tại
    create_tables()

    db = SessionLocal()

    try:

        # -------------------------------------
        # 1. CUSTOMER
        # -------------------------------------

        customer = db.scalar(
            select(Customer).where(
                Customer.email == "customer.a@example.com"
            )
        )

        if customer is None:

            customer = Customer(
                full_name="Nguyen Van A",
                email="customer.a@example.com",
                phone="0900000001",
                address="Ho Chi Minh City"
            )

            db.add(customer)
            db.flush()

        
        # -------------------------------------
        # CUSTOMER CREDENTIALS
        # -------------------------------------

        user_credentials = db.scalar(
            select(UserCredential).where(
                UserCredential.customer_id == customer.id
            )
        )

        if user_credentials is None:

            user_credentials = UserCredential(
                customer_id=customer.id,
                password_hash=hash_password("abc@123")
            )

            db.add(user_credentials)


        # -------------------------------------
        # 2. CATEGORIES
        # -------------------------------------

        category_data = [
            ("Beverages", "Drinks and beverages"),
            ("Food", "Food and groceries"),
            ("Household", "Household products"),
        ]

        categories = {}

        for name, description in category_data:

            category = db.scalar(
                select(Category).where(
                    Category.name == name
                )
            )

            if category is None:

                category = Category(
                    name=name,
                    description=description
                )

                db.add(category)
                db.flush()

            categories[name] = category

        # -------------------------------------
        # 3. PRODUCTS
        # -------------------------------------

        product_data = [
            {
                "name": "Mineral Water 500ml",
                "description": "Bottled mineral water",
                "price": Decimal("5000"),
                "stock_quantity": 100,
                "category": "Beverages",
            },
            {
                "name": "Fresh Milk 1L",
                "description": "Fresh cow milk",
                "price": Decimal("32000"),
                "stock_quantity": 50,
                "category": "Food",
            },
            {
                "name": "Dishwashing Liquid",
                "description": "Household dishwashing liquid",
                "price": Decimal("45000"),
                "stock_quantity": 30,
                "category": "Household",
            },
        ]

        products = {}

        for item in product_data:

            product = db.scalar(
                select(Product).where(
                    Product.name == item["name"]
                )
            )

            if product is None:

                product = Product(
                    name=item["name"],
                    description=item["description"],
                    price=item["price"],
                    stock_quantity=item["stock_quantity"],
                    category_id=categories[
                        item["category"]
                    ].id
                )

                db.add(product)
                db.flush()

            products[item["name"]] = product

        # -------------------------------------
        # 4. SAMPLE ORDER
        # -------------------------------------

        order = db.scalar(
            select(Order).where(
                Order.order_code == "DH0001"
            )
        )

        if order is None:

            order = Order(
                customer_id=customer.id,
                order_code="DH0001",
                total_amount=Decimal("32000"),
                order_status="SHIPPING",
                shipping_address="Ho Chi Minh City"
            )

            db.add(order)
            db.flush()

            order_item = OrderItem(
                order_id=order.id,
                product_id=products["Fresh Milk 1L"].id,
                product_name_snapshot="Fresh Milk 1L",
                unit_price=Decimal("32000"),
                quantity=1
            )

            db.add(order_item)

            shipment = Shipment(
                order_id=order.id,
                tracking_code="TRACK0001",
                carrier="Sample Express",
                shipment_status="SHIPPING"
            )

            db.add(shipment)

        # -------------------------------------
        # 5. PUBLIC KNOWLEDGE DOCUMENT
        # -------------------------------------

        policy = db.scalar(
            select(KnowledgeDocument).where(
                KnowledgeDocument.title == "Return Policy"
            )
        )

        if policy is None:

            policy = KnowledgeDocument(
                title="Return Policy",
                source=(
                    "data/documents/policies/"
                    "return_policy.txt"
                ),
                visibility="PUBLIC",
                document_type="POLICY",
                owner_customer_id=None
            )

            db.add(policy)

        # -------------------------------------
        # COMMIT
        # -------------------------------------

        db.commit()

        print("Sample data inserted successfully.")

    except Exception as error:

        db.rollback()

        print(f"Seed error: {error}")

        raise

    finally:

        db.close()


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    seed_database()
