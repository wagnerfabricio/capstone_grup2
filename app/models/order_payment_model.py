from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
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
    type = Column(String(60), nullable=False)
    status = Column(String(60), nullable=False)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)

    # orders = relationship("Order", backref=backref("payment", uselist=False))
