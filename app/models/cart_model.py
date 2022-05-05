from dataclasses import dataclass
from email.policy import default
from uuid import uuid4

from datetime import datetime as dt

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Date, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, validates

from app.models.exception_model import TypeFieldError


@dataclass
class Cart(db.Model):
    id: str

    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # products = relationship("Products", secondary="carts_products", backref="carts")
