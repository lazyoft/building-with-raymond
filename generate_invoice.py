from datetime import datetime

from external.db import (
    get_order,
    get_customer,
    get_product,
    save_invoice,
    generate_id,
    Invoice,
    InvoiceLine,
)
from domain.vat import VAT_RATE


def generate_invoice(order_id: str) -> Invoice:
    order = get_order(order_id)
    customer = get_customer(order.customer_id)

    if order.status not in ("confirmed", "refunded"):
        raise ValueError(f"Cannot invoice order {order_id} (status: {order.status})")

    lines: list[InvoiceLine] = []
    for item in order.items:
        product = get_product(item.product_id)
        lines.append(
            InvoiceLine(
                product_name=product.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.unit_price * item.quantity,
            )
        )

    subtotal = sum(line.line_total for line in lines)
    vat = round(subtotal * VAT_RATE, 2)
    total = subtotal + vat

    invoice = Invoice(
        id=generate_id(),
        order_id=order_id,
        customer_name=customer.name,
        customer_email=customer.email,
        lines=lines,
        subtotal=subtotal,
        vat=vat,
        total=total,
        issued_at=datetime.now(),
    )

    save_invoice(invoice)
    return invoice
