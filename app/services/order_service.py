from dataclasses import asdict

from flask import current_app
from sqlalchemy.orm import Session, Query
from sqlalchemy import func
from flask_jwt_extended import get_jwt_identity

from app.models import Order, OrderStatus, OrderPayment, UserModel, Products
from app.models.order_product_model import OrderProduct
from .query_service import retrieve_by_id
from app.models.exception_model import (
    OrderKeysError,
    IdNotFoundError,
    MissingKeysError,
    TypeFieldError,
)


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

    if not user_query:
        raise IdNotFoundError()

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


def retrieve_orders_detail_user(id):
    session = current_app.db.session

    order_query: Order = session.query(Order).filter(Order.id == id).first()

    if not order_query:
        raise IdNotFoundError()

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

    order_products = [item._asdict() for item in order_product_query]

    response = {"total": order_query.total, "products": order_products}

    return response


def validate_order_keys(order_data: dict):
    valid_keys = ["payment", "total"]

    wrong_keys = [key for key in list(order_data.keys()) if key not in valid_keys]

    if wrong_keys:
        raise OrderKeysError(wrong_keys, valid_keys)

    missing_keys = [key for key in valid_keys if key not in list(order_data.keys())]

    if missing_keys:
        raise MissingKeysError(missing_keys, list(order_data.keys()))


def format_order_data(data: dict, jwt_user):
    session = current_app.db.session
    payment = data.pop("payment")

    if not type(payment) is str:
        raise TypeFieldError("string", "payment")

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    status: OrderStatus = (
        session.query(OrderStatus).filter_by(type="Preparando").first()
    )
    query_payment: OrderPayment = (
        session.query(OrderPayment).filter_by(type=payment.title()).first()
    )

    data["status_id"] = status.id
    data["payment_id"] = query_payment.id
    data["user_id"] = user.id


def serialize_and_create_order_products(list_products, order):
    session = current_app.db.session

    for product in list_products:
        new_data = {
            "order_id": order.id,
            "product_id": product["id"],
            "sale_value": product["price"],
        }
        order_product = OrderProduct(**new_data)
        session.add(order_product)
        session.commit()


def validate_keys_update(data_keys: list):
    valid_keys = ["type"]

    wrong_keys = [key for key in data_keys if key not in valid_keys]

    if wrong_keys:
        raise OrderKeysError(wrong_keys, valid_keys)

    missing_keys = [key for key in valid_keys if key not in data_keys]

    if missing_keys:
        raise MissingKeysError(missing_keys, data_keys)


def validate_payment_keys(data_keys):
    valid_keys = ["type"]

    wrong_keys = [key for key in data_keys if key not in valid_keys]

    if wrong_keys:
        raise OrderKeysError(wrong_keys, valid_keys)

    missing_keys = [key for key in valid_keys if key not in data_keys]

    if missing_keys:
        raise MissingKeysError(missing_keys, data_keys)


def validate_status_keys(data_keys):
    valid_keys = ["status"]

    wrong_keys = [key for key in data_keys if key not in valid_keys]

    if wrong_keys:
        raise OrderKeysError(wrong_keys, valid_keys)

    missing_keys = [key for key in valid_keys if key not in data_keys]

    if missing_keys:
        raise MissingKeysError(missing_keys, data_keys)


def validate_rating_keys(data_keys):
    valid_keys = ["rating", "comment"]

    wrong_keys = [key for key in data_keys if key not in valid_keys]

    if wrong_keys:
        raise OrderKeysError(wrong_keys, valid_keys)

    missing_keys = [key for key in valid_keys if key not in data_keys]

    if missing_keys:
        raise MissingKeysError(missing_keys, data_keys)
