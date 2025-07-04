import asyncpg
from fastapi import HTTPException, status
from app.database.pg_db import get_db_connection
from app.models.user_model import registerRequest

# Reusable DB connection handler
async def with_db_connection(callback):
    pool = await get_db_connection()
    async with pool.acquire() as conn:
        return await callback(conn)

# Get user details
async def get_schools():
    query = """
        SELECT * FROM tuda.school_reference;
    """
    async def run(conn):
        try:
            return await conn.fetchrow(query)
        except Exception as e:
            raise Exception(f"Failed to get schools: {str(e)}")

    return await with_db_connection(run)