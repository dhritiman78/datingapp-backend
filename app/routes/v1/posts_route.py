from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, status, Depends

from app.controllers.v1.posts_controller import upload_posts_controllers, get_user_posts_controllers
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