from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, validates

from app.configs.database import db
from app.models.exception_model import TypeFieldError


@dataclass
class OrderPayment(db.Model):
    id: str
    type: str

    __tablename__ = "orders_payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(60), nullable=False, unique=True)

    @validates("type")
    def validate_field_type(self, key, field):
        if not type(field) is str:
            raise TypeFieldError("string",key)

        return field.title()
