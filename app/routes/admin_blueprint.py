from flask import Blueprint

from app.controllers import admin_controller

bp = Blueprint('admin', __name__, url_prefix='/admin')

# ----------------------------------- USERS ---------------------------------- #
bp.get('/users')(admin_controller.retrieve_users)
bp.get('/users/<user_id>')(admin_controller.retrieve_user_by_id)
bp.patch('/users/<user_id>')(admin_controller.update_user_by_id)
bp.delete('/users/<user_id>')(admin_controller.delete_user_by_id)

# ---------------------------------- ORDERS ---------------------------------- #    
bp.get('/orders')(admin_controller.retrieve_orders)
bp.get('/orders/<order_id>')(admin_controller.retrieve_order_detail)