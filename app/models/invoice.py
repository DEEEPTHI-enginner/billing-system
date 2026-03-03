from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    total_amount = Column(Float)
    total_tax = Column(Float)
    grand_total = Column(Float)
    paid_amount = Column(Float)
    balance_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", backref="invoices")

    items = relationship("InvoiceItem", back_populates="invoice")
