from dataclasses import dataclass
from datetime import date, datetime
import uuid


@dataclass
class Customer:
    id: str
    name: str
    email: str
    date_of_birth: date
    is_active: bool


@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: float


@dataclass
class Order:
    id: str
    customer_id: str
    items: list[OrderItem]
    subtotal: float
    vat: float
    total: float
    status: str
    created_at: datetime


@dataclass
class RefundLineItem:
    product_id: str
    quantity: int
    unit_price: float


@dataclass
class Refund:
    id: str
    order_id: str
    items: list[RefundLineItem]
    subtotal: float
    vat: float
    total: float
    created_at: datetime


@dataclass
class InvoiceLine:
    product_name: str
    quantity: int
    unit_price: float
    line_total: float


@dataclass
class Invoice:
    id: str
    order_id: str
    customer_name: str
    customer_email: str
    lines: list[InvoiceLine]
    subtotal: float
    vat: float
    total: float
    issued_at: datetime


CUSTOMERS: dict[str, Customer] = {}
PRODUCTS: dict[str, Product] = {}
ORDERS: dict[str, Order] = {}
REFUNDS: dict[str, Refund] = {}
INVOICES: dict[str, Invoice] = {}


def get_customer(customer_id: str) -> Customer:
    return CUSTOMERS[customer_id]


def get_product(product_id: str) -> Product:
    return PRODUCTS[product_id]


def get_products(product_ids: list[str]) -> dict[str, Product]:
    return {pid: PRODUCTS[pid] for pid in product_ids}


def get_order(order_id: str) -> Order:
    return ORDERS[order_id]


def save_order(order: Order) -> Order:
    ORDERS[order.id] = order
    return order


def update_order_status(order_id: str, status: str) -> None:
    ORDERS[order_id].status = status


def update_product_stock(product_id: str, new_stock: int) -> None:
    PRODUCTS[product_id].stock = new_stock


def save_refund(refund: Refund) -> Refund:
    REFUNDS[refund.id] = refund
    return refund


def save_invoice(invoice: Invoice) -> Invoice:
    INVOICES[invoice.id] = invoice
    return invoice


def generate_id() -> str:
    return str(uuid.uuid4())
