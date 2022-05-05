from http import HTTPStatus
from itertools import product
from flask import request, jsonify
from app.models.categories import Categories
from app.models.products_model import Products
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import DataError, IntegrityError
from psycopg2.errors import InvalidTextRepresentation, UniqueViolation
from app.services.category_service import verify_if_category_exists

def create_products():
    try:
        data = request.get_json()

        data_keys = {key for key in data.keys()}

        products_columns = {
            "name",
            "description",
            "price",
            "active",
            "qtt_stock",
            "category",
        }

        missing_keys = products_columns - data_keys
      
        if missing_keys:
            return {
                "error": "missing keys",
                "expected": list(products_columns),
                "received": list(data_keys),
                "missing": list(missing_keys),
            }, HTTPStatus.BAD_REQUEST

        if type(data["name"]) == str and type(data["description"]) == str:

            if type(data["active"]) != bool:
                return {"error": "active must be bool."}, HTTPStatus.BAD_REQUEST

            if type(data["price"]) != int and type(data["price"]) != float:
                return {
                    "error": "price must be a numeric value."
                }, HTTPStatus.BAD_REQUEST

            if type(data["qtt_stock"]) != int:
                return {
                    "error": "qtt_stock must be a integer value."
                }, HTTPStatus.BAD_REQUEST

            data["name"] = data["name"].title()

            
            category_name = data.pop('category')

            session: Session = db.session()
            category = verify_if_category_exists(category_name)

            data['category_id'] = category.id
            

            product = Products(**data)


            session.add(product)
            session.commit()

            return jsonify(product), HTTPStatus.CREATED

        else:
            return {
                "error": "name and description must be a string value"
            }, HTTPStatus.BAD_REQUEST
    except:
        return {"error": "this product already exists!"}, HTTPStatus.CONFLICT


def retrieve_products():
    try:
        category = request.args.get('category')

        if category:

            base_query: Query = db.session.query(Categories)

            record_query: BaseQuery = base_query.filter(Categories.name.ilike(f'%{category}%'))

            record = record_query.first_or_404(description="id not found")

            r = {"name": record.name,
                "products": record.products}

            return jsonify(r), HTTPStatus.OK
        
        product_name = request.args.get('name')
    
        if product_name:
         
            base_query: Query = db.session.query(Products)

            record_query: BaseQuery = base_query.filter(Products.name.ilike(f'%{product_name}%'))

            record = record_query.first_or_404(description="id not found")

            r = {"name": record.name}

            return jsonify(r), HTTPStatus.OK
           
        base_query: Query = db.session.query(Products)
        records = base_query.all()

        return (
            jsonify(
                [
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "category": product.category.name,
                        "description": product.description,
                        "quantityStock": product.qtt_stock,
                        "img": product.img,
                    }
                    for product in records
                ]
            ),
            HTTPStatus.OK,
        )
    except Exception as error:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND


def retrieve_products_by_id(id):
    base_query: Query = db.session.query(Products)

    record_query: BaseQuery = base_query.filter_by(id=id)

    try:
        record = record_query.first_or_404(description="id not found")

        return jsonify(record), HTTPStatus.OK

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except DataError as e:

        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "product does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND


def update_product(id):
    try:
        data = request.get_json()

        session: Session = db.session

        record = session.query(Products).get(id)

        if not record:
            return {"error": "id not found"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(record, key, value)

        session.commit()

        return jsonify(record), HTTPStatus.OK

    except DataError as e:

        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "product does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND


def delete_product(id):
    try:
        session: Session = db.session

        record = session.query(Products).get(id)

        if not record:
            return {"error": "id not found"}, HTTPStatus.NOT_FOUND

        session.delete(record)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except DataError as e:

        if isinstance(e.orig, InvalidTextRepresentation):
            return {"error": "product does not exists"}, HTTPStatus.NOT_FOUND

        return {"error": e.args[0]}, HTTPStatus.NOT_FOUND
