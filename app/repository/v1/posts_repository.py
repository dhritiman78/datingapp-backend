import asyncpg
from fastapi import HTTPException
from starlette import status

from app.database.pg_db import with_db_connection


async def upload_user_post (user_uid: str, picture: str, caption: str):
    query = """
            SELECT * FROM tuda.upload_user_post(
                $1,
                $2,
                $3
            );
       """

    async def run(conn):
        try:
            result = await conn.execute(query,user_uid,picture,caption)
            return True if result else False

        except asyncpg.exceptions.RaiseError as e:
            if "does not exist" in str(e):
                raise HTTPException(status_code=404, detail=str(e))
            raise HTTPException(status_code=500, detail="Database error: " + str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get schools: {str(e)}"
            )

    return await with_db_connection(run)

async def fetch_user_posts (user_uid: str):
    query = """
                   select * from tuda.get_user_posts($1)
               """

    async def run(conn):
        try:
            return await conn.fetch(
                query,
                user_uid
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get user posts: {str(e)}"
            )

    return await with_db_connection(run)