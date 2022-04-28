from app.configs.database import db
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


class UserClassModel(db.Model):
    __tablename__ = 'users_classes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = db.Column(db.String, unique=True, nullable=False)

    