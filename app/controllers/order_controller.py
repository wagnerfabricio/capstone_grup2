from datetime import datetime as dt
from http import HTTPStatus
from flask import jsonify, request
from app.models import Order, OrderProduct, OrderStatus, OrderPayment, OrderRating
from app.services import (
    retrieve,
    retrieve_by_id,
    retrieve_orders_detail,
    retrieve_orders_user,
)
from app.services.order_service import retrieve_orders_admin

from app.configs.database import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


from app.configs.database import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_order():
    data = request.get_json()
    list_products = data["products"]
    try:
        new_order: Order = Order(**data)
        db.session.add(new_order)
        db.session.commit()

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
        db.session.add(order_product)
        db.session.commit()

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

    print("STATUS PUXADO", new_status)
    print("ORDER", order.status)

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
