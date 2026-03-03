from sqlalchemy import Column, Integer
from app.database import Base

class Denomination(Base):
    __tablename__ = "denominations"

    id = Column(Integer, primary_key=True)
    value = Column(Integer, unique=True)
    available_count = Column(Integer)
