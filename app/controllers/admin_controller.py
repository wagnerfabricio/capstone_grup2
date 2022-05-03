from http import HTTPStatus
from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user_model import UserModel
from app.models.user_class_model import UserClassModel
from os import getenv
from app.services import retrieve_orders_admin, retrieve_orders_detail, retrieve_by_id
from dotenv import load_dotenv
from app.models import Order, OrderStatus, OrderProduct
from app.models.exception_model import IdNotFoundError

load_dotenv()

# ----------------------------------- USERS ---------------------------------- #
@jwt_required()
def retrieve_users():
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
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

    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


@jwt_required()
def retrieve_user_by_id(user_id: str):
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
        user = UserModel.query.get(user_id)

        if not user:
            return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "birthday": user.birthday,
            }
        )

    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


@jwt_required()
def update_user_by_id(user_id: str):
    data = request.get_json()

    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
        user = UserModel.query.get(user_id)

        if not user:
            return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(user, key, value)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return "", HTTPStatus.OK

    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


@jwt_required()
def delete_user_by_id(user_id: str):
    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
        user = UserModel.query.get(user_id)

        if not user:
            return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

        current_app.db.session.delete(user)
        current_app.db.session.commit()

        return "", HTTPStatus.OK
    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


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
        try:
            order = retrieve_orders_detail(order_id)
        except IdNotFoundError:
            return {"error": "Id not found!"}, HTTPStatus.NOT_FOUND
        return jsonify(order), HTTPStatus.OK


@jwt_required()
def update_order(order_id):
    data: dict = request.get_json()
    session = current_app.db.session

    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
        new_status = session.query(OrderStatus).filter_by(type=data["type"]).first()

        # order: Order = session.query(Order).filter_by(id=order_id).first()
        try:
            order: Order = retrieve_by_id(Order, order_id)
        except IdNotFoundError:
            return {"error": "Id not found!"}, HTTPStatus.NOT_FOUND
        for key, value in data.items():
            setattr(order.status, key, value)

        session.add(order)
        session.commit()

        order_detail = retrieve_orders_detail(order_id)
        return jsonify(order_detail), HTTPStatus.OK
    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED


@jwt_required()
def delete_order(order_id):

    admin: UserModel = UserModel.query.filter_by(
        email=get_jwt_identity()["email"]
    ).first()

    if str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
        session = current_app.db.session
        # order_to_delete = session.query(Order).filter(Order.id == order_id).first()
        order_to_delete = retrieve_by_id(Order, order_id)

        orders_products_to_delete = (
            session.query(OrderProduct).filter(OrderProduct.order_id == order_id).all()
        )

        if orders_products_to_delete:
            for order_product in orders_products_to_delete:
                session.delete(order_product)

        session.delete(order_to_delete)
        session.commit()
        return {}, HTTPStatus.NO_CONTENT

    return {
        "error": "you are not authorized to access this page"
    }, HTTPStatus.UNAUTHORIZED
