from fastapi import BackgroundTasks

from app.models.user_model import registerRequest
from app.service.email_service import send_registration_confirmation
from app.service.user_service import insert_user_service


async def ping_controller():
    return {
        "message": "pinging"
    }

async def register_controller(register_data: registerRequest, background_tasks: BackgroundTasks, user: dict[str,str]):
    result = await insert_user_service(register_data,user)
    background_tasks.add_task(send_registration_confirmation, user["email"])

    return result