from http import HTTPStatus

from flask import request, jsonify
from app.configs.database import db
from app.models import OrderRating, Order, UserModel
from app.models.exception_model import OrderKeysError, MissingKeysError, TypeFieldError
from app.services import validate_rating_keys
from flask_jwt_extended import jwt_required


@jwt_required()
def create_rating(id):
    data = request.get_json()

    try:
        validate_rating_keys(data)
    except OrderKeysError as error:
        return {
            "error": error.message,
            "invalid_keys": error.invalid_keys,
            "expected_keys": error.expected_keys,
        }, error.status_code
    except MissingKeysError as error:
        return {
            "error": error.message,
            "missing_keys": error.missing_keys,
            "received_keys": error.received_keys,
        }, error.status_code
    except TypeFieldError as error:
        return {"error": error.message}, error.status_code

    session = db.session

    rating = OrderRating(**data)

    session.add(rating)
    session.commit()

    order_to_update: Order = session.query(Order).filter(Order.id == id).first()

    order_to_update.rating_id = rating.id
    session.add(order_to_update)
    session.commit()

    return jsonify(rating), HTTPStatus.CREATED


def retrieve_ratings():
    session = db.session
    query = (
        session.query(UserModel.name, OrderRating.comment, OrderRating.rating)
        .select_from(Order)
        .join(UserModel)
        .join(OrderRating)
        .all()
    )

    mapped_ratings = [order._asdict() for order in query]

    return jsonify(mapped_ratings), HTTPStatus.OK
