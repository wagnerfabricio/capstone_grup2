from email.policy import default
from app.configs.database import db
from sqlalchemy import Column, String,Integer
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

@dataclass
class Categories(db.Model):

    name: str

    __tablename__ = "categories"

    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    id = db.Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    product = db.relationship("Products", back_populates="category", uselist=True)