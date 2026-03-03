

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Customer, Invoice

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Page to search customer invoices
@router.get("/history")
def search_history_page(request: Request):
    return templates.TemplateResponse(
        "history_search.html",
        {"request": request}
    )


# Show all invoices of a customer
@router.post("/history")
async def customer_history(request: Request, db: Session = Depends(get_db)):

    form = await request.form()
    email = form.get("email")

    customer = db.query(Customer).filter_by(email=email).first()

    if not customer:
        return templates.TemplateResponse(
            "history_list.html",
            {
                "request": request,
                "email": email,
                "invoices": [],
                "message": "No customer found"
            }
        )

    invoices = db.query(Invoice).filter_by(customer_id=customer.id).all()

    return templates.TemplateResponse(
        "history_list.html",
        {
            "request": request,
            "email": email,
            "invoices": invoices,
            "message": None
        }
    )


# Show specific invoice details
@router.get("/invoice/{invoice_id}")
def view_invoice(invoice_id: int, request: Request, db: Session = Depends(get_db)):

    invoice = db.query(Invoice).filter_by(id=invoice_id).first()

    return templates.TemplateResponse(
        "invoice_details.html",
        {
            "request": request,
            "invoice": invoice
        }
    )
