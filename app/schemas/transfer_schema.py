from pydantic import BaseModel, Field
from typing import Optional

class TransferCreate(BaseModel):
    receiver_email: str
    amount: float
    description: str | None = None
    idempotency_key: str

class TransferResponse(BaseModel):
    sender_balance: float
    receiver_balance: float
