from flask import Blueprint
from app.controllers import cart_controller

bp = Blueprint('cart', __name__)

bp.post('/cart')(cart_controller.create_cart)
bp.patch('/products/<id>')(cart_controller.update_cart)
bp.delete('/products/<id>')(products_controller.delete_cart)