def get_user_profile(user: dict):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "is_active": user["is_active"],
        "created_at": user["created_at"]
    }
