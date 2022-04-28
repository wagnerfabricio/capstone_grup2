from flask import Blueprint
from app.controllers import products_controller

bp = Blueprint('products', __name__)

bp.post('/products')(products_controller.create_products)
bp.get('/products')(products_controller.retrieve_products)