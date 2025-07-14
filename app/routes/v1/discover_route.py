from fastapi import APIRouter, Depends

from app.models.discover_model import searchData
from app.repository.v1.discover_repository import fetch_users_by_search
from app.service.v1.dependencies import verify_token

router = APIRouter()

@router.post('/search', status_code=200)
async def search_route(
    searched_key: searchData,
    user: dict[str, str] = Depends(verify_token)
):
    return await fetch_users_by_search(user["uid"],searched_key.search_parameter)