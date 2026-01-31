from datetime import datetime, timedelta, date
from bson import ObjectId
from app.database import transactions_collection
from app.utils.mongo import serialize_mongo



def create_transaction(
    user_id: str,
    tx_type: str,  # CREDIT or DEBIT
    amount: float,
    balance_after: float,
    description: str | None = None,
    session=None
):
    transaction = {
        "user_id": ObjectId(user_id),
        "type": tx_type,
        "amount": amount,
        "balance_after": balance_after,
        "description": description,
        "created_at": datetime.utcnow(),
    }

    if session:
        transactions_collection.insert_one(transaction, session=session)
    else:
        transactions_collection.insert_one(transaction)

    return transaction


def get_user_transactions(user_id: str, limit: int = 20):
    cursor = (
        transactions_collection
        .find({"user_id": ObjectId(user_id)})
        .sort("created_at", -1)
        .limit(limit)
    )

    transactions = []
    for tx in cursor:
        tx["id"] = str(tx["_id"])
        tx.pop("_id", None)
        tx.pop("user_id", None)
        transactions.append(tx)

    return transactions


def get_transaction_statement(
    user_id: str,
    from_date=None,
    to_date=None,
    limit: int = 20,
    skip: int = 0
):
    query = {"user_id": ObjectId(user_id)}

    if from_date or to_date:
        query["created_at"] = {}

        if from_date:
           
            if isinstance(from_date, date):
                start = datetime.combine(from_date, datetime.min.time())
            else:
                start = from_date

            query["created_at"]["$gte"] = start

        if to_date:
            
            if isinstance(to_date, date):
                end = datetime.combine(to_date, datetime.min.time()) + timedelta(days=1)
            else:
                end = to_date + timedelta(days=1)

            query["created_at"]["$lt"] = end

    cursor = (
        transactions_collection
        .find(query)
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )

    results = []

    for tx in cursor:
        tx["id"] = str(tx["_id"])
        tx.pop("_id", None)

        if "user_id" in tx:
            tx.pop("user_id")

        if "wallet_id" in tx:
            tx.pop("wallet_id")

        results.append(tx)

    return results

def get_transaction_statement_summary(
    user_id: str,
    from_date: datetime,
    to_date: datetime,
    limit: int = 50,
    skip: int = 0
):
    pipeline = [
        {
            "$match": {
                "user_id": ObjectId(user_id),
                "created_at": {
                    "$gte": from_date,
                    "$lt": to_date
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_credit": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "CREDIT"]},
                            "$amount",
                            0
                        ]
                    }
                },
                "total_debit": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "DEBIT"]},
                            "$amount",
                            0
                        ]
                    }
                },
                "count": {"$sum": 1}
            }
        }
    ]

    result = list(transactions_collection.aggregate(pipeline))

    if not result:
        return {
            "total_credit": 0,
            "total_debit": 0,
            "count": 0
        }

    summary = result[0]

    summary.pop("_id", None)

    return summary

def get_transaction_statement_paginated(
    user_id: str,
    from_date=None,
    to_date=None,
    limit: int = 20,
    skip: int = 0
):
    query = {"user_id": ObjectId(user_id)}

    if from_date or to_date:
        query["created_at"] = {}
        if from_date:
            query["created_at"]["$gte"] = from_date
        if to_date:
            query["created_at"]["$lt"] = to_date

    total = transactions_collection.count_documents(query)

    cursor = (
        transactions_collection
        .find(query)
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )

    items = []
    for tx in cursor:
        tx["id"] = str(tx["_id"])
        tx.pop("_id", None)
        tx.pop("user_id", None)

    # 🔥 THIS LINE FIXES EVERYTHING
        tx = serialize_mongo(tx)
        items.append(tx)


    return {
        "items": items,
        "total": total,
        "limit": limit,
        "skip": skip,
        "has_next": skip + limit < total,
        "has_previous": skip > 0
    }