import json

from fastapi import HTTPException

from app.repository.v1.relations_repository import fetch_user_relations, set_user_relations


async def get_user_relations_service(ref_user: str, target_user: str):
    try:
        relations = await fetch_user_relations(ref_user, target_user)

        # If already a list or dict, no need to decode
        if isinstance(relations, (dict, list)):
            return relations

        # If it *is* a string, then decode it
        return json.loads(relations)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to decode user data JSON"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

async def set_user_relations_service(ref_user: str, likes, swipes, blocks, unblocks):
    try:
        result = await set_user_relations(ref_user, likes, swipes, blocks, unblocks)

        # asyncpg should return it as dict; but if it's still a JSON string, decode
        if isinstance(result, (dict, list)):
            return result

        import json
        return json.loads(result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set user relations: {str(e)}"
        )
