from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.configs.database import db


@dataclass
class OrderStatus(db.Model):
    id: str
    type: str

    __tablename__ = "order_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(30), nullable=False)
