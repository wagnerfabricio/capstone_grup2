from datetime import datetime as dt
from http import HTTPStatus
from dotenv import load_dotenv


from flask import jsonify, request
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.exception_model import OrderKeysError, MissingKeysError, TypeFieldError
from app.services import (
    validate_order_keys,
    validate_status_keys,
    validate_payment_keys,
)

from os import getenv

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
    validate_keys_update,
)
from app.services.order_service import retrieve_orders_admin


load_dotenv()


@jwt_required()
def create_order():
    data = request.get_json()
    jwt_user = get_jwt_identity()
    try:
        validate_order_keys(data)
        format_order_data(data, jwt_user)
    except OrderKeysError as error:
        return {
            "error": error.message,
            "wrong_keys": error.invalid_keys,
            "expected_keys": error.expected_keys,
        }, error.status_code
    except TypeFieldError as error:
        return {"error": error.message}, error.status_code

    session = db.session

    list_products = data.pop("products")

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

        return e.args[0]

    serialize_and_create_order_products(list_products, new_order)
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


@jwt_required()
def retrieve_orders():
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):

        list_orders = retrieve_orders_admin()
        return jsonify(list_orders), HTTPStatus.OK

    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


def retrieve_order_by_id(id: int):
    response = retrieve_orders_detail(id)

    if not response:
        return {"error": f"id {id} not found!"}, HTTPStatus.NOT_FOUND

    return jsonify(response), HTTPStatus.OK


@jwt_required()
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


@jwt_required()
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


def create_order_payment():
    data = request.get_json()

    try:
        validate_payment_keys(list(data.keys()))
        order_payment = OrderPayment(**data)
        db.session.add(order_payment)
        db.session.commit()
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

    return jsonify(order_payment), HTTPStatus.OK


@jwt_required()
def create_order_status():
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):

        data: dict = request.get_json()

        try:
            validate_status_keys(list(data.keys()))
            data["status"] = data["status"].capitalize()
            order_status = OrderStatus(**data)
            db.session.add(order_status)
            db.session.commit()

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

    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


# def create_order_rating():
#     data = request.get_json()

#     order_rating = OrderRating(**data)

#     db.session.add(order_rating)
#     db.session.commit()

#     return jsonify(order_rating), HTTPStatus.OK
