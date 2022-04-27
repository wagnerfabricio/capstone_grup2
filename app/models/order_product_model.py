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
    total: float

    __tablename__ = "orders_products"

    id = Column(
        # UUID(as_uuid=True), 
       Integer, primary_key=True
    #    , default=uuid4
       )
    product_quantity = Column(Integer, default=1)
    discount = Column(Numeric(asdecimal=False), default=0)
    total = Column(Numeric(asdecimal=False))

    order_id = Column(
        # UUID(as_uuid=True), 
        Integer,ForeignKey("orders.id"), nullable=False)
    ## Está comentada pois ainda não existe a tabela products
    product_id = Column(
        # UUID(as_uuid=True), 
        Integer,ForeignKey("products.id"), nullable=False)
