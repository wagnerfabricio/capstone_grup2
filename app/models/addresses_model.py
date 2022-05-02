from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String

@dataclass
class AddressesModel(db.Model):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    cep = Column(String(9), nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(58), nullable=False)
    info = Column(String(100), nullable=False)
    district = Column(String(60), nullable=False)
    number = Column(Integer, nullable=False)

