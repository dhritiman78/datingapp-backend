import json

from fastapi import Header, HTTPException
from firebase_admin import auth
from typing import Optional

# 👇 Ensure Firebase is initialized
import app.utils.firebase
from app.database.redis import redis_client


async def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header")

    token = authorization.split(" ")[1]

    # Try Redis
    cached_user = await redis_client.get(f"token_{token}")
    if cached_user:
        return json.loads(cached_user)

    try:
        decoded_token = auth.verify_id_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

    user_data = {
        "uid": decoded_token.get("uid"),
        "email": decoded_token.get("email"),
        "name": decoded_token.get("name", ""),
    }

    ttl = decoded_token.get("exp", 0) - decoded_token.get("iat", 0)
    if ttl > 0:
        await redis_client.set(f"token_{token}", json.dumps(user_data), ex=ttl)

    return user_data