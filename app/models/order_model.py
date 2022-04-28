from dataclasses import dataclass
from uuid import uuid4

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Date, Numeric,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref


@dataclass
class Order(db.Model):
    id: str
    status: dict
    # date: str
    # subtotal: float
    # total: float

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date)
    subtotal = Column(Numeric(asdecimal=False))
    total = Column(Numeric(asdecimal=False))
    
    status_id = Column(
        # UUID(as_uuid=True),
         Integer,
         ForeignKey("orders_status.id"), nullable=False
    )
    rating_id = Column(
        # UUID(as_uuid=True),
         Integer,ForeignKey("orders_ratings.id")
    )
    payment_id = Column(
        # UUID(as_uuid=True),
         Integer,ForeignKey("orders_payments.id"), nullable=False
    )

    user = relationship(
        "UserModel", backref=backref("orders", uselist=True), uselist=False
    )
    status = relationship("OrderStatus", uselist=False)
    rating = relationship("OrderRating", uselist=False)
    payment = relationship("OrderPayment", uselist=False)
