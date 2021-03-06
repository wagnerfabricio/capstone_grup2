from dataclasses import asdict
from datetime import datetime as dt
from http import HTTPStatus
import re


from flask import jsonify, request
from app.controllers.payment_controller import create_payment
from app.models.payments_model import PaymentModel
from app.models.user_model import UserModel
from app.models.products_model import Products
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.exception_model import (
    OrderKeysError,
    MissingKeysError,
    TypeFieldError,
    UnauthorizedError,
)
from app.services import (
    validate_order_keys,
    validate_status_keys,
    validate_payment_keys,
)

from sqlalchemy import func


from app.configs.database import db
from app.models import (
    Order,
    # OrderPayment,
    OrderProduct,
    OrderRating,
    OrderStatus,
    UserModel,
    Cart,
    CartProducts,
    Products,
)
from app.services import (
    retrieve,
    retrieve_by_id,
    retrieve_orders_detail,
    retrieve_orders_user,
    format_order_data,
    serialize_and_create_order_products,
    validate_keys_update,
)
from app.services.admin_service import verify_admin_access
from app.services.order_service import (
    retrieve_orders_admin,
    retrieve_orders_detail_user,
)


@jwt_required()
def create_order():
    data = request.get_json()
    jwt_user = get_jwt_identity()
    session = db.session

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    cart = Cart.query.filter(Cart.user_id == user.id).first()

    if not cart:
        return {"error": "cart is empty"}, HTTPStatus.BAD_REQUEST

    total = (
        session.query(func.sum(Products.price))
        .select_from(CartProducts)
        .join(Products)
        .filter(CartProducts.cart_id == cart.id)
        .first()
    )

    data["total"] = total[0]

    cart_products = (
        session.query(
            Products.id,
            Products.name,
            Products.price,
        )
        .select_from(Cart)
        .join(CartProducts)
        .join(Products)
        .filter(Cart.id == cart.id)
        .all()
    )

    mapped_cart_products = [product._asdict() for product in cart_products]

    try:
        # validate_order_keys(data)
        format_order_data(data, jwt_user)
    except OrderKeysError as error:
        return {
            "error": error.message,
            "wrong_keys": error.invalid_keys,
            "expected_keys": error.expected_keys,
        }, error.status_code
    except TypeFieldError as error:
        return {"error": error.message}, error.status_code

    try:
        new_order: Order = Order(**data)
        session.add(new_order)
        session.commit()

    except TypeFieldError as error:
        return {"error": error.message}, error.status_code

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

    cart_products_to_be_deleted = (
        session.query(CartProducts).filter(CartProducts.cart_id == cart.id).all()
    )

    serialize_and_create_order_products(mapped_cart_products, new_order)

    for cart_product in cart_products_to_be_deleted:
        session.delete(cart_product)
    session.commit()

    session.delete(cart)
    session.commit()

    payment_method = create_payment(new_order.id)

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
                "userId": str(user.id),
            }
            for product in products_list
        ],
    }

    return result, HTTPStatus.CREATED


# @jwt_required()
def retrieve_orders():
    # try:
    # verify_admin_access()
    list_orders = retrieve_orders_user()

    result = []
    for order in list_orders:
        order_id = str(order.get('id'))
        order_info = retrieve_orders_detail(order_id)
        order_info['payment'] = asdict(PaymentModel.query.filter_by(order_id=order_id).first())

        if order_info:
            result.append(order_info)

    # except UnauthorizedError as e:
    #     return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED

    # return jsonify(result), HTTPStatus.OK

    return jsonify(
        [{
            "user":{
                "email": order.get('email'),
                "name": order.get('name'),
                "id": order.get('user_id'),
                "address": "",
            },
            "id": order.get('id'),
            "price": order.get('total'),
            "payment": order['payment']['type'],
            "status": order.get('status'),
            "details": order.get('products')
        } for order in result]
    ), HTTPStatus.OK


def retrieve_order_by_id(id: int):
    # response = retrieve_orders_detail_user(id)
    response = retrieve_orders_detail(id)

    if not response:
        return {"error": f"id {id} not found!"}, HTTPStatus.NOT_FOUND

    payment = PaymentModel.query.filter_by(order_id=id).first()

    payment = asdict(payment)

    if payment.get("mercadopago_id"):
        payment.pop("order_id")
        response["payment_info"] = payment

        return jsonify(response), HTTPStatus.OK

    payment.pop("mercadopago_id")
    payment.pop("mercadopago_type")

    response["payment_info"] = payment

    return jsonify(response), HTTPStatus.OK


def delete_order(order_id):
    session = db.session
    order_to_delete = session.query(Order).filter(Order.id == order_id).first()

    if not order_to_delete:
        return {"error": f"id {order_id} not found!"}, HTTPStatus.NOT_FOUND

    orders_products_to_delete = (
        session.query(OrderProduct).filter(OrderProduct.order_id == order_id).all()
    )

    for order_product in orders_products_to_delete:
        session.delete(order_product)

    session.delete(order_to_delete)
    session.commit()

    return {}, HTTPStatus.NO_CONTENT


def update_order(order_id):
    data: dict = request.get_json()
    session = db.session

    try:
        validate_keys_update(list(data.keys()))
    except OrderKeysError as error:
        return {
            "error": error.message,
            "invalid_keys": error.invalid_keys,
            "expected_keys": error.expected_keys,
        }, error.status_code
    except MissingKeysError as error:
        return {
            "error": error.message,
            "missing_keys": error.missing_keys,
            "received_keys": error.received_keys,
        }, error.status_code

    new_status = session.query(OrderStatus).filter_by(type=data["type"]).first()
    order: Order = session.query(Order).filter_by(id=order_id).first()

    if not order:
        return {"error": f"id {order_id} not found!"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(order.status, key, value)

    session.add(order)
    session.commit()

    order_detail = retrieve_orders_detail(order_id)
    return jsonify(order_detail), HTTPStatus.OK


@jwt_required()
def create_order_status():
    data = request.get_json()
    try:
        verify_admin_access()
        validate_status_keys(list(data.keys()))
        order_status = OrderStatus(**data)
        db.session.add(order_status)
        db.session.commit()

    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED

    except OrderKeysError as error:
        return {
            "error": error.message,
            "invalid_keys": error.invalid_keys,
            "expected_keys": error.expected_keys,
        }, error.status_code

    except MissingKeysError as error:
        return {
            "error": error.message,
            "missing_keys": error.missing_keys,
            "received_keys": error.received_keys,
        }, error.status_code

    except TypeFieldError as error:
        return {"error": error.message}, error.status_code

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

    return jsonify(order_status), HTTPStatus.OK


# def create_order_rating():
#     data = request.get_json()

#     order_rating = OrderRating(**data)

#     db.session.add(order_rating)
#     db.session.commit()

#     return jsonify(order_rating), HTTPStatus.OK
