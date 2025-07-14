import asyncpg
from fastapi import HTTPException, status
from app.database.pg_db import get_db_connection

# Reusable DB connection handler
async def with_db_connection(callback):
    pool = await get_db_connection()
    async with pool.acquire() as conn:
        return await callback(conn)

async def get_schools():
    query = """
         SELECT * FROM tuda.school_reference;
    """
    async def run(conn):
        try:
            return await conn.fetch(query)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get schools: {str(e)}"
            )
    return await with_db_connection(run)

async def get_branches():
    query = """
         SELECT * FROM tuda.department_reference;
    """
    async def run(conn):
        try:
            return await conn.fetch(query)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get departments: {str(e)}"
            )
    return await with_db_connection(run)

async def get_programmes():
    query = """
         SELECT * FROM tuda.programme_reference;
    """
    async def run(conn):
        try:
            return await conn.fetch(query)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get programmes: {str(e)}"
            )
    return await with_db_connection(run)