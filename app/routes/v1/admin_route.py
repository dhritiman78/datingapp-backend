from fastapi import APIRouter, Depends

from app.models.v1.admin_model import AdminUidRequest

router = APIRouter()

@router.delete('/delete/posts', status_code=200)
async def search_route(
        user_uid: AdminUidRequest
):
    return user_uid
