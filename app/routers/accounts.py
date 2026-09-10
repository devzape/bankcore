from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate, AccountResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/accounts", tags=["Cuentas"])


@router.post("/", response_model=AccountResponse)
def create_account(
    account_data: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_account = Account(
        alias=account_data.alias,
        currency=account_data.currency,
        owner_id=current_user.id,
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


@router.get("/", response_model=list[AccountResponse])
def list_my_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Account).filter(Account.owner_id == current_user.id).all()


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if account.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tenés acceso a esta cuenta")

    return account