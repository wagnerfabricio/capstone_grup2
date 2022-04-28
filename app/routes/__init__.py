from flask import Blueprint, Flask
from .hello_world_blueprint import bp as bp_hello_world
from .user_blueprint import bp as bp_user
from .products_blueprint import bp as bp_products
from .categories_blueprint import bp as bp_categories
from .order_blueprint import bp_orders
from .admin_blueprint import bp as bp_admin


api = Blueprint("api", __name__)


def init_app(app: Flask):
    api.register_blueprint(bp_hello_world)
    api.register_blueprint(bp_user)
    api.register_blueprint(bp_products)
    api.register_blueprint(bp_categories)
    api.register_blueprint(bp_orders)
    api.register_blueprint(bp_admin)
    app.register_blueprint(api)
