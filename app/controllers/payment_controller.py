from dataclasses import asdict
from http import HTTPStatus
from uuid import uuid4
from flask import jsonify, request
from dotenv import load_dotenv
from os import getenv
import json
from app.models.exception_model import UnauthorizedError
from app.models.order_model import Order

from app.models.payments_model import PaymentModel
from app.configs.database import db

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from flask_jwt_extended import jwt_required

from app.services.admin_service import verify_admin_access


load_dotenv()

import requests


def mercado_pago_listener():
    data = request.get_json()

    payment_id = data.get("data")

    if not payment_id:
        return {"error": "invalid payment method"}

    payment_id = payment_id.get("id")

    requisition = requests.get(
        f"https://api.mercadopago.com/v1/payments/{payment_id}",
        headers={"Authorization": f'Bearer {getenv("MERCADO_PAGO_TOKEN")}'},
    )

    payment_info = json.loads(requisition.content)

    payment = PaymentModel.query.filter_by(
        order_id=payment_info.get("external_reference")
    ).first()

    update_data = {
        "type": "Mercado Pago",
        "status": payment_info.get("status"),
        "mercadopago_id": payment_info.get("id"),
        "mercadopago_type": payment_info.get("payment_type_id"),
    }

    for key, value in update_data.items():
        setattr(payment, key, value)

    db.session.add(payment)
    db.session.commit()

    return {"success": "pagamento alterado com sucesso"}, HTTPStatus.CREATED


def create_payment(order_id: uuid4):
    new_payment = PaymentModel(order_id=order_id)
    db.session.add(new_payment)
    db.session.commit()

    return new_payment

@jwt_required()
def retrieve_payments():
    try:
        verify_admin_access()
        payment_list = PaymentModel.query.all()
        return jsonify(payment_list), HTTPStatus.OK
    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED 
    


@jwt_required()
def update_payment(id):
    try:
        verify_admin_access()
        data = request.get_json()
        payment_status = data.get("status")

        payment = PaymentModel.query.get(id)

        if not payment:
            return {"error": "Payment not found"}, HTTPStatus.NOT_FOUND

        if not payment_status:
            return {"error": "Payment status not found"}, HTTPStatus.BAD_REQUEST

        setattr(payment, "status", payment_status)

        db.session.add(payment)
        db.session.commit()

        return jsonify(payment), HTTPStatus.OK
    except UnauthorizedError as e:
        return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED