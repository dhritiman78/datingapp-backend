import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

db_pool = None

async def connect_to_db():
    global db_pool
    if not db_pool:
        db_pool = await asyncpg.create_pool(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            min_size=1,
            max_size=10
        )

async def get_db_connection():
    if not db_pool:
        await connect_to_db()
    return db_pool