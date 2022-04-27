from http import HTTPStatus
from flask import request, jsonify
from app.models.categories import Categories
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query

def create_categories():
    try:
        data = request.get_json()

        data_keys = [key for key in data.keys()]

        wrong_key = []

        categories_columns = [
                "name",
            ]

        for key in data_keys:
                if key not in categories_columns:
                    wrong_key.append(key)
        
        if len(wrong_key) > 0:
                return {"valid keys": categories_columns,
                        "keys sent": wrong_key}, 422

        if type(data['name']) == str:

            data['name'] = data['name'].title()

            category = Categories(**data)

            session: Session = db.session()

            session.add(category)
            session.commit()

            return jsonify(category), HTTPStatus.CREATED

        else:
            return {"error": "name must be a string value"}, HTTPStatus.BAD_REQUEST
    except:
        return {"error": "this category already exists!"}, HTTPStatus.CONFLICT

def retrieve_categories():
    try:
        base_query: Query = db.session.query(Categories)
        records = base_query.all()

        return jsonify(records), HTTPStatus.OK
    except:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND