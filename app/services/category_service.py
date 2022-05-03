# segunda parte

from dataclasses import asdict
import json
from unicodedata import category

from flask import current_app, jsonify, session
from sqlalchemy.orm import Session
from app.models.categories import Categories
from app.configs.database import db
from app.models.categories import Categories

def verify_if_category_exists(category_name: str):

    category = Categories.query.filter_by(name=category_name).first()

    if not category:

        new_category = Categories(name=category_name)
        db.session.add(new_category)
        db.session.commit()

        return new_category

    return category