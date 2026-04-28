from dataclasses import dataclass
from datetime import datetime

from external.db import (
    get_order,
    get_product,
    update_order_status,
    update_product_stock,
    save_refund,
    generate_id,
    Refund,
    RefundLineItem,
)


VAT_RATE = 0.19


@dataclass
class RefundItem:
    product_id: str
    quantity: int


def process_refund(order_id: str, items: list[RefundItem]) -> Refund:
    order = get_order(order_id)

    if order.status != "confirmed":
        raise ValueError(f"Order {order_id} cannot be refunded (status: {order.status})")

    order_items_by_product = {item.product_id: item for item in order.items}

    refund_line_items: list[RefundLineItem] = []
    for item in items:
        order_item = order_items_by_product.get(item.product_id)
        if order_item is None:
            raise ValueError(f"Product {item.product_id} not in order {order_id}")
        if item.quantity > order_item.quantity:
            raise ValueError(
                f"Refund quantity {item.quantity} exceeds ordered quantity "
                f"{order_item.quantity} for product {item.product_id}"
            )
        refund_line_items.append(
            RefundLineItem(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=order_item.unit_price,
            )
        )

    refund_subtotal = sum(item.unit_price * item.quantity for item in refund_line_items)
    refund_vat = round(refund_subtotal * VAT_RATE, 2)
    refund_total = refund_subtotal + refund_vat

    refund = Refund(
        id=generate_id(),
        order_id=order_id,
        items=refund_line_items,
        subtotal=refund_subtotal,
        vat=refund_vat,
        total=refund_total,
        created_at=datetime.now(),
    )

    save_refund(refund)
    update_order_status(order_id, "refunded")

    for item in refund_line_items:
        product = get_product(item.product_id)
        update_product_stock(product.id, product.stock + item.quantity)

    return refund
