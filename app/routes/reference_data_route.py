from fastapi import APIRouter, Depends

from app.repository.reference_data_repository import get_schools
from app.service.dependencies import verify_token

router = APIRouter()

@router.post('/schools', dependencies=[Depends(verify_token)], status_code=200)
async def register_route():
    return await get_schools()