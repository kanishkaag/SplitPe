from sqlalchemy import Column, BigInteger, String, DECIMAL, Boolean, TIMESTAMP, text
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    idempotency_key = Column(String(100), unique=True, nullable=False)
    order_id = Column(String(64), unique=True, nullable=False)
    total_amount = Column(DECIMAL(14,2), nullable=False)
    split_status = Column(Boolean, default=False, nullable=False)
    date_created = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
