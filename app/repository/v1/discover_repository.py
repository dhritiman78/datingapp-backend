from typing import Optional, List, Dict, Any

import asyncpg
from fastapi import HTTPException, status
from app.database.pg_db import get_db_connection

# Reusable DB connection handler
async def with_db_connection(callback):
    pool = await get_db_connection()
    async with pool.acquire() as conn:
        return await callback(conn)

async def fetch_users_by_search(user_id: str, search_parameter: str):
    query = """
             SELECT * FROM tuda.search_users_by_name_prefix($1,$2);
        """

    async def run(conn):
        try:
            return await conn.fetch(query,user_id,search_parameter)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get users: {str(e)}"
            )
    return await with_db_connection(run)

async def fetch_user_custom_fields(
        fields: Optional[List[str]] = None,
        user_id: Optional[int] = None,
        user_uid: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
    query = """
                SELECT tuda.get_user_custom_fields($1::TEXT[], $2::INT, $3::TEXT);
           """

    async def run(conn):
        try:
            p_fields_arg = fields if fields is not None else None
            p_id_arg = user_id if user_id is not None else None
            p_uid_arg = user_uid if user_uid is not None else None
            return await conn.fetchval(
                query,
                p_fields_arg,
                p_id_arg,
                p_uid_arg
            )
        except asyncpg.exceptions.PostgresError as e:
            # Catch specific PostgreSQL errors
            if "User not found" in str(e):
                return None  # Indicate user not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User Not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get users: {str(e)}"
            )

    return await with_db_connection(run)