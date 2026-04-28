from external.db import (
    get_order,
    get_products,
    update_order_status,
    update_product_stock,
    Order,
)


def cancel_order(order_id: str) -> Order:
    order = get_order(order_id)
    products = get_products([item.product_id for item in order.items])

    if order.status != "confirmed":
        raise ValueError(f"Order {order_id} cannot be canceled (status: {order.status})")

    update_order_status(order_id, "canceled")

    for item in order.items:
        product = products[item.product_id]
        update_product_stock(product.id, product.stock + item.quantity)

    return order
