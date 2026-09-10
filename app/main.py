from fastapi import FastAPI

app = FastAPI(
    title="BankCore",
    description="Motor de cuentas y transacciones estilo fintech",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "BankCore"}