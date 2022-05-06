from flask import Blueprint

from app.controllers import addresses_controller

bp_addresses = Blueprint('addresses', __name__, url_prefix='/addresses')

bp_addresses.get('<id>')(addresses_controller.get_address_by_id)
bp_addresses.post('')(addresses_controller.create_address)
bp_addresses.patch('<id>')(addresses_controller.update_address)
bp_addresses.delete('<id>')(addresses_controller.delete_address)
bp_addresses.get('/verify/<cep_number>')(addresses_controller.check_cep)
# bp_addresses.get('/verify_cep/<number>')(addresses_controller.verify_cep)