import json

from app.database.redis import redis_client
from app.models.user_model import registerRequest
from app.repository.v1.user_repository import enter_user_details_into_DB, get_user_details


async def insert_user_service(registerData: registerRequest, user: dict[str, str]):
   return await enter_user_details_into_DB(registerData,user)

async def get_user_service(uid: str):
    cached_key = f'user_{uid}'

    # Try from Redis cache
    cached = await redis_client.get(cached_key)
    if cached:
        return json.loads(cached)

    # Fetch from DB
    user_details = await get_user_details(uid)

    # Convert Record to dict and handle datetime fields
    user_dict = dict(user_details)

    # Cache with datetime-safe serialization
    await redis_client.set(cached_key, json.dumps(user_dict, default=str), ex=86400)

    return user_dict

