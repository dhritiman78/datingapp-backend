from typing import Optional, List

from app.service.v1.discover_service import get_user_custom_data, get_random_users_for_match_service
from app.service.v1.user_service import get_user_service


async def get_user_data_by_id_or_uid_controller(
    user_id: Optional[int] = None,
    user_uid: Optional[str] = None,
    fields: Optional[List[str]] = None,
):
    if user_uid and not  fields:
        return await get_user_service(user_uid)

    return await get_user_custom_data(fields,user_id,user_uid)

async def get_random_users_for_match_controller(user_uid: str):
    return await get_random_users_for_match_service(user_uid)