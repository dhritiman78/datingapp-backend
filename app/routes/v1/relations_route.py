from fastapi import APIRouter, Depends

from app.controllers.v1.relations_controller import get_user_relations_controller, set_user_relations_controller
from app.models.v1.relations_model import getUserRelations, SetUserRelations
from app.service.v1.dependencies import verify_token

router = APIRouter()

@router.post('/byUid', status_code=200)
async def get_relations_by_uid(
    target: getUserRelations,
    user: dict[str, str] = Depends(verify_token)
):
    return await get_user_relations_controller(target.target_uid,user["uid"])

@router.post('/set', status_code=200)
async def set_user_relations_route(
    body: SetUserRelations,
    user: dict[str, str] = Depends(verify_token)
):
    return await set_user_relations_controller(
        ref_user=user["uid"],
        likes=body.likes,
        swipes=body.swipes,
        blocks=body.blocks,
        unblocks=body.unblocks
    )
