from dataclasses import asdict

from flask import current_app
from sqlalchemy.orm import Session, Query
from sqlalchemy import func

from app.models import Order, OrderStatus, OrderPayment, UserModel, Products
from app.models.order_product_model import OrderProduct
from .query_service import retrieve_by_id
from app.models.exception_model import OrderKeysError


def retrieve_orders_admin():
    session: Session = current_app.db.session

    orders = session.query(Order).all()

    list_orders = []
    for order in orders:
        mapped_order = {
            "id": order.id,
            "status": order.status.type,
            "user": order.user,
            "total": order.total,
        }
        list_orders.append(mapped_order)

    return list_orders


def retrieve_orders_detail(id):

    session = current_app.db.session

    order_product_query: Query = (
        session.query(
            Products.name,
            Products.img,
            func.sum(OrderProduct.sale_value).label("sale_value"),
            func.count(Products.name).label("quantity"),
        )
        .select_from(Order)
        .join(OrderProduct)
        .join(Products)
        .filter(Order.id == id)
        .group_by(Products.name, OrderProduct.sale_value, Products.img)
        .all()
    )

    user_query: Query = (
        session.query(
            UserModel.name,
            UserModel.email,
            Order.id,
            Order.total,
            OrderStatus.type.label("status"),
            OrderPayment.type.label("payment"),
        )
        .select_from(Order)
        .join(UserModel)
        .join(OrderStatus)
        .join(OrderPayment)
        .filter(Order.id == id)
        .first()
    )

    order_user = user_query._asdict()
    orders_products = [item._asdict() for item in order_product_query]

    response = {**order_user, "products": orders_products}

    return response


def retrieve_orders_user():
    session: Session = current_app.db.session

    orders = session.query(Order).all()

    list_orders = [
        {"id": order.id, "status": order.status.type, "payment": order.payment.type}
        for order in orders
    ]

    return list_orders


def retrieve_orders_detail_user():
    session = current_app.db.session

    order_product_query: Query = (
        session.query(
            OrderProduct.sale_value,
            OrderProduct.id,
            Products.name,
        )
        .select_from(Order)
        .join(OrderProduct)
        .join(Products)
        .filter(Order.id == id)
        .all()
    )


def validate_order_keys(order_data: dict):
    valid_keys = ["payment", "products", "total"]

    wrong_keys = [key for key in list(order_data.keys()) if key not in valid_keys]

    if wrong_keys:
        raise OrderKeysError(wrong_keys, valid_keys)

    missing_keys = [key for key in valid_keys if key not in list(order_data.keys())]

    if missing_keys:
        raise OrderKeysError()
