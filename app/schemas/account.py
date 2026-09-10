from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    alias: str = Field(min_length=1, max_length=50)
    currency: str = "ARS"


class AccountResponse(BaseModel):
    id: int
    alias: str
    balance: float
    currency: str
    is_active: bool

    class Config:
        from_attributes = True