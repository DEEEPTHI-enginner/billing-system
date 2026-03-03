from app.database import SessionLocal
from app.models import Product

db = SessionLocal()

products = [
    Product(product_id="P001", name="Laptop", available_stock=10, price=50000, tax_percentage=18),
    Product(product_id="P002", name="Mouse", available_stock=50, price=500, tax_percentage=5),
    Product(product_id="P003", name="Keyboard", available_stock=30, price=1500, tax_percentage=12)
]

db.add_all(products)
db.commit()

print("Products inserted successfully!")
