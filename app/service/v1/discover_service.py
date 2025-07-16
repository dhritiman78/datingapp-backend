import json
from typing import Optional, List

from fastapi import HTTPException

from app.models.discover_model import UserCustomFields
from app.repository.v1.discover_repository import fetch_user_custom_fields


async def get_user_custom_data(
    fields: Optional[List[str]] = None,
    user_id: Optional[int] = None,
    user_uid: Optional[str] = None
):
    user_data_dict = await fetch_user_custom_fields(
        fields=fields,
        user_id=user_id,
        user_uid=user_uid
    )

    if user_data_dict:
        if isinstance(user_data_dict, str):
            try:
                user_data_dict = json.loads(user_data_dict)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to decode user data JSON"
                )
        return user_data_dict

    return None