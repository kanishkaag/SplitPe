from pydantic import BaseModel

class OrderCreate(BaseModel):
    idempotency_key: str
    order_id: str
    total_amount: float
