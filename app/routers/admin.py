from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.account import AccountResponse
from app.schemas.transaction import TransactionResponse
from app.core.deps import require_admin
from app.core.audit import log_action

router = APIRouter(prefix="/admin", tags=["Administración"])


@router.get("/accounts", response_model=list[AccountResponse])
def list_all_accounts(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(Account).all()


@router.get("/transactions", response_model=list[TransactionResponse])
def list_all_transactions(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(Transaction).all()


@router.patch("/accounts/{account_id}/freeze", response_model=AccountResponse)
def freeze_account(account_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if account.is_active:
        account.is_active = False
        log_action(db, action="FREEZE_ACCOUNT", detail=f"Cuenta {account.id} congelada", user_id=admin.id)
        db.commit()
        db.refresh(account)

    return account


@router.patch("/accounts/{account_id}/unfreeze", response_model=AccountResponse)
def unfreeze_account(account_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if not account.is_active:
        account.is_active = True
        log_action(db, action="UNFREEZE_ACCOUNT", detail=f"Cuenta {account.id} descongelada", user_id=admin.id)
        db.commit()
        db.refresh(account)

    return account