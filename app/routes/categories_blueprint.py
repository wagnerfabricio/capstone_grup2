from flask import Blueprint
from app.controllers import categories_controller

bp = Blueprint('categories', __name__)

bp.post('/categories')(categories_controller.create_categories)
bp.get('/categories')(categories_controller.retrieve_categories)