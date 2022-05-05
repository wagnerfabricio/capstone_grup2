from http import HTTPStatus
from os import getenv
from dotenv import load_dotenv
from flask import request, jsonify
from app.models.categories import Categories
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import DataError
from psycopg2.errors import InvalidTextRepresentation
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user_model import UserModel

load_dotenv()


@jwt_required()
def create_categories():
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
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
                return {"valid keys": categories_columns, "keys sent": wrong_key}, 422

            if type(data["name"]) == str:

                data["name"] = data["name"].title()

                category = Categories(**data)

                session: Session = db.session()

                session.add(category)
                session.commit()

                return jsonify(category), HTTPStatus.CREATED

            else:
                return {"error": "name must be a string value"}, HTTPStatus.BAD_REQUEST
        except:
            return {"error": "this category already exists!"}, HTTPStatus.CONFLICT
    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


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
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
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
    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


def delete_category(id):
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
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

    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED
