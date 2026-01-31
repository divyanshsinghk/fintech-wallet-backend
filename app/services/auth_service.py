from app.database import users_collection, wallets_collection
from app.utils.security import hash_password, verify_password, create_access_token
from datetime import datetime


def register_user(email: str, password: str):
    existing = users_collection.find_one({"email": email})
    if existing:
        raise ValueError("User already exists")

    user = {
        "email": email,
        "password_hash": hash_password(password),
        "created_at": datetime.utcnow(),
        "is_active": True
    }

    result = users_collection.insert_one(user)

    wallet = {
        "user_id": result.inserted_id,
        "balance": 0.0,
        "currency": "INR",
        "status": "ACTIVE",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    wallets_collection.insert_one(wallet)

    return {"message": "User registered successfully"}


def login_user(email: str, password: str):
    user = users_collection.find_one({"email": email})

    if not user or not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}
