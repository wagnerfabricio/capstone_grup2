from flask import Blueprint
from app.controllers import cart_controller

bp = Blueprint("carts", __name__, url_prefix="/carts")


bp.patch("")(cart_controller.update_cart)
bp.delete("/<id>")(cart_controller.delete_product_to_cart)
bp.get("")(cart_controller.retrieve_cart_products)
