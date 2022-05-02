from dataclasses import dataclass
from uuid import uuid4

from datetime import datetime as dt

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Date, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref


@dataclass
class Order(db.Model):
    id: str
    status: dict
 

    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=dt.now())
    total = Column(Numeric(asdecimal=False))

    status_id = Column(
        UUID(as_uuid=True), ForeignKey("orders_status.id"), nullable=False
    )

    rating_id = Column(UUID(as_uuid=True), ForeignKey("orders_ratings.id"), unique=True)
    payment_id = Column(
        UUID(as_uuid=True), ForeignKey("orders_payments.id"), nullable=False
    )

    user = relationship(
        "UserModel", backref=backref("orders", uselist=True), uselist=False
    )
    status = relationship("OrderStatus", uselist=False)
    rating = relationship("OrderRating", uselist=False)
    payment = relationship("OrderPayment", uselist=False)
