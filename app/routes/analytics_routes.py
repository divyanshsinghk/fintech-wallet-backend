from fastapi import APIRouter, Depends, Query
from datetime import date, datetime, timedelta
from app.utils.security import get_current_user
from app.services.analytics_service import transaction_summary

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def analytics_summary(
    from_date: date = Query(...),
    to_date: date = Query(...),
    current_user=Depends(get_current_user)
):
    start = datetime.combine(from_date, datetime.min.time())
    end = datetime.combine(to_date, datetime.min.time()) + timedelta(days=1)

    return transaction_summary(
        user_id=str(current_user["_id"]),
        from_date=start,
        to_date=end
    )
