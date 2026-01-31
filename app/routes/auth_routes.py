from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate):
    try:
        return register_user(user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return login_user(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

