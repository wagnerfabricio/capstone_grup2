from http import HTTPStatus
from flask import jsonify, request
from dotenv import load_dotenv
from os import getenv
import json

from app.models.payments_model import PaymentModel
from app.configs.database import db

load_dotenv()

import requests


def mercado_pago_listener():
    data = request.get_json()

    payment_id = data.data.get(id)

    if payment_id:
        requisition = requests.get(
            f"https://api.mercadopago.com/v1/payments/{payment_id}",
            headers={"Authorization": getenv("MERCADO_PAGO_TOKEN")},
        )

        payment_info = json.loads(requisition.content)

        new_payment = PaymentModel(type='Mercado Pago', status=payment_info.get('status'), mercadopago_id=payment_info.get('id'), mercadopago_type=payment_info.get('payment_type_id'))

        db.session.add(payment_info)
        db.cm.session.commit()

    return {"success": 'pagamento criado'}, HTTPStatus.CREATED


def retrieve_payments():
    payment_list = PaymentModel.query.all()

    return jsonify(payment_list), HTTPStatus.OK