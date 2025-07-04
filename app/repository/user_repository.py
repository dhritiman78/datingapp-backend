import asyncpg
from fastapi import HTTPException, status
from app.database.pg_db import get_db_connection
from app.models.user_model import registerRequest

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
            $6, $7, $8, $9, $10, $11, $12
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
                registerData.interests or []     #12
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


from fastapi import HTTPException, status

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
