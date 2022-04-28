from http import HTTPStatus
from flask import jsonify, request
from app.models import Order
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


def create_order():
    data = request.get_json()

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

    return jsonify(new_order), HTTPStatus.CREATED


def retrieve_orders():
    list_orders = retrieve_orders_admin()

    return jsonify(list_orders), HTTPStatus.OK


def retrieve_order_by_id(id: int):
    response = retrieve_orders_detail(id)
    
    return jsonify(response),HTTPStatus.OK
    


def delete_order():
    ...


def update_order():
    ...
