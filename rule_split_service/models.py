from sqlalchemy import Column, String, Float, Date
from .database import Base

class Party(Base):
    __tablename__ = "parties"

    # Add lengths to String columns
    party_id = Column(String(64), primary_key=True, index=True)   # ID can be up to 64 chars
    party_name = Column(String(255), nullable=False)              # Name up to 255 chars
    split_rule = Column(String(50), nullable=False)               # "50%" or "1000"
    total_amount = Column(Float, default=0.0)
    date = Column(Date)
