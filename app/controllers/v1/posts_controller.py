from datetime import datetime

from fastapi import UploadFile

from app.service.v1.posts_service import upload_posts_service
from app.utils.compress_image import compress_image


async def upload_posts_controllers (user_uid: str, picture: UploadFile, caption: str):
        contents = await picture.read()
        compressed_buffer = await compress_image(contents)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"user_posts/{user_uid}_post_{timestamp}.jpg"

        return await upload_posts_service(user_uid,filename,caption,compressed_buffer)