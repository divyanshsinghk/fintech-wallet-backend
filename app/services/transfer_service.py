from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from app.database import db, get_session
from app.services.transaction_service import create_transaction

# collection for idempotency
idempotency = db["idempotency_keys"]


def transfer_money(
    sender_id: str,
    receiver_email: str,
    amount: float,
    description: str,
    idempotency_key: str
):
    users = db["users"]
    wallets = db["wallets"]

    
    # VALIDATIONS

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if amount > 100000:
        raise HTTPException(status_code=400, detail="Transfer limit exceeded")

   
    # IDEMPOTENCY CHECK

    existing = idempotency.find_one({"key": idempotency_key})
    if existing:
        return existing["response"]

    
    # RECEIVER CHECK
    
    receiver = users.find_one({"email": receiver_email})
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    if str(receiver["_id"]) == sender_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to yourself")

    
    # ATOMIC TRANSACTION
  
    session = get_session()

    with session.start_transaction():
        sender_oid = ObjectId(sender_id)
        receiver_oid = receiver["_id"]

        sender_wallet = wallets.find_one(
            {"user_id": sender_oid},
            session=session
        )

        receiver_wallet = wallets.find_one(
            {"user_id": receiver_oid},
            session=session
        )

        if not sender_wallet:
            raise HTTPException(status_code=404, detail="Sender wallet not found")

        if not receiver_wallet:
            receiver_wallet = {
                "user_id": receiver_oid,
                "balance": 0,
                "currency": "INR",
                "status": "ACTIVE",
                "created_at": datetime.utcnow()
            }
            wallets.insert_one(receiver_wallet, session=session)
            receiver_wallet["balance"] = 0

        if sender_wallet["balance"] < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # ---- Debit sender ----
        sender_new_balance = sender_wallet["balance"] - amount
        wallets.update_one(
            {"_id": sender_wallet["_id"]},
            {"$set": {"balance": sender_new_balance}},
            session=session
        )

        create_transaction(
            user_id=str(sender_oid),
            tx_type="DEBIT",
            amount=amount,
            balance_after=sender_new_balance,
            description=f"Transfer to {receiver_email}",
            session=session
        )

        # ---- Credit receiver ----
        receiver_new_balance = receiver_wallet["balance"] + amount
        wallets.update_one(
            {"user_id": receiver_oid},
            {"$set": {"balance": receiver_new_balance}},
            session=session
        )

        create_transaction(
            user_id=str(receiver_oid),
            tx_type="CREDIT",
            amount=amount,
            balance_after=receiver_new_balance,
            description=f"Transfer from {sender_id}",
            session=session
        )

   
    # STORE IDEMPOTENCY RESULT
    
    result = {
        "sender_balance": sender_new_balance,
        "receiver_balance": receiver_new_balance
    }

    idempotency.insert_one({
        "key": idempotency_key,
        "response": result,
        "created_at": datetime.utcnow()
    })

    return result
