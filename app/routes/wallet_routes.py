from fastapi import APIRouter, Depends, HTTPException
from app.schemas.transaction_schema import TransactionCreate
from app.services.wallet_service import credit_wallet, debit_wallet
from app.utils.security import get_current_user

router = APIRouter(prefix="/wallet", tags=["Wallet"])

@router.post("/credit")
def credit(data: TransactionCreate, user=Depends(get_current_user)):
    return credit_wallet(user["_id"], data.amount, data.description)

@router.post("/debit")
def debit(data: TransactionCreate, user=Depends(get_current_user)):
    try:
        return debit_wallet(user["_id"], data.amount, data.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
