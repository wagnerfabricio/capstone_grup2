from uuid import uuid4
from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

# carts_products = db.Table(
#     "carts_products",
#     db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
#     db.Column("cart_id", UUID(as_uuid=True), db.ForeignKey("carts.id")),
#     db.Column("product_id", UUID(as_uuid=True), db.ForeignKey("products.id")),
# )


@dataclass
class CartProducts(db.Model):
    id: str
    cart_id: str
    product_id: str

    __tablename__ = "carts_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
