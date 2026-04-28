from dataclasses import dataclass
from datetime import datetime

from external.db import (
    get_customer,
    get_products,
    save_order,
    update_product_stock,
    generate_id,
    Order,
    OrderItem,
)
from domain.vat import VAT_RATE


@dataclass
class PlaceOrderItem:
    product_id: str
    quantity: int


def place_order(customer_id: str, items: list[PlaceOrderItem]) -> Order:
    customer = get_customer(customer_id)
    products = get_products([item.product_id for item in items])

    if not customer.is_active:
        raise ValueError(f"Customer {customer_id} is not active")

    order_items: list[OrderItem] = []
    for item in items:
        product = products[item.product_id]
        if item.quantity > product.stock:
            raise ValueError(f"Insufficient stock for {product.name}")
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
            )
        )

    subtotal = sum(item.unit_price * item.quantity for item in order_items)
    vat = round(subtotal * VAT_RATE, 2)
    total = subtotal + vat

    order = Order(
        id=generate_id(),
        customer_id=customer_id,
        items=order_items,
        subtotal=subtotal,
        vat=vat,
        total=total,
        status="confirmed",
        created_at=datetime.now(),
    )

    save_order(order)

    for item in order_items:
        product = products[item.product_id]
        update_product_stock(product.id, product.stock - item.quantity)

    return order
