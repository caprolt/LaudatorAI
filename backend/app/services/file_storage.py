"""File storage service for S3/MinIO."""

import os
import hashlib
from typing import Optional, BinaryIO
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class FileStorageService:
    """File storage service using S3 or MinIO."""
    
    def __init__(self):
        """Initialize file storage service."""
        self.storage_type = settings.file_storage_type
        
        if self.storage_type == "s3":
            self._init_s3()
        else:
            self._init_minio()
    
    def _init_s3(self):
        """Initialize S3 client."""
        self.bucket_name = settings.S3_BUCKET_NAME
        
        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL  # For S3-compatible services like R2
        )
        
        self._ensure_bucket_exists()
    
    def _init_minio(self):
        """Initialize MinIO client."""
        self.bucket_name = settings.MINIO_BUCKET_NAME
        
        # Initialize MinIO client
        self.minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        
        # Initialize S3 client as fallback
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}" if not settings.MINIO_SECURE else f"https://{settings.MINIO_ENDPOINT}",
            region_name='us-east-1'  # Default region for MinIO
        )
        
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create if it doesn't."""
        try:
            if self.storage_type == "s3":
                # Check if bucket exists
                try:
                    self.s3_client.head_bucket(Bucket=self.bucket_name)
                except ClientError as e:
                    error_code = e.response['Error']['Code']
                    if error_code == '404':
                        # Create bucket
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:
                        raise
            else:
                # MinIO bucket check
                if not self.minio_client.bucket_exists(self.bucket_name):
                    self.minio_client.make_bucket(self.bucket_name)
        except Exception as e:
            raise Exception(f"Failed to create bucket: {e}")
    
    def upload_file(self, file_path: str, object_name: Optional[str] = None) -> str:
        """Upload a file to storage."""
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        try:
            if self.storage_type == "s3":
                self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            else:
                self.minio_client.fput_object(
                    self.bucket_name,
                    object_name,
                    file_path
                )
            return f"{self.bucket_name}/{object_name}"
        except Exception as e:
            raise Exception(f"Failed to upload file: {e}")
    
    def upload_fileobj(self, file_obj: BinaryIO, object_name: str, content_type: Optional[str] = None) -> str:
        """Upload a file object to storage."""
        try:
            if self.storage_type == "s3":
                self.s3_client.upload_fileobj(file_obj, self.bucket_name, object_name)
            else:
                self.minio_client.put_object(
                    self.bucket_name,
                    object_name,
                    file_obj,
                    length=-1,  # Let MinIO determine length
                    content_type=content_type
                )
            return f"{self.bucket_name}/{object_name}"
        except Exception as e:
            raise Exception(f"Failed to upload file object: {e}")
    
    def download_file(self, object_name: str, file_path: str) -> bool:
        """Download a file from storage."""
        try:
            if self.storage_type == "s3":
                self.s3_client.download_file(self.bucket_name, object_name, file_path)
            else:
                self.minio_client.fget_object(
                    self.bucket_name,
                    object_name,
                    file_path
                )
            return True
        except Exception as e:
            raise Exception(f"Failed to download file: {e}")
    
    def get_file_url(self, object_name: str, expires: int = 3600) -> str:
        """Get a presigned URL for file access."""
        try:
            if self.storage_type == "s3":
                return self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': object_name},
                    ExpiresIn=expires
                )
            else:
                return self.minio_client.presigned_get_object(
                    self.bucket_name,
                    object_name,
                    expires=expires
                )
        except Exception as e:
            raise Exception(f"Failed to generate presigned URL: {e}")
    
    def delete_file(self, object_name: str) -> bool:
        """Delete a file from storage."""
        try:
            if self.storage_type == "s3":
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            else:
                self.minio_client.remove_object(self.bucket_name, object_name)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete file: {e}")
    
    def file_exists(self, object_name: str) -> bool:
        """Check if a file exists in storage."""
        try:
            if self.storage_type == "s3":
                self.s3_client.head_object(Bucket=self.bucket_name, Key=object_name)
            else:
                self.minio_client.stat_object(self.bucket_name, object_name)
            return True
        except Exception:
            return False
    
    def get_file_info(self, object_name: str) -> dict:
        """Get file information."""
        try:
            if self.storage_type == "s3":
                response = self.s3_client.head_object(Bucket=self.bucket_name, Key=object_name)
                return {
                    "size": response['ContentLength'],
                    "last_modified": response['LastModified'],
                    "etag": response['ETag'].strip('"'),
                    "content_type": response.get('ContentType', 'application/octet-stream')
                }
            else:
                stat = self.minio_client.stat_object(self.bucket_name, object_name)
                return {
                    "size": stat.size,
                    "last_modified": stat.last_modified,
                    "etag": stat.etag,
                    "content_type": stat.content_type
                }
        except Exception as e:
            raise Exception(f"Failed to get file info: {e}")
    
    def list_files(self, prefix: str = "", recursive: bool = True) -> list:
        """List files in storage."""
        try:
            if self.storage_type == "s3":
                response = self.s3_client.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=prefix
                )
                return [obj['Key'] for obj in response.get('Contents', [])]
            else:
                objects = self.minio_client.list_objects(
                    self.bucket_name,
                    prefix=prefix,
                    recursive=recursive
                )
                return [obj.object_name for obj in objects]
        except Exception as e:
            raise Exception(f"Failed to list files: {e}")


# Global file storage service instance - lazy initialization
_file_storage_instance = None

def get_file_storage():
    """Get the global file storage service instance with lazy initialization."""
    global _file_storage_instance
    if _file_storage_instance is None:
        _file_storage_instance = FileStorageService()
    return _file_storage_instance

# For backward compatibility, create a property that calls get_file_storage
class FileStorageProxy:
    """Proxy class to maintain backward compatibility while enabling lazy initialization."""
    
    def __getattr__(self, name):
        return getattr(get_file_storage(), name)

file_storage = FileStorageProxy()


def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def is_valid_file_type(filename: str, allowed_extensions: list) -> bool:
    """Check if file type is allowed."""
    return get_file_extension(filename) in allowed_extensions
