from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction, Movement
from app.models.user import User
from app.schemas.transaction import TransferCreate, TransactionResponse
from app.core.deps import get_current_user

from app.schemas.transaction import DepositCreate

router = APIRouter(prefix="/transactions", tags=["Transacciones"])


@router.post("/transfer", response_model=TransactionResponse)
def transfer(
    data: TransferCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if data.from_account_id == data.to_account_id:
        raise HTTPException(status_code=400, detail="No se puede transferir a la misma cuenta")

    from_account = db.query(Account).filter(Account.id == data.from_account_id).with_for_update().first()
    to_account = db.query(Account).filter(Account.id == data.to_account_id).with_for_update().first()

    if not from_account or not to_account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if from_account.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="La cuenta de origen no te pertenece")

    if not from_account.is_active or not to_account.is_active:
        raise HTTPException(status_code=403, detail="Una de las cuentas está inactiva")

    if from_account.balance < data.amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    # Actualizar saldos
    from_account.balance -= data.amount
    to_account.balance += data.amount

    # Crear la transacción "paraguas"
    new_transaction = Transaction(amount=data.amount, description=data.description)
    db.add(new_transaction)
    db.flush()  # para que new_transaction.id ya exista, sin cerrar la transacción de DB

    # Crear los dos movimientos (doble entrada)
    debit = Movement(
        amount=-data.amount,
        balance_after=from_account.balance,
        account_id=from_account.id,
        transaction_id=new_transaction.id,
    )
    credit = Movement(
        amount=data.amount,
        balance_after=to_account.balance,
        account_id=to_account.id,
        transaction_id=new_transaction.id,
    )
    db.add_all([debit, credit])

    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.post("/deposit", response_model=TransactionResponse)
def deposit(
    data: DepositCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = db.query(Account).filter(Account.id == data.account_id).with_for_update().first()

    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if account.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Esa cuenta no te pertenece")

    if not account.is_active:
        raise HTTPException(status_code=403, detail="La cuenta está inactiva")

    account.balance += data.amount

    new_transaction = Transaction(amount=data.amount, description=data.description or "Depósito")
    db.add(new_transaction)
    db.flush()

    credit = Movement(
        amount=data.amount,
        balance_after=account.balance,
        account_id=account.id,
        transaction_id=new_transaction.id,
    )
    db.add(credit)

    db.commit()
    db.refresh(new_transaction)
    return new_transaction