from fastapi import APIRouter, Depends

from app.controllers.v1.discover_controller import get_user_data_by_id_or_uid_controller, \
    get_random_users_for_match_controller
from app.models.v1.discover_model import searchData, ByIdRequest, ByUidRequest
from app.repository.v1.discover_repository import fetch_users_by_search
from app.service.v1.dependencies import verify_token

router = APIRouter()

@router.post('/search', status_code=200)
async def search_route(
    searched_key: searchData,
    user: dict[str, str] = Depends(verify_token)
):
    return await fetch_users_by_search(user["uid"],searched_key.search_parameter)

@router.post('/byId', status_code=200)
async def get_user_by_id(req: ByIdRequest):
    return await get_user_data_by_id_or_uid_controller(req.user_id, None,req.fields)

@router.post('/byUid', status_code=200)
async def get_user_by_uid(req: ByUidRequest):
    return await get_user_data_by_id_or_uid_controller(None, req.user_uid,req.fields)

@router.post('/random', status_code=200)
async def get_random_users_for_match_route(
    user: dict[str, str] = Depends(verify_token)
):
    return await get_random_users_for_match_controller(user["uid"])