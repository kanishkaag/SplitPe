from pydantic import BaseModel
from datetime import datetime,date

# ----- Party -----
class PartyCreate(BaseModel):
    party_id: str
    party_name: str
    split_rule: str
  

class PartyResponse(BaseModel):
    party_id: str
    party_name: str
    split_rule: str
    total_amount: float

    class Config:
        orm_mode = True

# ----- Wallet Credit (Split Event) -----
class WalletCreditRequested(BaseModel):
    party_id: str
    amount: float
    order_id: str

class SplitResponse(BaseModel):
    id: int
    party_id: str
    order_id: str
    amount: float
    timestamp: datetime

    class Config:
        orm_mode = True
