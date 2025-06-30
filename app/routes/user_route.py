from fastapi import APIRouter, Depends, BackgroundTasks

from app.controllers.user_controller import ping_controller, register_controller
from app.models.user_model import registerRequest
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