import asyncpg
from fastapi import HTTPException, status

from app.database.pg_db import with_db_connection


async def fetch_user_relations(ref_user: str, target_user: str):
    query = """
             select * from tuda.get_user_relations(
                $1,
                $2
            )
        """

    async def run(conn):
        try:
            return await conn.fetchval(query,ref_user,target_user)
        except asyncpg.exceptions.PostgresError as e:
            # Catch specific PostgreSQL errors
            if "User not found" in str(e):
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

async def set_user_relations(ref_user: str, likes, swipes, blocks, unblocks):
    query = """
        SELECT tuda.set_user_relations($1, $2, $3, $4, $5)
    """

    async def run(conn):
        return await conn.fetchval(query, ref_user, likes, swipes, blocks, unblocks)

    return await with_db_connection(run)
