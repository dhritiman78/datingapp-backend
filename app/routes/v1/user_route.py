import json
from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File, Form, HTTPException

from app.controllers.v1.user_controller import ping_controller, register_controller, get_user_controller, \
    update_profile_controller, get_user_selected_details_controller
from app.database.redis import redis_client
from app.models.v1.user_model import registerRequest, UpdateRequest, CustomUserRequest
from app.service.v1.dependencies import verify_token

router = APIRouter()

@router.get('/')
async def ping_route():
    return await ping_controller()


@router.post('/register', status_code=201)
async def register_route(
    register_data: registerRequest,
    background_tasks: BackgroundTasks,
    user: dict[str,str] = Depends(verify_token)
):
    return await register_controller(register_data, background_tasks, user)

@router.put("/profile/update")
async def update_profile(
    user: dict[str, str] = Depends(verify_token),
    file: Optional[UploadFile] = File(None),
    update_json: Optional[str] = Form(None)
):
    try:
        update_data = UpdateRequest(**json.loads(update_json)) if update_json else None
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid update JSON")

    return await update_profile_controller(user["uid"], update_data, file)

@router.get('/profile', status_code=200)
async def get_profile(
        user: dict[str, str] = Depends(verify_token)
):
    return await get_user_controller(user)

@router.post("/custom")
async def get_custom_user_data(requests: CustomUserRequest):
    return await get_user_selected_details_controller(requests.user_id,requests.fields)

@router.get("/redis/clear")
async def clear_user_redis():
    cursor = b'0'
    pattern = "user/*"

    while cursor:
        cursor, keys = await redis_client.scan(cursor=cursor, match=pattern, count=100)
        if keys:
            await redis_client.delete(*keys)

    return {"message": "User Redis keys cleared successfully"}