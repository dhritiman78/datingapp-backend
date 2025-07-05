import json

from app.database.redis import redis_client
from app.repository.reference_data_repository import get_schools, get_branches, get_programmes


async def get_school_service():
    cached_key = "school_reference"
    cached = await redis_client.get(cached_key)
    if cached:
        return json.loads(cached)
    schools = await get_schools()
    schools = [dict(row) for row in schools]
    await redis_client.set(cached_key, json.dumps(schools), ex=604800)
    return schools

async def get_branch_service():
    cached_key = "branch_reference"
    cached = await redis_client.get(cached_key)
    if cached:
        return json.loads(cached)
    branches = await get_branches()
    branches = [dict(row) for row in branches]
    await redis_client.set(cached_key, json.dumps(branches), ex=604800)
    return branches

async def get_programme_service():
    cached_key = "programme_reference"
    cached = await redis_client.get(cached_key)
    if cached:
        return json.loads(cached)
    programmes = await get_programmes()
    programmes = [dict(row) for row in programmes]
    await redis_client.set(cached_key, json.dumps(programmes), ex=604800)
    return programmes