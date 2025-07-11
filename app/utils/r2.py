import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("R2_ENDPOINT_URL"),
)

BUCKET_NAME = os.getenv("R2_BUCKET_NAME")

async def upload_to_r2(file_obj, filename):
    s3.upload_fileobj(
        file_obj,
        BUCKET_NAME,
        filename,
        ExtraArgs={"ContentType": "image/jpeg"}
    )
    return f"{os.getenv('R2_ENDPOINT_URL')}/{BUCKET_NAME}/{filename}"

async def delete_from_r2(key: str):
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=key)
        return True
    except Exception as e:
        return False
