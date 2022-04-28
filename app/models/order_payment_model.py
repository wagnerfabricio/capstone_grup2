from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from app.configs.database import db


@dataclass
class OrderPayment(db.Model):
    id: str
    type: str
    status: str

    __tablename__ = "orders_payments"

    id = Column(Integer, primary_key=True)
    type = Column(String(60), nullable=False)
    status = Column(String(60), nullable=False)

    # orders = relationship("Order", backref=backref("payment", uselist=False))
