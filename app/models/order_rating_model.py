from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from app.configs.database import db
from app.models.exception_model import TypeFieldError


@dataclass
class OrderRating(db.Model):
    id: str
    rating: int
    comment: str

    __tablename__ = "orders_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    rating = Column(Integer, nullable=False)
    comment = Column(String(200))

    @validates("rating")
    def validate_type_rating(self, key, field):
        if type(field) != int:
            raise TypeFieldError("integer", key)

        return field

    @validates("comment")
    def validate_type_comment(self, key, field):
        if type(field) != str:
            raise TypeFieldError("string", key)

        return field.capitalize()
