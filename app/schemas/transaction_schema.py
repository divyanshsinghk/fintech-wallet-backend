from pydantic import BaseModel, Field
from typing import Optional
from typing import Literal
from datetime import datetime


class TransactionCreate(BaseModel):
    amount: float
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    type: str  # CREDIT or DEBIT
    amount: float
    balance_after: float
    description: Optional[str]
    created_at: datetime

class TransactionStatementQuery(BaseModel):
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    limit: int = 20
    skip: int = 0