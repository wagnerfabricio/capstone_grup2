from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

@dataclass
class AddressesModel(db.Model):
    id: str
    street: str
    number: int
    info: str
    district: str
    city: str
    state: str
    country: str
    cep: str

    __tablename__ = "addresses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    street = Column(String(100), nullable=False)
    number = Column(Integer, nullable=False)
    info = Column(String(100))
    district = Column(String(60), nullable=False)
    city = Column(String(58), nullable=False, default="Recife")
    state = Column(String(58), nullable=False, default="Pernambuco")
    country = Column(String(100), nullable=False, default="Brasil")
    cep = Column(String(9), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)