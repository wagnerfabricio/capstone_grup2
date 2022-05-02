from flask import Blueprint

from app.controllers import addresses_controller

bp_addresses = Blueprint('addresses', __name__, url_prefix='/addresses')

# ----------------------------------- USERS ---------------------------------- #
bp_addresses.get('/')(addresses_controller.get_addresses)
bp_addresses.get('<int:id>')(addresses_controller.get_addresses_by_id)
bp_addresses.post('/')(addresses_controller.post_addresses)
bp_addresses.patch('<int:id>')(addresses_controller.patch_addresses)
bp_addresses.delete('<int:id>')(addresses_controller.delete_addresses)