from pydantic import BaseModel
from datetime import date

class PartyBase(BaseModel):
    party_id: str
    party_name: str
    split_rule: str
    date: date

class PartyCreate(PartyBase):
    pass

class PartyResponse(PartyBase):
    total_amount: float

    class Config:
        orm_mode = True

class SplitResult(BaseModel):
    party_id: str
    amount: float
    order_id: str
