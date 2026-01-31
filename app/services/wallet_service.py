from datetime import datetime
from app.database import wallets_collection, transactions_collection
from app.utils.security import get_current_user
from app.services.transaction_service import create_transaction


def credit_wallet(user_id, amount: float, description: str = "Credit"):
    wallet = wallets_collection.find_one({"user_id": user_id})

    new_balance = wallet["balance"] + amount

    wallets_collection.update_one(
        {"_id": wallet["_id"]},
        {"$set": {"balance": new_balance, "updated_at": datetime.utcnow()}}
    )

    transactions_collection.insert_one({
        "user_id": user_id,
        "wallet_id": wallet["_id"],
        "type": "CREDIT",
        "amount": amount,
        "balance_after": new_balance,
        "description": description,
        "created_at": datetime.utcnow()
    })

    return {"balance": new_balance}


def debit_wallet(user_id, amount: float, description: str = "Debit"):
    wallet = wallets_collection.find_one({"user_id": user_id})

    if wallet["balance"] < amount:
        raise ValueError("Insufficient balance")

    new_balance = wallet["balance"] - amount

    wallets_collection.update_one(
        {"_id": wallet["_id"]},
        {"$set": {"balance": new_balance, "updated_at": datetime.utcnow()}}
    )

    transactions_collection.insert_one({
        "user_id": user_id,
        "wallet_id": wallet["_id"],
        "type": "DEBIT",
        "amount": amount,
        "balance_after": new_balance,
        "description": description,
        "created_at": datetime.utcnow()
    })

    return {"balance": new_balance}
