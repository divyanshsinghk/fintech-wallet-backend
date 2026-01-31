from fastapi import APIRouter, Depends, Query
from datetime import date, datetime, timedelta
from typing import List
from datetime import datetime
from app.schemas.transaction_schema import TransactionResponse
from app.services.transaction_service import (
    get_user_transactions,
    get_transaction_statement,
    get_transaction_statement_summary,
)
from app.utils.security import get_current_user
from fastapi.responses import StreamingResponse
from app.services.transaction_export_service import export_transactions_csv
from app.services.transaction_service import get_transaction_statement_paginated



router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get(
    "/me",
    response_model=List[TransactionResponse],
)
def my_transactions(user=Depends(get_current_user)):
    return get_user_transactions(str(user["_id"]))

@router.get("/statement")
def transaction_statement(
    from_date: datetime | None = Query(None),
    to_date: datetime | None = Query(None),
    limit: int = Query(20, le=100),
    skip: int = Query(0),
    current_user=Depends(get_current_user)
):
    return get_transaction_statement(
        user_id=str(current_user["_id"]),
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        skip=skip
    )

@router.get("/statement/summary")
def transaction_statement_summary(
    from_date: date,
    to_date: date,
    limit: int = 50,
    skip: int = 0,
    current_user=Depends(get_current_user)
):
    start = datetime.combine(from_date, datetime.min.time())
    end = datetime.combine(to_date, datetime.min.time()) + timedelta(days=1)

    return get_transaction_statement_summary(
        user_id=str(current_user["_id"]),
        from_date=start,
        to_date=end,
        limit=limit,
        skip=skip
    )

@router.get("/statement/export")
def export_statement_csv(
    from_date: datetime | None = Query(None),
    to_date: datetime | None = Query(None),
    current_user=Depends(get_current_user)
):
    csv_file = export_transactions_csv(
        user_id=str(current_user["_id"]),
        from_date=from_date,
        to_date=to_date
    )

    filename = f"transaction_statement_{datetime.utcnow().date()}.csv"

    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@router.get("/statement/paginated")
def transaction_statement_paginated(
    from_date: datetime | None = Query(None),
    to_date: datetime | None = Query(None),
    limit: int = Query(20, le=100),
    skip: int = Query(0),
    current_user=Depends(get_current_user)
):
    return get_transaction_statement_paginated(
        user_id=str(current_user["_id"]),
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        skip=skip
    )
