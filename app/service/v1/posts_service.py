from io import BytesIO

from fastapi import UploadFile, HTTPException

from app.repository.v1.posts_repository import upload_user_post, fetch_user_posts
from app.utils.r2 import upload_to_r2


async def upload_posts_service (user_uid: str, picture: str, caption: str, buffer: BytesIO):
    try:
        await upload_to_r2(buffer, picture)

        await upload_user_post(user_uid, picture, caption)

        return {"message": "Successfully posted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_posts_service (user_uid: str):
    try:
        return await fetch_user_posts(user_uid)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))