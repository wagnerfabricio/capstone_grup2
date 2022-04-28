from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, String,Integer
from sqlalchemy.dialects.postgresql import UUID

from app.configs.database import db


@dataclass
class OrderStatus(db.Model):
    id: str
    type: str

    __tablename__ = "orders_status"

    id = Column(Integer, primary_key=True)
    type = Column(String(30), nullable=False)
