from flask import Blueprint

from app.controllers import admin_controller, order_controller,products_controller,categories_controller

bp = Blueprint("admin", __name__, url_prefix="/admin")

# ----------------------------------- USERS ---------------------------------- #
bp.get('/users')(admin_controller.retrieve_users)
bp.get('/users/<user_id>')(admin_controller.retrieve_user_by_id)
bp.patch('/users/<user_id>')(admin_controller.update_user_by_id)
bp.delete('/users/<user_id>')(admin_controller.delete_user_by_id)

# ---------------------------------- ORDERS ---------------------------------- #    
bp.get('/orders')(admin_controller.retrieve_orders)
bp.get('/orders/<order_id>')(admin_controller.retrieve_order_detail)
bp.delete('/orders/<order_id>')(admin_controller.delete_order)
bp.patch('/orders/<order_id>')(admin_controller.update_order)

# ---------------------------------- STATUS ---------------------------------- #   
bp.post("/orders/status")(order_controller.create_order_status)

# --------------------------------- ADDRESSES -------------------------------- #
bp.get('/addresses')(admin_controller.get_addresses)
bp.get('/addresses/<address_id>')(admin_controller.get_address_by_id)
bp.delete('/addresses/<address_id>')(admin_controller.delete_address)

# --------------------------------- PRODUCTS --------------------------------- #
bp.post("/products")(products_controller.create_products)
bp.patch("/products/<id>")(products_controller.update_product)
bp.delete("/products/<id>")(products_controller.delete_product)

# --------------------------------- CATEGORIES ------------------------------- #
bp.post("/categories")(categories_controller.create_categories)
bp.patch("/categories/<id>")(categories_controller.update_category)
bp.delete("/categories/<id>")(categories_controller.delete_category)