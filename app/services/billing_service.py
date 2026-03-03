
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Product, Customer, Invoice, InvoiceItem, Denomination


def create_invoice(db: Session, email: str, items: list, paid_amount: float):

    # ✅ 1. Create or Fetch Customer
    customer = db.query(Customer).filter_by(email=email).first()
    if not customer:
        customer = Customer(email=email)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # ✅ 2. Create Invoice (initial)
    invoice = Invoice(customer_id=customer.id)
    db.add(invoice)
    db.flush()

    total_amount = 0
    total_tax = 0

    # ✅ 3. Process Products
    for item in items:
        product = db.query(Product).filter_by(product_id=item["product_id"]).first()

        if not product:
            raise HTTPException(status_code=400, detail="Invalid Product ID")

        if product.available_stock < item["quantity"]:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        # Reduce stock
        product.available_stock -= item["quantity"]

        subtotal = product.price * item["quantity"]
        tax = subtotal * (product.tax_percentage / 100)

        total_amount += subtotal
        total_tax += tax

        db.add(InvoiceItem(
            invoice_id=invoice.id,
            product_id=product.id,   # ✅ FIXED (use correct field)
            quantity=item["quantity"],
            unit_price=product.price,
            tax_percentage=product.tax_percentage,
            total_price=subtotal + tax
        ))

    grand_total = total_amount + total_tax
    balance = paid_amount - grand_total

    if balance < 0:
        raise HTTPException(status_code=400, detail="Insufficient payment")

    # ✅ 4. Update Invoice Totals
    invoice.total_amount = total_amount
    invoice.total_tax = total_tax
    invoice.grand_total = grand_total
    invoice.paid_amount = paid_amount
    invoice.balance_amount = balance

    # ✅ 5. Greedy Denomination Algorithm
    denominations = (
        db.query(Denomination)
        .order_by(Denomination.value.desc())
        .all()
    )

    breakdown = []
    remaining_balance = int(balance)

    for denom in denominations:
        if remaining_balance <= 0:
            break

        if denom.available_count <= 0:
            continue

        max_notes_needed = remaining_balance // denom.value
        notes_to_give = min(max_notes_needed, denom.available_count)

        if notes_to_give > 0:
            remaining_balance -= notes_to_give * denom.value
            denom.available_count -= notes_to_give

            breakdown.append({
                "value": denom.value,
                "count": notes_to_give
            })

    # ✅ If exact change not possible
    if remaining_balance > 0:
        raise HTTPException(
            status_code=400,
            detail="Exact change cannot be given with available denominations"
        )

    db.commit()

    return invoice, breakdown
