from http import HTTPStatus
from flask import jsonify, request
from app.models.exception_model import InvalidEmailError, InvalidPasswordError
from app.models.user_model import UserModel
from app.configs.database import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, NotNullViolation
from app.services import retrieve_orders_user

from datetime import timedelta

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


def create_user():
    data = request.get_json()
    try:
        new_user: UserModel = UserModel(**data)
        db.session.add(new_user)
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

        if isinstance(e.orig, NotNullViolation):

            expected = UserModel.expected_keys
            received = {key for key in data.keys()}
            missing = expected - received

            return {
                "error": "missing keys",
                "expected": list(expected),
                "received": list(received),
                "missing": list(missing),
            }, HTTPStatus.BAD_REQUEST

        return e.args[0]

    except InvalidPasswordError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST

    except InvalidEmailError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST

    return jsonify(new_user), HTTPStatus.CREATED


def signin():
    data = request.get_json()

    user: UserModel = UserModel.query.filter_by(email=data["email"]).first()

    if not user or not user.verify_password(data["password"]):
        return {"error": "Invalid email or password"}, HTTPStatus.UNAUTHORIZED

    token = create_access_token(user, expires_delta=timedelta(days=30))
    admin = bool(user.user_class)

    return {
        "data": {
            "access_token": token,
            "user": {
                "email": user.email,
                "name": user.name,
                "id": user.id,
                "admin": admin,
            },
        }
    }, HTTPStatus.OK


def retrieve_orders():
    orders = retrieve_orders_user()

    return jsonify(orders), HTTPStatus.OK
