from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    movements = relationship("Movement", back_populates="transaction")


class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)  # negativo = débito, positivo = crédito
    balance_after = Column(Float, nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)

    account = relationship("Account")
    transaction = relationship("Transaction", back_populates="movements")