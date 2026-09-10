from pydantic import BaseModel, Field
from datetime import datetime


class TransferCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float = Field(gt=0)
    description: str = ""


class MovementResponse(BaseModel):
    id: int
    amount: float
    balance_after: float
    account_id: int

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    created_at: datetime
    movements: list[MovementResponse]

    class Config:
        from_attributes = True

class DepositCreate(BaseModel):
    account_id: int
    amount: float = Field(gt=0)
    description: str = ""