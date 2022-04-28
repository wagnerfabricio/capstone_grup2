from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.configs.database import db


@dataclass
class OrderProduct(db.Model):
    id: str
    discount: float
    sale_value: float

    __tablename__ = "orders_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    discount = Column(Numeric(asdecimal=False), default=0)
    sale_value = Column(Numeric(asdecimal=False))

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
