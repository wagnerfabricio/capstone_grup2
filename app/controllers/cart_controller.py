from http import HTTPStatus
from dataclasses import asdict

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.configs.database import db
from app.models import UserModel, Cart, Products, CartProducts
from app.services.cart_service import retrieve_products_in_cart

# @jwt_required()
# def create_cart():
#     jwt_user = get_jwt_identity()

#     session = db.session

#     user = UserModel.query.filter_by(email=jwt_user["email"]).first()

#     if not user:
#         return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

#     cart = Cart(user_id=user.id)

#     session.add(cart)
#     session.commit()

#     return {}, HTTPStatus.NO_CONTENT
#     ...


@jwt_required()
def update_cart():
    jwt_user = get_jwt_identity()

    session = db.session

    data = request.get_json()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    cart = Cart.query.filter(Cart.user_id == user.id).first()

    if not cart:
        cart = Cart(user_id=user.id)
        session.add(cart)
        session.commit()

    product = Products.query.filter_by(id=data["id"]).first()

    cart_product = CartProducts(cart_id=cart.id, product_id=product.id)

    session.add(cart_product)
    session.commit()

    return jsonify(product), HTTPStatus.OK


@jwt_required()
def delete_product_to_cart(id):
    jwt_user = get_jwt_identity()

    session = db.session

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    cart: Cart = Cart.query.filter_by(user_id=user.id).first()

    filtered_products = (
        session.query(CartProducts)
        .filter(CartProducts.cart_id == cart.id)
        .filter(CartProducts.product_id == id)
        .all()
    )

    for product in filtered_products:
        session.delete(product)

    session.commit()

    return {}, HTTPStatus.NO_CONTENT


@jwt_required()
def retrieve_cart_products():
    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    cart: Cart = Cart.query.filter(Cart.user_id == user.id).first()

    if not cart:
        return {"error": "cart not found!"}, HTTPStatus.NOT_FOUND

    cart_products = retrieve_products_in_cart(cart.id)
    # mapped_cart_products = [product._asdict() for product in cart_products]

    return jsonify(cart_products), HTTPStatus.OK
