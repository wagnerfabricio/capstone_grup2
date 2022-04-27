from http import HTTPStatus
from flask import jsonify, request
from app.models import Order
from app.services import retrieve, retrieve_by_id


def create_order():
    ...


def retrieve_orders():
    list_orders = retrieve(Order)

    return jsonify(list_orders), HTTPStatus.OK


def retrieve_order_by_id():
    ...


def delete_order():
    ...


def update_order():
    ...
