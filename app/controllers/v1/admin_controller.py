import os
from fastapi import HTTPException, status
from app.service.v1.user_service import delete_user_service

ADMIN_KEY = os.getenv("ADMIN_KEY")   # Load from .env


async def delete_user_controller(uuid: str, admin_key: str):
    # 1. Validate admin key
    if not admin_key or admin_key != ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid admin key."
        )

    # 2. If authorized, delete the user
    return await delete_user_service(uuid)
