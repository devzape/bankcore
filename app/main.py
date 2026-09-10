from fastapi import FastAPI
from app.database import Base, engine
import app.models
from app.routers import auth, accounts, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BankCore",
    description="Motor de cuentas y transacciones estilo fintech",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)