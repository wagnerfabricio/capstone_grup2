from flask import Blueprint

from app.controllers import addresses_controller

bp_addresses = Blueprint('addresses', __name__, url_prefix='/addresses')

bp_addresses.get('/')(addresses_controller.get_addresses)
bp_addresses.get('<id>')(addresses_controller.get_addresses_by_id)
bp_addresses.post('/')(addresses_controller.post_addresses)
bp_addresses.patch('<id>')(addresses_controller.patch_addresses)
bp_addresses.delete('<id>')(addresses_controller.delete_addresses)