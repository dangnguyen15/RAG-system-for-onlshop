
from sqlalchemy import inspect, select

from backend.database.connection import (
    engine,
    SessionLocal,
    check_database_connection
)

from backend.database.models import (
    Customer,
    Product,
    Order,
    OrderItem,
    Shipment
)


# 1. Check connection
print("Database connected:", check_database_connection())


# 2. Check tables
inspector = inspect(engine)

print("\nDATABASE TABLES:")

for table in inspector.get_table_names():
    print("-", table)


# 3. Check sample data
db = SessionLocal()

try:

    print("\nCUSTOMERS:")

    customers = db.scalars(
        select(Customer)
    ).all()

    for customer in customers:
        print(customer.full_name, customer.email)

    print("\nPRODUCTS:")

    products = db.scalars(
        select(Product)
    ).all()

    for product in products:
        print(
            product.name,
            product.price,
            product.stock_quantity
        )

    print("\nORDERS:")

    orders = db.scalars(
        select(Order)
    ).all()

    for order in orders:
        print(
            order.order_code,
            order.order_status,
            order.total_amount
        )

    print("\nORDER DETAILS:")

    items = db.scalars(
        select(OrderItem)
    ).all()

    for item in items:
        print(
            item.product_name_snapshot,
            item.quantity,
            item.unit_price
        )

    print("\nSHIPMENTS:")

    shipments = db.scalars(
        select(Shipment)
    ).all()

    for shipment in shipments:
        print(
            shipment.tracking_code,
            shipment.shipment_status
        )

finally:
    db.close()
