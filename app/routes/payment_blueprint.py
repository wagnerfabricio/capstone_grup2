from flask import Blueprint

from app.controllers import payment_controller

bp = Blueprint('payments', __name__, url_prefix='/payments')

bp.get('')(payment_controller.retrieve_payments)
bp.patch('/<id>')(payment_controller.update_payment)
bp.post('/mercadopago')(payment_controller.mercado_pago_listener)