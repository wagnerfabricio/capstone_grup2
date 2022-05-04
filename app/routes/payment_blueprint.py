from flask import Blueprint

from app.controllers import payment_controller

bp = Blueprint('users', __name__, url_prefix='/payments')

bp.post('/mercadopago')(payment_controller.mercado_pago_listener)
bp.get('')(payment_controller.retrieve_payments)
