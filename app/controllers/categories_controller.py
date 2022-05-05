from http import HTTPStatus
from flask import request, jsonify
from app.models.categories import Categories
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import DataError
from psycopg2.errors import InvalidTextRepresentation
from app.models.products_model import Products
from app.services.category_service import verify_if_category_exists
from app.models.exception_model import CategoryAlreadyExistsError
from sqlalchemy.sql.operators import ilike_op


def create_categories():
    try:
        data = request.get_json()

        data_keys = [key for key in data.keys()]

        wrong_key = []

        categories_columns = [
            "name",
        ]

        for key in data_keys:
            if key not in categories_columns:
                wrong_key.append(key)

        if len(wrong_key) > 0:
                return {
                        "error": "invalid key",
                        "valid key": categories_columns,
                        "key sent": wrong_key}, 422

        if type(data["name"]) == str:

            data["name"] = data["name"].title()

            category = Categories.query.filter_by(name=data['name']).first()

            if category:
                raise CategoryAlreadyExistsError

            new_category = Categories(name=data['name'])
            db.session.add(new_category)
            db.session.commit()

            return jsonify(new_category), HTTPStatus.CREATED

        else:
            return {"error": "name must be a string value"}, HTTPStatus.BAD_REQUEST

    except CategoryAlreadyExistsError: 
        return {"error": "this category already exists!"}, HTTPStatus.CONFLICT


def retrieve_categories():
    try:
        base_query: Query = db.session.query(Categories)
        records = base_query.all()

        return jsonify(records), HTTPStatus.OK
    except:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND


def retrieve_categories_by_id(id):
    base_query: Query = db.session.query(Categories)

    record_query: BaseQuery = base_query.filter_by(id=id)

    try:
        record = record_query.first_or_404(description="id not found")

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except DataError as e:
        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "category does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND

    return jsonify(record), HTTPStatus.OK


def update_category(id):
    try:
        data = request.get_json()

        session: Session = db.session

        record = session.query(Categories).get(id)

        if not record:
            return {"error": "id not found"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(record, key, value)

        session.commit()

        return jsonify(record), HTTPStatus.OK

    except DataError as e:
        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "category does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND


def delete_category(id):
    try:
        session: Session = db.session

        record = session.query(Categories).get(id)

        if not record:
            return {"error": "id not found"}, HTTPStatus.NOT_FOUND

        session.delete(record)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except DataError as e:
        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "category does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND
