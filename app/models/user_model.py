import re
from uuid import uuid4

from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from app.configs.database import db
from app.models.exception_model import InvalidEmailError, InvalidPasswordError

from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass


@dataclass
class UserModel(db.Model):
    email: str
    name: str

    __tablename__ = "users"
    expected_keys = {"name", "email", "password"}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.DateTime)
    # address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    user_class = db.Column(UUID(as_uuid=True), db.ForeignKey("users_classes.id"))

    # orders = db.relationship('OrderModel', backref=db.backref('users', uselist=False))
    # cart = db.relationship('CartModel', backref=db.backref('users', uselist=False))

    @validates("email")
    def validate_email(self, key, email_to_be_validated):
        pattern = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

        if not re.fullmatch(pattern, email_to_be_validated):
            raise InvalidEmailError("Invalid email address")

        return email_to_be_validated.lower()

    @validates("name")
    def validate_name(self, key, name_to_be_validated):
        return name_to_be_validated.title()

    @property
    def password(self):
        raise AttributeError("You cannot access the password attribute")

    @password.setter
    def password(self, password_to_hash):
        if not password_to_hash or len(password_to_hash) < 4:
            raise InvalidPasswordError(
                "Field password must be at least 4 characters long"  # todo: mudar para 8 no projeto final!
            )

        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
