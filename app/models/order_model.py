from dataclasses import dataclass
from uuid import uuid4

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref


@dataclass
class Order(db.Model):
    id: str
    status: str
    # date: str
    # subtotal: float
    # total: float

    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    ## Está comentada pois ainda nao existe a tabela users
    # user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status_id = Column(
        UUID(as_uuid=True), ForeignKey("orders_status.id"), nullable=False
    )
    rating_id = Column(
        UUID(as_uuid=True), ForeignKey("orders_ratings.id"), nullable=False
    )
    date = Column(Date)
    subtotal = Column(Numeric(asdecimal=False))
    total = Column(Numeric(asdecimal=False))
    payment_id = Column(
        UUID(as_uuid=True), ForeignKey("orders_payments.id"), nullable=False
    )

    user = relationship(
        "UserModel", backref=backref("orders", uselist=True), uselist=False
    )

    status = relationship("OrderStatus", uselist=False)
    rating = relationship("OrderRating", uselist=False)
    payment = relationship("OrderPayment", uselist=False)
