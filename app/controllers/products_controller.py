from http import HTTPStatus
from flask import request, jsonify
from app.models.products_model import Products
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import DataError
from psycopg2.errors import InvalidTextRepresentation

def create_products():
    try:
        data = request.get_json()

        data_keys = [key for key in data.keys()]

        wrong_key = []

        products_columns = [
                "name",
                "description",
                "price",
                "active",
                "qtt_stock",
                "img",
            ]

        for key in data_keys:
                if key not in products_columns:
                    wrong_key.append(key)
        
        if len(wrong_key) > 0:
                return {"valid keys": products_columns,
                        "keys sent": wrong_key}, 422

        if type(data['name']) == str and type(data['description']) == str:

            if type(data["active"]) != bool:
                return {"error": "active must be bool."}, HTTPStatus.BAD_REQUEST

            if type(data["price"]) != int and type(data["price"]) != float:
                return {"error": "price must be a numeric value."}, HTTPStatus.BAD_REQUEST

            if type(data["qtt_stock"]) != int:
                return {"error": "qtt_stock must be a integer value."}, HTTPStatus.BAD_REQUEST
            
            data['name'] = data['name'].title()

            product = Products(**data)

            session: Session = db.session()

            session.add(product)
            session.commit()

            return jsonify(product), HTTPStatus.CREATED

        else:
            return {"error": "name and description must be a string value"}, HTTPStatus.BAD_REQUEST
    except:
        return {"error": "this product already exists!"}, HTTPStatus.CONFLICT

def retrieve_products():
    try:
        base_query: Query = db.session.query(Products)
        records = base_query.all()

        return jsonify(records), HTTPStatus.OK
    except:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND

def retrieve_products_by_id(id):
    base_query: Query = db.session.query(Products)

    record_query: BaseQuery = base_query.filter_by(id=id)

    try:
        record = record_query.first_or_404(description="id not found")

        return jsonify(record), HTTPStatus.OK

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except DataError as e:

        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "product does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND

    

def update_product(id):
    try:
        data = request.get_json()

        session: Session = db.session

        record = session.query(Products).get(id)

        if not record:
            return {"error": "id not found"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(record, key, value)

        session.commit()

        return jsonify(record), HTTPStatus.OK

    except DataError as e:

        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "product does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND

def delete_product(id):
    try:
        session: Session = db.session

        record = session.query(Products).get(id)

        if not record:
            return {"error": "id not found"}, HTTPStatus.NOT_FOUND

        session.delete(record)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except DataError as e:

        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "product does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND