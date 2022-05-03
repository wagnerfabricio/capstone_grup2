from app.models.exception_model import UnauthorizedError
from app.models.user_model import UserModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from os import getenv
from dotenv import load_dotenv


load_dotenv()

def verify_admin_access():
    admin: UserModel = UserModel.query.filter_by(email=get_jwt_identity()["email"]).first()

    if not str(admin.user_class) == getenv("ADMIN_CLASS_ID"):
        raise UnauthorizedError("you are not authorized to access this page")

        # --------------------------- EXCEPTION TO BE USED --------------------------- #
        # except UnauthorizedError as e:
        #     return {"error": e.args[0]}, HTTPStatus.UNAUTHORIZED
