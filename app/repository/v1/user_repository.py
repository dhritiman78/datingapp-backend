from typing import Optional, List

import asyncpg
from fastapi import HTTPException, status
from app.database.pg_db import get_db_connection
from app.models.v1.user_model import registerRequest, UpdateRequest


# Reusable DB connection handler
async def with_db_connection(callback):
    pool = await get_db_connection()
    async with pool.acquire() as conn:
        return await callback(conn)

# Main DB insert function
async def enter_user_details_into_DB(registerData: registerRequest, user: dict[str, str]):
    insert_query = """
        SELECT tuda.insert_new_user(
            $1, $2, $3, $4, $5,
            $6, $7, $8, $9, $10, $11, $12, $13, $14
        );
    """

    async def run(conn):
        try:
            result = await conn.fetchrow(
                insert_query,
                user["uid"],                     # $1
                user["name"],                    # $2
                user["email"],                   # $3
                registerData.gender,             # $4
                registerData.dateOfBirth,      # $5
                registerData.bio,                # $6
                registerData.avataar,            # $7
                registerData.preferred_gender,   # $8
                registerData.school_id,          # $9
                registerData.programme_id,       #10
                registerData.department_id,      #11
                registerData.personality,       #12
                registerData.looking_for,       #13
                registerData.interests or []     #14
            )

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to insert user, no result returned."
                )

            return {
                "message": "User registered successfully.",
                "data": dict(result)
            }

        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this UID or email already exists."
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    return await with_db_connection(run)


async def update_profile_repository(user_id: str, update_data: Optional[UpdateRequest], filename: Optional[str]):
    query = """
            SELECT tuda.update_user_profile(
                p_uid := $1,
                p_name := $2,
                p_gender := $3,
                p_dateOfBirth := $4,
                p_bio := $5,
                p_avataar := $6,
                p_preferred_gender := $7,
                p_school_id := $8,
                p_programme_id := $9,
                p_department_id := $10,
                p_personality := $11,
                p_looking_for := $12,
                p_interests := $13
            );
        """
    async def run(conn):
        try:
            result = await conn.execute(query,
                                        user_id,
                                        update_data.name if update_data else None,
                                        update_data.gender if update_data else None,
                                        update_data.dateOfBirth if update_data else None,
                                        update_data.bio if update_data else None,
                                        filename,
                                        update_data.preferred_gender if update_data else None,
                                        update_data.school_id if update_data else None,
                                        update_data.programme_id if update_data else None,
                                        update_data.department_id if update_data else None,
                                        update_data.personality if update_data else None,
                                        update_data.looking_for if update_data else None,
                                        update_data.interests if update_data else None
                                        )
            return True if result else False

        except asyncpg.exceptions.RaiseError as e:
            if "does not exist" in str(e):
                raise HTTPException(status_code=404, detail=str(e))
            raise HTTPException(status_code=500, detail="Database error: " + str(e))

    return await with_db_connection(run)

# Get user details
async def get_user_details(user_id: str):
    query = """
         SELECT * FROM tuda.get_user_profile($1);
    """
    async def run(conn):
        try:
            results = await conn.fetchrow(query, user_id)

            if not results:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No user with that uid is available."
                )

            return results

        except HTTPException:
            # Let HTTPException bubble up (don't wrap it in another exception)
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get the user: {str(e)}"
            )

    return await with_db_connection(run)


async def get_user_selected_fields(user_id: str, fields: List[str]) -> Optional[dict]:
    # Prevent SQL injection by whitelisting columns
    allowed_fields = {
        "uid", "name", "email", "gender", "dateofbirth", "bio", "avataar",
        "preferred_gender", "school_id", "programme_id", "department_id",
        "is_verified", "is_admin", "created_at", "last_updated", "last_logged_in",
        "personality", "looking_for"
    }

    selected = [f for f in fields if f in allowed_fields]
    if not selected:
        raise ValueError("No valid fields requested.")

    query = f"""
        SELECT {', '.join(selected)}
        FROM tuda.users
        WHERE uid = $1
    """

    async def run(conn):
        return await conn.fetchrow(query, user_id)

    row = await with_db_connection(run)
    return dict(row) if row else None

# Delete user from DB
async def delete_user_repository(uuid: str):
    query = """
        DELETE FROM tuda.users
        WHERE uid = $1
        RETURNING uid;
    """

    async def run(conn):
        try:
            result = await conn.fetchrow(query, uuid)
            return True if result else False

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error while deleting user: {str(e)}"
            )

    return await with_db_connection(run)

