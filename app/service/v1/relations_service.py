import asyncio
import json
import traceback

from fastapi import HTTPException
from firebase_admin import db

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

# ✅ Background task to push matches to Firebase
async def save_matches_to_firebase(ref_user: str, matched_users: list):
    try:
        ref = db.reference("usermatches")
        for uid in matched_users:
            try:
                ref.push({
                    "user1": ref_user,
                    "user2": uid
                })
            except Exception as inner_error:
                print(f"❌ Error pushing match for {ref_user} ↔ {uid}: {inner_error}")
                traceback.print_exc()

    except Exception as outer_error:
        print("❌ Firebase push task failed:", outer_error)
        traceback.print_exc()


async def set_user_relations_service(ref_user: str, likes, swipes, blocks, unblocks):
    try:
        result = await set_user_relations(ref_user, likes, swipes, blocks, unblocks)

        if not isinstance(result, (dict, list)):
            result = json.loads(result)

        matched = result.get("matched", [])

        # ✅ Run Firebase match saving in background
        if matched:
            asyncio.create_task(save_matches_to_firebase(ref_user, matched))

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set user relations: {str(e)}"
        )