from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

@dataclass
class AddressesModel(db.Model):
    __tablename__ = "addresses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    street = Column(String(100), nullable=False)
    cep = Column(String(9), nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(58), nullable=False)
    info = Column(String(100))
    district = Column(String(60), nullable=False)
    number = Column(Integer, nullable=False)

