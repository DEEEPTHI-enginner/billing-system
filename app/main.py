from fastapi import FastAPI
from app.database import Base, engine
from app.routes import billing_routes, history_routes
# from app import models
from app.models import Customer, Invoice, InvoiceItem, Product, Denomination



app = FastAPI(title="Billing System")
Base.metadata.create_all(bind=engine)

app.include_router(billing_routes.router)
app.include_router(history_routes.router)