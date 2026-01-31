from bson import ObjectId
from datetime import datetime
from app.database import transactions_collection

def transaction_summary(user_id: str, from_date: datetime, to_date: datetime):
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
                "_id": "$type",
                "total_amount": {"$sum": "$amount"},
                "count": {"$sum": 1}
            }
        }
    ]

    result = list(transactions_collection.aggregate(pipeline))

    summary = {
        "total_credit": 0,
        "total_debit": 0,
        "credit_count": 0,
        "debit_count": 0,
        "net_flow": 0
    }

    for r in result:
        if r["_id"] == "CREDIT":
            summary["total_credit"] = r["total_amount"]
            summary["credit_count"] = r["count"]
        elif r["_id"] == "DEBIT":
            summary["total_debit"] = r["total_amount"]
            summary["debit_count"] = r["count"]

    summary["net_flow"] = summary["total_credit"] - summary["total_debit"]

    return summary
