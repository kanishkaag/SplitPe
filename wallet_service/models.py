from sqlalchemy import Column, String, Float, Date , BigInteger , DECIMAL ,Boolean ,TIMESTAMP, text, Integer, ForeignKey, DateTime, func
from .database import Base

class Party(Base):
    __tablename__ = "parties"

    # Add lengths to String columns
    party_id = Column(String(64), primary_key=True, index=True)   # ID can be up to 64 chars
    party_name = Column(String(255), nullable=False)              # Name up to 255 chars
    split_rule = Column(String(50), nullable=False)               # "50%" or "1000"
    total_amount = Column(Float, default=0.0)
    date = Column(Date)


class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    idempotency_key = Column(String(100), unique=True, nullable=False)
    order_id = Column(String(64), unique=True, nullable=False)
    total_amount = Column(DECIMAL(14,2), nullable=False)
    split_status = Column(Boolean, default=False, nullable=False)
    date_created = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

class Split(Base):
    __tablename__ = "splits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    party_id = Column(String(50), ForeignKey("parties.party_id"))
    order_id = Column(String(50), ForeignKey("orders.order_id"))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())    