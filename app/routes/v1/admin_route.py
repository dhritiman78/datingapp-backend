from fastapi import APIRouter, Depends

from app.controllers.v1.admin_controller import delete_user_controller
from app.models.v1.admin_model import AdminDeleteRequest

router = APIRouter()

@router.delete('/delete/user', status_code=200)
async def search_route(
        admin_delete: AdminDeleteRequest
):
    return await delete_user_controller(admin_delete.uid,admin_delete.key)
