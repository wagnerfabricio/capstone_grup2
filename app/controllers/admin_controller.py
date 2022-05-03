from http import HTTPStatus
from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.addresses_model import AddressesModel
from app.models.exception_model import UnauthorizedError
from app.models.user_model import UserModel
from app.models.user_class_model import UserClassModel
from os import getenv
from app.services import retrieve_orders_admin, retrieve_orders_detail
from dotenv import load_dotenv

from sqlalchemy.orm.exc import UnmappedInstanceError

from app.services.admin_service import verify_admin_access


load_dotenv()

# ----------------------------------- USERS ---------------------------------- #
@jwt_required()
def retrieve_users():

    try:
        verify_admin_access()

        users_list = UserModel.query.order_by("name").all()

        return jsonify(
            [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "birthday": user.birthday,
                }
                for user in users_list
            ]
        )

    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def retrieve_user_by_id(user_id: str):
    try:
        verify_admin_access()

        user = UserModel.query.get(user_id)
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

    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def update_user_by_id(user_id: str):
    data = request.get_json()

    try:
        verify_admin_access()

        user = UserModel.query.get(user_id)

        if not user:
            return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(user, key, value)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return "", HTTPStatus.OK

    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def delete_user_by_id(user_id: str):
    try:
        verify_admin_access()

        user = UserModel.query.get(user_id)
        if not user:
            return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

        current_app.db.session.delete(user)
        current_app.db.session.commit()

        return "", HTTPStatus.OK

    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED


# ---------------------------------- ORDERS ---------------------------------- #
@jwt_required()
def retrieve_orders():
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
        orders = retrieve_orders_admin()

        return jsonify(orders), HTTPStatus.OK
        ...
    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


@jwt_required()
def retrieve_order_detail(order_id: int):
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
        order = retrieve_orders_detail(order_id)

        return jsonify(order), HTTPStatus.OK

    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


# --------------------------------- ADDRESSES -------------------------------- #
@jwt_required()
def get_addresses():
    try:
        verify_admin_access()

        addresses = AddressesModel.query.all()

        return jsonify(addresses), HTTPStatus.OK

    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def get_address_by_id(address_id):
    try:
        verify_admin_access()

        address = AddressesModel.query.get(address_id)

        if not address:
            return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

        return jsonify(address)

    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def delete_address(address_id):
    try:
        verify_admin_access()

        address = AddressesModel.query.get(address_id)
        current_app.db.session.delete(address)
        current_app.db.session.commit()

        return "", HTTPStatus.NO_CONTENT

    except UnmappedInstanceError:
        return {"error": "address id not found"}, HTTPStatus.UNPROCESSABLE_ENTITY

    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED
