from http import HTTPStatus

from flask import request, jsonify
from app.configs.database import db
from app.models import OrderRating, Order


def create_rating(id):
    data = request.get_json()

    session = db.session

    rating = OrderRating(**data)

    session.add(rating)
    session.commit()

    order_to_update: Order = session.query(Order).filter(Order.id == id).first()

    order_to_update.rating_id = rating.id
    session.add(order_to_update)
    session.commit()

    return jsonify(rating), HTTPStatus.CREATED
