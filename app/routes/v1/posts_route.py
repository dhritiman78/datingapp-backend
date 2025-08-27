from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, status, Depends

from app.controllers.v1.posts_controller import upload_posts_controllers, get_user_posts_controllers, \
    delete_user_post_controller, get_user_feed_posts
from app.models.v1.posts_model import GetUserPosts
from app.service.v1.dependencies import verify_token

router = APIRouter()

@router.post('/upload', status_code=status.HTTP_201_CREATED)
async def upload_posts_route(
    user: dict[str, str] = Depends(verify_token),
    picture: UploadFile = File(...),
    caption: str = Form(...)
):
    return await upload_posts_controllers(user["uid"],picture,caption)

@router.get('/all', status_code=status.HTTP_200_OK)
async def get_user_posts(
    target: Optional[str] = None,
    user: dict[str, str] = Depends(verify_token),
):
    return await get_user_posts_controllers(user["uid"], target)

@router.delete('/delete/{post_id}', status_code=status.HTTP_200_OK)
async def delete_user_post_route(
    post_id: int,
    user: dict[str, str] = Depends(verify_token),
):
    return await delete_user_post_controller(user["uid"], post_id)

@router.get('/feed/{page_no}', status_code=status.HTTP_200_OK)
async def get_feed_route(
        page_no: int,
        user: dict[str, str] = Depends(verify_token),
):
        return await get_user_feed_posts(user["uid"],page_no)