from app.service.v1.relations_service import get_user_relations_service, set_user_relations_service


async def get_user_relations_controller(ref_user: str, target_user: str):
    return await get_user_relations_service(ref_user, target_user)

async def set_user_relations_controller(ref_user: str, likes, swipes, blocks, unblocks):
    return await set_user_relations_service(ref_user, likes, swipes, blocks, unblocks)