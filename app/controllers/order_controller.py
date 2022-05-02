from datetime import datetime as dt
from http import HTTPStatus

from flask import jsonify, request
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from app.models.exception_model import OrderKeysError
from app.services import validate_order_keys

from app.configs.database import db
from app.models import (
    Order,
    OrderPayment,
    OrderProduct,
    OrderRating,
    OrderStatus,
    UserModel,
)
from app.services import (
    retrieve,
    retrieve_by_id,
    retrieve_orders_detail,
    retrieve_orders_user,
    format_order_data,
    serialize_and_create_order_products,
)
from app.services.order_service import retrieve_orders_admin


@jwt_required()
def create_order():
    data = request.get_json()

    try:
        validate_order_keys(data)
        format_order_data(data)
    except OrderKeysError as error:
        return {
            "error": error.message,
            "wrong_keys": error.invalid_keys,
            "expected_keys": error.expected_keys,
        }, error.status_code

    session = db.session

    list_products = data.pop("products")

    try:
        new_order: Order = Order(**data)
        session.add(new_order)
        session.commit()

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            return {
                "error": e.args[0]
                .split("Key (", 1)[-1]
                .replace("(", " ")
                .replace(")", " ")
                .replace("\n", "")
            }, HTTPStatus.CONFLICT

        return e.args[0]

    serialize_and_create_order_products()
    # for product in list_products:
    #     new_data = {
    #         "order_id": new_order.id,
    #         "product_id": product["id"],
    #         "sale_value": product["sub_total"],
    #     }
    #     order_product = OrderProduct(**new_data)
    #     session.add(order_product)
    #     session.commit()

    order_detail = retrieve_orders_detail(new_order.id)
    return jsonify(order_detail), HTTPStatus.CREATED


def retrieve_orders():
    list_orders = retrieve_orders_admin()

    return jsonify(list_orders), HTTPStatus.OK


def retrieve_order_by_id(id: int):
    response = retrieve_orders_detail(id)

    return jsonify(response), HTTPStatus.OK


def delete_order(id):
    session = db.session
    order_to_delete = session.query(Order).filter(Order.id == id).first()

    orders_products_to_delete = (
        session.query(OrderProduct).filter(OrderProduct.order_id == id).all()
    )

    for order_product in orders_products_to_delete:
        session.delete(order_product)

    session.delete(order_to_delete)
    session.commit()

    return {}, HTTPStatus.NO_CONTENT


def update_order(id):
    data: dict = request.get_json()
    session = db.session

    new_status = session.query(OrderStatus).filter_by(type=data["type"]).first()
    order: Order = session.query(Order).filter_by(id=id).first()

    for key, value in data.items():
        setattr(order.status, key, value)

    session.add(order)
    session.commit()

    order_detail = retrieve_orders_detail(id)
    return jsonify(order_detail), HTTPStatus.OK


def create_order_payment():
    data = request.get_json()

    order_payment = OrderPayment(**data)

    db.session.add(order_payment)
    db.session.commit()

    return jsonify(order_payment), HTTPStatus.OK


def create_order_status():
    data = request.get_json()

    order_status = OrderStatus(**data)

    db.session.add(order_status)
    db.session.commit()

    return jsonify(order_status), HTTPStatus.OK


def create_order_rating():
    data = request.get_json()

    order_rating = OrderRating(**data)

    db.session.add(order_rating)
    db.session.commit()

    return jsonify(order_rating), HTTPStatus.OK
