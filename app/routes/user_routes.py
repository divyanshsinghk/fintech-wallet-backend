from fastapi import APIRouter, Depends
from app.utils.auth_dependency import get_current_user
from app.services.user_service import get_user_profile

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return get_user_profile(current_user)

