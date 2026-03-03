from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.billing_service import create_invoice
from app.models import Product
from app.models import Denomination

## this for mail sending
from fastapi import BackgroundTasks
from app.services.email_service import send_invoice_email


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def billing_page(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse(
        "billing_form.html",
        {"request": request, "products": products}
    )



@router.post("/generate")
# async def generate_bill(request: Request, db: Session = Depends(get_db)):
async def generate_bill(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):


    form = await request.form()

    email = form.get("email")
    paid_amount = float(form.get("paid_amount"))

    # ✅ 1. STORE / UPDATE DENOMINATIONS FIRST
    denomination_values = [500, 50, 20, 10, 5, 2, 1]


    for value in denomination_values:
        # count = int(form.get(f"denom_{value}", 0))
        raw_value = form.get(f"denom_{value}")
        count = int(raw_value) if raw_value and raw_value.strip() != "" else 0


        denom = db.query(Denomination).filter_by(value=value).first()

        if not denom:
            denom = Denomination(value=value, available_count=count)
            db.add(denom)
        else:
            denom.available_count = count

    db.commit()

    # ✅ 2. PARSE PRODUCTS
    items = []
    index = 0

    while form.get(f"product_id_{index}"):
        items.append({
            "product_id": form.get(f"product_id_{index}"),
            "quantity": int(form.get(f"quantity_{index}"))
        })
        index += 1

    # ✅ 3. CREATE INVOICE (this will use greedy algorithm)
    invoice, breakdown = create_invoice(db, email, items, paid_amount)

    # Async email sending
    background_tasks.add_task(send_invoice_email, email, invoice)


    #  reload invoice with relationships
    invoice = db.query(type(invoice)) \
                .filter(type(invoice).id == invoice.id) \
                .first()

    return templates.TemplateResponse(
        "invoice_result.html",
        {
            "request": request,
            "invoice": invoice,
            "items": invoice.items,
            "breakdown": breakdown
        }
    )
