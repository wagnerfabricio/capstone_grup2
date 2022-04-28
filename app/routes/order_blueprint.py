from flask import Blueprint
from app.controllers import order_controller

bp_orders = Blueprint("bp_orders", __name__, url_prefix="/orders")

bp_orders.post("")(order_controller.create_order)
bp_orders.get("")(order_controller.retrieve_orders)
bp_orders.get("/<id>")(order_controller.retrieve_order_by_id)
bp_orders.delete("/<id>")(order_controller.delete_order)
# bp_orders.patch("/<id>")(order_controller.patch_order)
