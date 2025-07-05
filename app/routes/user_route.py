from fastapi import APIRouter, Depends, BackgroundTasks

from app.controllers.user_controller import ping_controller, register_controller, get_user_controller
from app.models.user_model import registerRequest
from app.repository.user_repository import get_user_details
from app.service.dependencies import verify_token

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

@router.get('/profile', status_code=200)
async def get_profile(
        user: dict[str, str] = Depends(verify_token)
):
    return await get_user_controller(user)
