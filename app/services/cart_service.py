from app.configs.database import db
from app.models import Products, Cart, CartProducts
from sqlalchemy import func


def retrieve_products_in_cart(cart_id, dict=True):
    session = db.session
    cart_products = (
        session.query(
            Products.id,
            Products.name,
            func.sum(Products.price).label("price"),
            func.count(Products.name).label("quantidade"),
            # Products.price,
            Products.img,
        )
        .select_from(Cart)
        .join(CartProducts)
        .join(Products)
        .filter(Cart.id == cart_id)
        .group_by(Products.name, Products.price, Products.img, Products.id)
        .all()
    )

    if dict:
        print("TA CHEGANDO")
        return [product._asdict() for product in cart_products]

    return cart_products
