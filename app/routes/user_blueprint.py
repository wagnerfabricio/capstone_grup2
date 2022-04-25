from flask import Blueprint
from app.controllers import user_controller

bp = Blueprint('users', __name__)

bp.post('/user')(user_controller.create_user)
bp.post('/signin')(user_controller.signin)