from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.configs.database import db


@dataclass
class OrderProduct(db.Model):
    id: str
    product_quantity: int
    discount: float
    sub_total: float

    __tablename__ = "order_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_quantity = Column(Integer, default=1)
    discount = Column(Numeric, default=0)
    sub_total = Column(Numeric)

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    ## Está comentada pois ainda não existe a tabela products
    # product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
