from dataclasses import dataclass
from uuid import uuid4

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID


@dataclass
class CartProducts(db.Model):

    id: str
    subtotal: float

    __tablename__ = "carts_products"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cart_id = Column(
        UUID(as_uuid=True), ForeignKey(
            "carts.id"), nullable=False)
    product_id = Column(
        # UUID(as_uuid=True),
        Integer,
        ForeignKey(
            "products.id"), nullable=False)
    product_quantity = Column(Integer, default=1)
    discount = Column(Numeric, default=0)
    subtotal = Column(Numeric(asdecimal=False))
