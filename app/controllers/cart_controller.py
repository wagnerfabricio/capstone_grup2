from http import HTTPStatus

from app.configs.database import db
from app.models.cart_products_model import CartProducts
from flask import jsonify, request
from flask_sqlalchemy import BaseQuery
from psycopg2.errors import InvalidTextRepresentation
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session
from werkzeug.exceptions import NotFound


def create_cart():
    try:
        data = request.get_json()

        data_keys = [key for key in data.keys()]

        wrong_key = []

        cart_columns = [
            "id",
            "cart_id",
            "products",
        ]

        for key in data_keys:
            if key not in cart_columns:
                wrong_key.append(key)

        if len(wrong_key) > 0:
            return {"valid keys": cart_columns, "keys sent": wrong_key}, 422

        if type(data["id"]) == str and type(data["cart_id"]) == str:

            if type(data["products"]) != list:
                return {"error": "products must be a list."}, HTTPStatus.BAD_REQUEST

            data["name"] = data["name"].title()

            cart = CartProducts(**data)

            session: Session = db.session()

            session.add(product)
            session.commit()

            return jsonify(cart), HTTPStatus.CREATED

        else:
            return {
                "error": "id and cart_id must be a string value"
            }, HTTPStatus.BAD_REQUEST
    except:
        return {"error": "this cart already exists!"}, HTTPStatus.CONFLICT


def update_cart(id):

    try:
        data = request.get_json()

        session: Session = db.session

        record = session.query(CartProducts).get(id)

        if not record:
        return {"error": "id not found"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
        setattr(record, key, value)

        session.commit()

        return jsonify(record), HTTPStatus.OK

            except DataError as e:

            if isinstance(e.orig, InvalidTextRepresentation):

            return {"error": "cart does not exists"}, HTTPStatus.NOT_FOUND 

            return {"error":"DEU RUIM" }, 404


    def delete_cart(id):
        try:
            session: Session = db.session
            record = session.query(CartProducts).get(id)
            if not record:
                return {"error": "id not found"}, HTTPStatus.NOT_FOUND
            session.delete(record)
            session.commit()
            return {"message": "cart deleted"}, HTTPStatus.OK
        except:
            return {"error": "cart does not exists"}, HTTPStatus.NOT_FOUND
