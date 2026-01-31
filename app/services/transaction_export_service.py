import csv
from io import StringIO
from bson import ObjectId
from datetime import datetime
from app.database import transactions_collection


def export_transactions_csv(
    user_id: str,
    from_date: datetime | None,
    to_date: datetime | None
):
    query = {"user_id": ObjectId(user_id)}

    if from_date or to_date:
        query["created_at"] = {}
        if from_date:
            query["created_at"]["$gte"] = from_date
        if to_date:
            query["created_at"]["$lt"] = to_date

    cursor = transactions_collection.find(query).sort("created_at", -1)

    output = StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "Date",
        "Type",
        "Amount",
        "Balance After",
        "Description"
    ])

    for tx in cursor:
        writer.writerow([
            tx["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
            tx["type"],
            tx["amount"],
            tx["balance_after"],
            tx.get("description", "")
        ])

    output.seek(0)
    return output