from http import HTTPStatus
from flask import jsonify, request
from app.models.exception_model import InvalidEmailError, InvalidPasswordError
from app.models.user_model import UserModel
from app.configs.database import db
from sqlalchemy.exc import IntegrityError

from datetime import timedelta

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


def create_user():
    data = request.get_json()
    try:
        new_user: UserModel = UserModel(**data)
        db.session.add(new_user)
        db.session.commit()

    except IntegrityError as e:
        return {
            "error": e.args[0]
            .split("Key (", 1)[-1]
            .replace("(", " ")
            .replace(")", " ")
            .replace("\n", "")
        }, HTTPStatus.CONFLICT

    except InvalidPasswordError as e:
        return {"error": e.args[0]}

    except InvalidEmailError as e:
        return {"error": e.args[0]}

    return jsonify(new_user), HTTPStatus.OK


def signin():
    data = request.get_json()

    user: UserModel = UserModel.query.filter_by(email=data["email"]).first()

    # if not user or not user.verify_password(data["password"]):
    #     return {"error": "Invalid email or password"}, HTTPStatus.UNAUTHORIZED

    token = create_access_token(user, expires_delta=timedelta(days=30))

    return {"access_token": token}, HTTPStatus.OK
