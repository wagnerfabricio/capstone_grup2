from dataclasses import asdict
from datetime import datetime as dt
from http import HTTPStatus
from flask import jsonify, request
from app.controllers.payment_controller import create_payment
from app.models import Order, OrderProduct, OrderStatus, OrderPayment, OrderRating
from app.models.user_model import UserModel
from app.models.products_model import Products
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

    list_products = data.pop("products")

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

        return e.args[0], HTTPStatus.BAD_REQUEST

    for product in list_products:
        new_data = {
            "order_id": new_order.id,
            "product_id": product["id"],
            "sale_value": product["sub_total"],
        }
        order_product = OrderProduct(**new_data)
        db.session.add(order_product)
        db.session.commit()

    payment_method = create_payment(new_order.id)

    # order_detail = retrieve_orders_detail(new_order.id)

    user = UserModel.query.get(data["user_id"])

    user_address = user.addresses[-1] if user.addresses else ""
    user_address = asdict(user_address) if user_address else ""

    order_status = OrderStatus.query.get(new_order.status_id).type

    order_products = OrderProduct.query.filter_by(order_id=new_order.id).all()

    products_list = [
        Products.query.get(product.product_id) for product in order_products
    ]

    result = {
        "user": {
            "email": user.email,
            "name": user.name,
            "id": str(user.id),
            "admin": bool(user.user_class),
            "address": f'{user_address.get("street")}, {user_address.get("number")}, Bairro: {user_address.get("district")}, Cidade: {user_address.get("city")}/{user_address.get("state")} - CEP: {user_address.get("cep")}'
            if type(user_address) is dict
            else "",
        },
        "id": str(new_order.id),
        "price": new_order.total,
        "payment": payment_method.type,
        "status": order_status,
        "detail": [
            {
                "id": str(product.id),
                "name": product.name,
                "description": product.description,
                "userId": str(user.id)
            }
            for product in products_list
        ],
    }

    return result, HTTPStatus.CREATED

    # return jsonify(order_detail), HTTPStatus.CREATED


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
