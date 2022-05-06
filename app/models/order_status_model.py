from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from app.configs.database import db
from app.models.exception_model import TypeFieldError


@dataclass
class OrderStatus(db.Model):
    id: str
    type: str

    __tablename__ = "orders_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(30), nullable=False, unique=True)

    @validates("type")
    def validate_type(self, key, field):
        if type(field) != str:
            raise TypeFieldError("string", key)

        return field.capitalize()
