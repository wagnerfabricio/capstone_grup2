from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.configs.database import db


@dataclass
class OrderRating(db.Model):
    id: str
    nota: int
    comment: str

    __tablename__ = "order_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nota = Column(Integer, nullable=False)
    comment = Column(String(200))
