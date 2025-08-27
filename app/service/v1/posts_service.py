import json
from io import BytesIO

from fastapi import UploadFile, HTTPException

from app.database.redis import redis_client
from app.repository.v1.posts_repository import upload_user_post, fetch_user_posts, delete_user_post, fetch_user_feed
from app.utils.r2 import upload_to_r2, delete_from_r2


async def upload_posts_service (user_uid: str, picture: str, caption: str, buffer: BytesIO):
    try:
        cached_key = f"posts/{user_uid}"
        await upload_to_r2(buffer, picture)

        await upload_user_post(user_uid, picture, caption)

        await redis_client.delete(cached_key)

        return {"message": "Successfully posted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_posts_service (user_uid: str):
    try:
        cached_key = f"posts/{user_uid}"
        cached = await redis_client.get(cached_key)
        if cached:
            return json.loads(cached)
        return await fetch_user_posts(user_uid)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_user_post_service(user_uid: str, post_id: int):
    try:
        cached_key = f"posts/{user_uid}"

        # Call repo to delete post in DB and get deleted row
        deleted_post = await delete_user_post(user_uid, post_id)

        if not deleted_post:
            raise HTTPException(
                status_code=404,
                detail=f"Post {post_id} not found for user {user_uid}"
            )

        # Delete cached posts for this user
        await redis_client.delete(cached_key)

        # Delete the picture from R2 storage
        if deleted_post.get("deleted_picture"):
            await delete_from_r2(deleted_post["deleted_picture"])

        return {
            "message": "Post deleted successfully",
            "deleted_id": deleted_post.get("deleted_id"),
            "deleted_picture": deleted_post.get("deleted_picture")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete post: {str(e)}")

    # app/service/v1/feed_service.py

async def get_feed_service(user_id: str, page_no: int):
        try:
            return await fetch_user_feed(user_id, page_no)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch posts: {str(e)}")
