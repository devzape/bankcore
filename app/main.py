from fastapi import FastAPI
from app.database import Base, engine
import app.models
from app.routers import auth, accounts, transactions
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BankCore",
    description="Motor de cuentas y transacciones estilo fintech",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)