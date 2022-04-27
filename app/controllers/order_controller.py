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


def create_order():
    ...


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
