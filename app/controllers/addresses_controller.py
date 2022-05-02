from http import HTTPStatus
import json
from flask import jsonify
import requests
from flask import request, jsonify
from app.models.addresses_model import AddressesModel
from app.configs.database import db
from sqlalchemy.orm.exc import UnmappedInstanceError

request_keys = ["street", "cep", "country", "city", "district", "number"]

def get_addresses():
    addresses = (
        AddressesModel
        .query
        .all()
    )
    result = []
    for addresse in addresses:
        addresse = addresse.__dict__
        addresse.pop('_sa_instance_state', None)
        result.append(addresse)

    if not result:
        return jsonify({"error": "no results"}), 404

    return jsonify({"addresses": result}), HTTPStatus.OK

def get_addresses_by_id(id):
    try:
        addresses = (
            AddressesModel
            .query
            .get(id)
        )
    
        addresses = addresses.__dict__
        addresses.pop('_sa_instance_state', None)
    
        return jsonify(addresses), HTTPStatus.OK
       
    except UnmappedInstanceError:
        return  {"msg": "addresses not found"}, HTTPStatus.NOT_FOUND


def post_addresses():
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
    
        if 'cep' not in data_addresses:
            return jsonify({"error": "cep does not exist"}), HTTPStatus.NOT_FOUND
        if len(data["cep"]) != 8:
            return jsonify({"error": "invalid zip code size"}), HTTPStatus.BAD_REQUEST

        data = verify_dados(data_addresses, data)
        data["city"] = data["city"].title()


        addresses = AddressesModel(**data)
        db.session.add(addresses)
        db.session.commit()
        
        return jsonify({
            "id": addresses.id,
            "street": addresses.street,
            "cep": addresses.cep,
            "country": addresses.country,
            "city": addresses.city,
            "info": addresses.info,
            "district": addresses.district,
            "number": addresses.number
        }), HTTPStatus.CREATED

    except TypeError:
        return jsonify({"error": "wrong type"}), HTTPStatus.BAD_REQUEST

def verify_cep(number):
    r = requests.get(f'http://viacep.com.br/ws/{number}/json/')
    return json.loads(r.content)

def verify_dados(data, result):
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
    return result

def patch_addresses(id):
    data = request.get_json()

    try:

        data_addresses = verify_cep(data["cep"])

        if 'cep' not in data_addresses:
            return jsonify({"error": "cep does not exist"}), HTTPStatus.NOT_FOUND
        if len(data["cep"]) != 8:
            return jsonify({"error": "invalid zip code size"}), HTTPStatus.BAD_REQUEST

        data = verify_dados(data_addresses, data)
        data["city"] = data["city"].title()

        addresses = AddressesModel.query.filter_by(id=id).one()

        for key, value in data.items():
            setattr(addresses, key, value)
  
        db.session.add(addresses)
        db.session.commit()
        
        return jsonify({
            "id": addresses.id,
            "street": addresses.street,
            "cep": addresses.cep,
            "country": addresses.country,
            "city": addresses.city,
            "info": addresses.info,
            "district": addresses.district,
            "number": addresses.number
        }), HTTPStatus.OK

    except TypeError:
        return jsonify({"error": "wrong type"}), HTTPStatus.BAD_REQUEST

def delete_addresses(id):
    try:
        addresses = AddressesModel.query.get(id)
        db.session.delete(addresses)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
    except UnmappedInstanceError:
        return  {"msg": "addresses not found"}, HTTPStatus.NOT_FOUND