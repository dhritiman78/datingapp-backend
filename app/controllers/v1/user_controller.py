from typing import Optional, List

from fastapi import BackgroundTasks, UploadFile
from datetime import datetime
from app.models.v1.user_model import registerRequest, UpdateRequest
from app.service.v1.email_service import send_registration_confirmation
from app.service.v1.user_service import insert_user_service, get_user_service, update_profile_service, \
    get_user_selected_fields_service
from app.utils.compress_image import compress_image


async def ping_controller():
    return {
        "message": "pinging"
    }

async def register_controller(register_data: registerRequest, background_tasks: BackgroundTasks, user: dict[str,str]):
    result = await insert_user_service(register_data,user)
    background_tasks.add_task(send_registration_confirmation, user["email"])

    return result

async def update_profile_controller(user_id: str, update_data: Optional[UpdateRequest], file: Optional[UploadFile]):
    compressed_buffer = None
    filename = None
    if file:
        contents = await file.read()
        compressed_buffer = await compress_image(contents)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"avatars/{user_id}_{timestamp}.jpg"

    return await update_profile_service(user_id, update_data, filename, compressed_buffer)

async def get_user_controller(user: dict[str, str]):
    return await get_user_service(user["uid"])

async def get_user_selected_details_controller(user_id: str, fields: List[str]):
    return await get_user_selected_fields_service(user_id, fields)