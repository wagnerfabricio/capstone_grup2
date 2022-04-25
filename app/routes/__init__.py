from flask import Blueprint, Flask
from .hello_world_blueprint import bp as bp_hello_world
api = Blueprint('api', __name__)

def init_app(app: Flask):
    api.register_blueprint(bp_hello_world)

    app.register_blueprint(api)