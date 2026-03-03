from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    available_stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)
