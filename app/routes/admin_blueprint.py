from flask import Blueprint

from app.controllers import admin_controller, order_controller

bp = Blueprint("admin", __name__, url_prefix="/admin")

# ----------------------------------- USERS ---------------------------------- #
bp.get('/users')(admin_controller.retrieve_users)
bp.get('/users/<user_id>')(admin_controller.retrieve_user_by_id)
bp.patch('/users/<user_id>')(admin_controller.update_user_by_id)
bp.delete('/users/<user_id>')(admin_controller.delete_user_by_id)

# ---------------------------------- ORDERS ---------------------------------- #    
bp.get('/orders')(admin_controller.retrieve_orders)
bp.get('/orders/<order_id>')(admin_controller.retrieve_order_detail)

# --------------------------------- ADDRESSES -------------------------------- #
bp.get('/addresses')(admin_controller.get_addresses)
bp.get('/addresses/<address_id>')(admin_controller.get_address_by_id)
bp.delete('/addresses/<address_id>')(admin_controller.delete_address)
