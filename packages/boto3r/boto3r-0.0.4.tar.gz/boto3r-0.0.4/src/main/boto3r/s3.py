from typing import *
from option import Result, Option, Ok, Err
import boto3


class S3:

    @classmethod
    def create(cls, region: str = None) -> Result['S3', str]:
        try:
            return Ok(S3(region))
        except Exception as e:
            return Err("Exception creating boto3 S3")

    def __init__(self, region: str = None) -> None:
        arg = {}
        if region is not None:
            arg['region_name'] = region
        self.__client = boto3.client('s3', **arg)

    def put_object(self, bucket: str, key: str, content: Any) -> Result[str, str]:
        try:
            self.__client.put_object(Bucket=bucket, Key=key, Body=str.encode(content))
            return Ok(f's3://{bucket}/{key}')
        except Exception as e:
            return Err(f"Exception: {e} uploading to s3://{bucket}/{key}")

    def get_object(self, bucket: str, key: str) -> Result[bytes, str]:
        try:
            r = self.__client.get_object(Bucket=bucket, Key=key)
            return Ok(r['Body'].read())
        except Exception as e:
            return Err(f"Exception: {e} getting to s3://{bucket}/{key}")

    def upload_file(self, bucket: str, key: str, filename: str) -> Result[str, str]:
        try:
            self.__client.upload_file(filename, Bucket=bucket, Key=key)
            return Ok(f's3://{bucket}/{key}')
        except Exception as e:
            return Err(f"Exception: {e} uploading {filename} to s3://{bucket}/{key}")

    def download_file(self, bucket: str, key: str, filename: str) -> Result[str, str]:
        try:
            self.__client.download_file(filename, Bucket=bucket, Key=key)
            return Ok(filename)
        except Exception as e:
            return Err(f"Exception: {e} downloading {filename} from s3://{bucket}/{key}")

    def get_attributes(cls, bucket: str, key: str) -> Result[Dict[str, Any], str]:
        try:
            r = cls.__client.head_object(Bucket=bucket, Key=key)
            return Ok(r)
        except Exception as e:
            return Err(f"Exception: {e} getting attributes of s3://{bucket}/{key}")
