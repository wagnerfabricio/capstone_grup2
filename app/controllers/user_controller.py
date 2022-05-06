from http import HTTPStatus
from flask import current_app, jsonify, request
from app.models.exception_model import InvalidEmailError, InvalidPasswordError
from app.models.user_model import UserModel
from app.configs.database import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, NotNullViolation
from app.services import retrieve_orders_user

from dataclasses import asdict

from datetime import timedelta

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


def create_user():
    data = request.get_json()
    try:
        new_user: UserModel = UserModel(
            name=data["name"], email=data["email"], password=data["password"]
        )
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

    # if not user or not user.verify_password(data["password"]):
    #     return {"error": "Invalid email or password"}, HTTPStatus.UNAUTHORIZED

    token = create_access_token(user, expires_delta=timedelta(days=30))
    admin = bool(user.user_class)

    user_address = user.addresses[-1] if user.addresses else ""
    # user_address = user_address.__dict__ if user_address else ""
    user_address = asdict(user_address) if user_address else ""

    return {
        "accessToken": token,
        "user": {
            "email": user.email,
            "name": user.name,
            "id": user.id,
            "admin": admin,
            "address": f'{user_address.get("street")}, {user_address.get("number")}, Bairro: {user_address.get("district")}, Cidade: {user_address.get("city")}/{user_address.get("state")} - CEP: {user_address.get("cep")}'
            if type(user_address) is dict
            else "",
        },
    }, HTTPStatus.OK


# --------------------------------- VERIFICAR -------------------------------- #
@jwt_required()
def retrieve_orders():
    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    orders = retrieve_orders_user()

    return jsonify(orders), HTTPStatus.OK


# --------------------------------- VERIFICAR -------------------------------- #


@jwt_required()
def retrieve_user():
    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    return jsonify(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "birthday": user.birthday,
            "addresses": user.addresses,
        }
    )


@jwt_required()
def update_user():
    data = request.get_json()

    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(user, key, value)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify(user), HTTPStatus.OK


@jwt_required()
def delete_user():
    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    current_app.db.session.delete(user)
    current_app.db.session.commit()

    return "", HTTPStatus.OK
