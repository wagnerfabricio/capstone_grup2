from dataclasses import dataclass
from uuid import uuid4

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID


@dataclass
class Cart(db.Model):

    id: str
    subtotal: float
    total: float

    __tablename__ = "carts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=False)
    subtotal = Column(Numeric(asdecimal=False))
    total = Column(Numeric(asdecimal=False))
