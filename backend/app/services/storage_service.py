import boto3
from botocore.config import Config
from app.config import settings
import uuid

r2_client = boto3.client(
    "s3",
    endpoint_url=settings.R2_ENDPOINT_URL,
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
    region_name="auto"
)

def upload_file(file_content: bytes, filename: str, content_type: str) -> dict:
    file_key = f"materials/{uuid.uuid4()}/{filename}"
    r2_client.put_object(
        Bucket=settings.R2_BUCKET_NAME,
        Key=file_key,
        Body=file_content,
        ContentType=content_type
    )
    url = r2_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.R2_BUCKET_NAME, "Key": file_key},
        ExpiresIn=604800
    )
    return {"key": file_key, "url": url}

def delete_file(file_key: str):
    r2_client.delete_object(
        Bucket=settings.R2_BUCKET_NAME,
        Key=file_key
    )

def get_presigned_url(file_key: str, expires: int = 3600) -> str:
    return r2_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.R2_BUCKET_NAME, "Key": file_key},
        ExpiresIn=expires
    )