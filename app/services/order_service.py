from dataclasses import asdict

from flask import current_app
from sqlalchemy.orm import Session, Query
from app.models import Order, OrderStatus, OrderPayment, UserModel, Products
from app.models.order_product_model import OrderProduct
from .query_service import retrieve_by_id


def retrieve_orders_admin():
    session: Session = current_app.db.session

    orders = session.query(Order).all()

    list_orders = []
    for order in orders:
        mapped_order = {**asdict(order), "user": order.user, "total": order.total}
        list_orders.append(mapped_order)

    return list_orders


def retrieve_orders_detail(id):

    session = current_app.db.session

    order_product_query: Query = (
        session.query(
            OrderProduct.total,
            OrderProduct.product_quantity,
            Products.name,
        )
        .select_from(Order)
        .join(OrderProduct)
        .join(Products)
        .filter(Order.id == id)
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
