from datetime import datetime as dt
from http import HTTPStatus

from flask import jsonify, request
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required
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
)
from app.services.order_service import retrieve_orders_admin


@jwt_required()
def create_order():
    jwt_user = get_jwt_identity()
    data = request.get_json()

    try:
        validate_order_keys(data)
    except OrderKeysError as error:
        return {
            "error": error.message,
            "wrong_keys": error.invalid_keys,
            "expected_keys": error.expected_keys,
        }, error.status_code

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    session = db.session
    payment = data["payment"]

    status: OrderStatus = (
        session.query(OrderStatus).filter_by(type="Aguardando").first()
    )
    query_payment: OrderPayment = session.query(OrderPayment).filter_by(
        type=payment.tile()
    )

    data["status_id"] = status.id
    data["payment_id"] = query_payment.id
    data["user_id"] = user.id

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

    for product in list_products:
        new_data = {
            "order_id": new_order.id,
            "product_id": product["id"],
            "sale_value": product["sub_total"],
        }
        order_product = OrderProduct(**new_data)
        session.add(order_product)
        session.commit()

    order_detail = retrieve_orders_detail(new_order.id)
    return jsonify(order_detail), HTTPStatus.CREATED


def retrieve_orders():
    list_orders = retrieve_orders_admin()

    return jsonify(list_orders), HTTPStatus.OK


def retrieve_order_by_id(id: int):
    response = retrieve_orders_detail(id)

    return jsonify(response), HTTPStatus.OK


def delete_order():
    ...


def update_order(id):
    data: dict = request.get_json()
    session = db.session

    new_status = session.query(OrderStatus).filter_by(type=data["type"]).first()
    order: Order = session.query(Order).filter_by(id=id).first()

    # order.status.type = new_status.type
    # order.status.id = new_status.id

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
