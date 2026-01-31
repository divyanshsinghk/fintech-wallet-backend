from fastapi import APIRouter, Depends
from app.schemas.transfer_schema import TransferCreate, TransferResponse
from app.services.transfer_service import transfer_money
from app.utils.security import get_current_user

router = APIRouter(prefix="/transfer", tags=["Transfers"])

@router.post("/", response_model=TransferResponse)
def transfer(
    data: TransferCreate,
    current_user=Depends(get_current_user)
):
    return transfer_money(
        sender_id=str(current_user["_id"]),
        receiver_email=data.receiver_email,
        amount=data.amount,
        description=data.description,
        idempotency_key=data.idempotency_key
    )
