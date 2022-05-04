from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

@dataclass
class PaymentModel(db.Model):
    id: str
    type: str
    status: str
    mercadopago_id: str
    mercadopago_type: str

    money_status = ["Aguardando Pagamento", ""]

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = db.Column(db.String(60), default='dinheiro')
    status = db.Column(db.String(50), default='Aguardando Pagamento')
    mercadopago_id = db.Column(db.String(60), unique=True)
    mercadopago_type = db.Column(db.String(50))
    
