from http import HTTPStatus
from flask import jsonify, request
from app.models import Order
from app.services import retrieve, retrieve_by_id,retrieve_orders_detail,retrieve_orders_user


def create_order():
    ...


def retrieve_orders():
    list_orders = retrieve_orders_user()

    return jsonify(list_orders), HTTPStatus.OK


def retrieve_order_by_id(id:int):
    response = retrieve_orders_detail(id)
    print(response)
    return ""
    ...


def delete_order():
    ...


def update_order():
    ...
