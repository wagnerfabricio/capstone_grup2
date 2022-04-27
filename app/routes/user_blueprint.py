from flask import Blueprint
from app.controllers import user_controller

bp = Blueprint('users', __name__)

bp.post('/register')(user_controller.create_user)
bp.post('/login')(user_controller.signin)