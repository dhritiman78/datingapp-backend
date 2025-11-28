import json
from io import BytesIO
from typing import Optional, List

from fastapi import HTTPException

from app.database.redis import redis_client
from app.models.v1.user_model import registerRequest, UpdateRequest
from app.repository.v1.user_repository import enter_user_details_into_DB, get_user_details, update_profile_repository, \
    get_user_selected_fields, delete_user_repository
from app.service.v1.posts_service import delete_all_posts_service
from app.utils.r2 import upload_to_r2, delete_from_r2


async def insert_user_service(registerData: registerRequest, user: dict[str, str]):
   return await enter_user_details_into_DB(registerData,user)

async def update_profile_service(user_id: str, update_data: Optional[UpdateRequest], filename: Optional[str], buffer: Optional[BytesIO]):
    cached_key = f'user/{user_id}'
    try:
        # Upload to R2 if avatar is present
        if filename and buffer:
            previous_avatar = await get_user_selected_fields(user_id, ["avataar"])
            if previous_avatar and previous_avatar != "":
                await delete_from_r2(previous_avatar['avataar'])
            r2_url = await upload_to_r2(buffer, filename)
        else:
            r2_url = None

        # Call repo to update DB
        updated = await update_profile_repository(user_id, update_data, filename)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")

        await redis_client.delete(cached_key)
        return {"message": "Profile updated successfully", "avatar_url": r2_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_user_service(uid: str):
    cached_key = f'user/{uid}'

    # Try from Redis cache
    cached = await redis_client.get(cached_key)
    if cached:
        return json.loads(cached)

    # Fetch from DB
    user_details = await get_user_details(uid)

    # Convert Record to dict and handle datetime fields
    user_dict = dict(user_details)

    # Cache with datetime-safe serialization
    await redis_client.set(cached_key, json.dumps(user_dict, default=str), ex=86400)

    return user_dict

async def get_user_selected_fields_service(user_id: str, fields: List[str]) -> dict:
    user_data = await get_user_selected_fields(user_id, fields)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

async def delete_user_avataar(uuid: str):
    try:
        # 1. Get the avatar field from DB
        user = await get_user_selected_fields(uuid, ["avataar"])
        avatar = user.get("avataar") if user else None

        # 2. No avatar stored
        if not avatar or avatar.strip() == "":
            return {"message": "No avatar found", "deleted": False}

        # 3. Delete from R2
        deleted = await delete_from_r2(avatar)

        if deleted:
            return {"message": "Avatar deleted successfully", "deleted": True}

        else:
            return {"message": "Failed to delete avatar from R2", "deleted": False}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_user_service(uuid: str):
    try:
        # 1. Delete all posts
        posts_deleted = await delete_all_posts_service(uuid)

        # 2. Delete avatar
        avatar_deleted = await delete_user_avataar(uuid)

        # 3. Delete user record from DB
        user_deleted = await delete_user_repository(uuid)

        return {
            "message": "User account deleted successfully",
            "posts_deleted": posts_deleted,
            "avatar_deleted": avatar_deleted,
            "user_deleted": user_deleted
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
