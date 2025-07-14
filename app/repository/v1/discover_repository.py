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