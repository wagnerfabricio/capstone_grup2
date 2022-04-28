from email.policy import default
from enum import unique
from xmlrpc.client import Boolean
from app.configs.database import db
from sqlalchemy import Column, Integer, Numeric, String, DateTime, Boolean
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

@dataclass
class Products(db.Model):

    name: str
    description: str
    price: str
    active: bool
    qtt_stock: int
    category_id: int

    __tablename__ = "products"

    id = db.Column(
        # UUID(as_uuid=True), 
        Integer,primary_key=True
        # , default=uuid4
        )
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)
    price = Column(Numeric(asdecimal=False), nullable=False)
    active = Column(Boolean)
    qtt_stock = Column(Integer)

    category_id = db.Column(
        # UUID(as_uuid=True), 
        Integer,db.ForeignKey("categories.id"))

    category = db.relationship("Categories", back_populates="product", uselist=False)

