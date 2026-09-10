from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BankCore",
    description="Motor de cuentas y transacciones estilo fintech",
    version="0.1.0",
)

app.include_router(auth.router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "BankCore"}