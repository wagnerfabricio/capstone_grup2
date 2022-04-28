from flask import Blueprint
from app.controllers import hello_world_controller


bp = Blueprint('hello_world', __name__, url_prefix='/hello')

bp.get('')(hello_world_controller.hello)