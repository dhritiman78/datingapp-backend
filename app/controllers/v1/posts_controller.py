from datetime import datetime
from typing import Optional

from fastapi import UploadFile

from app.service.v1.posts_service import upload_posts_service, get_posts_service
from app.service.v1.relations_service import get_user_relations_service
from app.utils.compress_image import compress_image


async def upload_posts_controllers (user_uid: str, picture: UploadFile, caption: str):
        contents = await picture.read()
        compressed_buffer = await compress_image(contents)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"user_posts/{user_uid}_post_{timestamp}.jpg"

        return await upload_posts_service(user_uid,filename,caption,compressed_buffer)

async def get_user_posts_controllers(user_uid: str, target_uid: Optional[str]):
    if target_uid:
        relations = await get_user_relations_service(user_uid, target_uid)
        if relations.get("is_blocked"):
            return []
        return await get_posts_service(target_uid)

    return await get_posts_service(user_uid)
