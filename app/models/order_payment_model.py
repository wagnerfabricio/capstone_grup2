from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from app.configs.database import db


@dataclass
class OrderPayment(db.Model):
    id: str
    type: str
    status: str

    __tablename__ = "orders_payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(60), nullable=False, unique=True)
    status = Column(String(60))
