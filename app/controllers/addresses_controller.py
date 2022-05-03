from http import HTTPStatus
import json
from flask import jsonify
import requests
from flask import request, jsonify
from app.models.addresses_model import AddressesModel
from app.configs.database import db
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.user_model import UserModel


request_keys = ["street", "number", "district", "city", "state", "country", "cep"]


@jwt_required()
def get_address_by_id(id):
    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    addresses = [str(address.__dict__["id"]) for address in user.addresses]

    if id not in addresses:
        return {"error": "invalid user address id"}, HTTPStatus.NOT_FOUND

    try:
        addresses = AddressesModel.query.get(id)

        return jsonify(addresses), HTTPStatus.OK

    except UnmappedInstanceError:
        return {"msg": "addresses not found"}, HTTPStatus.NOT_FOUND


@jwt_required()
def create_address():
    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    data = request.get_json()

    try:
        data_keys = data.keys()
        missing_keys = []
        data_addresses = verify_cep(data["cep"])

        for key in request_keys:
            if key not in data_keys:
                missing_keys.append(key)
        if len(missing_keys) > 0:
            return {"error": f"missing key {missing_keys}"}, HTTPStatus.BAD_REQUEST

        if "cep" not in data_addresses:
            return jsonify({"error": "cep does not exist"}), HTTPStatus.NOT_FOUND
        if len(data["cep"]) != 8:
            return jsonify({"error": "invalid zip code size"}), HTTPStatus.BAD_REQUEST

        data = verify_data(data_addresses, data)
        data["city"] = data["city"].title()
        data["user_id"] = user.id

        addresses = AddressesModel(**data)
        db.session.add(addresses)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": addresses.id,
                    "street": addresses.street,
                    "number": addresses.number,
                    "info": addresses.info,
                    "district": addresses.district,
                    "city": addresses.city,
                    "state": addresses.state,
                    "country": addresses.country,
                    "cep": addresses.cep,
                }
            ),
            HTTPStatus.CREATED,
        )

    except TypeError:
        return jsonify({"error": "wrong type"}), HTTPStatus.BAD_REQUEST


def verify_cep(number):
    r = requests.get(f"http://viacep.com.br/ws/{number}/json/")
    return json.loads(r.content)


def verify_data(data, result):
    if data["cep"] != "":
        result["cep"] = data["cep"]
    else:
        result["cep"] = result["cep"].title()

    if data["logradouro"] != "":
        result["street"] = data["logradouro"]
    else:
        result["street"] = result["street"].title()

    if data["bairro"] != "":
        result["district"] = data["bairro"]
    else:
        result["district"] = result["district"].title()

    if data["localidade"] != "":
        result["city"] = data["localidade"]
    else:
        result["city"] = result["city"].title()

    if data["uf"] != "":
        result["state"] = data["uf"]
    return result


@jwt_required()
def update_address(id):
    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    addresses = [str(address.__dict__["id"]) for address in user.addresses]

    if id not in addresses:
        return {"error": "user address not found"}, HTTPStatus.NOT_FOUND

    data = request.get_json()

    try:

        data_addresses = verify_cep(data["cep"])

        if "cep" not in data_addresses:
            return jsonify({"error": "cep does not exist"}), HTTPStatus.NOT_FOUND
        if len(data["cep"]) != 8:
            return jsonify({"error": "invalid zip code size"}), HTTPStatus.BAD_REQUEST

        data = verify_data(data_addresses, data)
        data["city"] = data["city"].title()

        addresses = AddressesModel.query.filter_by(id=id).one()

        for key, value in data.items():
            setattr(addresses, key, value)

        db.session.add(addresses)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": addresses.id,
                    "street": addresses.street,
                    "number": addresses.number,
                    "info": addresses.info,
                    "district": addresses.district,
                    "state": addresses.state,
                    "city": addresses.city,
                    "country": addresses.country,
                    "cep": addresses.cep,
                }
            ),
            HTTPStatus.OK,
        )

    except TypeError:
        return jsonify({"error": "wrong type"}), HTTPStatus.BAD_REQUEST


@jwt_required()
def delete_address(id):
    jwt_user = get_jwt_identity()

    user = UserModel.query.filter_by(email=jwt_user["email"]).first()

    if not user:
        return {"error": "user id not found"}, HTTPStatus.NOT_FOUND

    user_addresses = [str(address.__dict__["id"]) for address in user.addresses]

    if id not in user_addresses:
        return {"error": "user address not found"}, HTTPStatus.NOT_FOUND

    try:
        addresses = AddressesModel.query.get(id)
        db.session.delete(addresses)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT

    except UnmappedInstanceError:
        return {"msg": "address not found"}, HTTPStatus.UNPROCESSABLE_ENTITY
