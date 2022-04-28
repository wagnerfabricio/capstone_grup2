from dataclasses import dataclass
from datetime import datetime as dt

from sqlalchemy import Column, DateTime, Integer, String

from app.configs.database import db


@dataclass
class HelloWorld(db.Model):
    id: int
    greeting: str
    visits: str
    last_visit: str

    now = dt.now()

    __tablename__ = "hello_world"

    id: int = Column(Integer, primary_key=True)
    greeting: str = Column(String, nullable=False)
    last_visit: dt = Column(DateTime, default=now)
    visits: int = Column(Integer, default=1)
