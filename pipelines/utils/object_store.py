"""
This module provides a high-level interface to an S3-compatible object store such as RustFS.
"""

import io
import logging
import os

import boto3
from botocore.exceptions import ClientError
import pandas as pd

"""Globally used S3 resource object"""
s3 = boto3.resource("s3")

"""The default bucket name provided by an environment variable"""
default_bucket = os.getenv("S3_BUCKET")

logger = logging.getLogger(__name__)


def create_bucket_if_not_exists(bucket_name=default_bucket):
    s3_client = boto3.client("s3")
    # Printing this for logging purposes
    s3_endpoint_url = os.getenv("AWS_ENDPOINT_URL_S3")
    try:
        # Check if bucket exists first
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(
            f"Bucket {bucket_name} already exists on object store {s3_endpoint_url}"
        )
    except ClientError as e:
        # A 404 indicates that the bucket does not exist
        if e.response["Error"]["Code"] == "404":
            s3_client.create_bucket(Bucket=bucket_name)
            logger.info(
                f"Created bucket {bucket_name} on object store {s3_endpoint_url}"
            )
        else:
            raise


def get_object(key, bucket_name=default_bucket):
    """Return an S3.Object representing the given object.
    If no bucket name is provided, the default bucket will be used."""
    return s3.Object(bucket_name, key)


def list_objects_in_dir(key_prefix, bucket_name=default_bucket):
    client = boto3.client("s3")

    # Result is a dict containing a list of objects under "Contents"
    # XXX: By default, only the first 1,000 objects are returned. We do not attempt to
    # fetch any objects past that for now.
    objects = client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=key_prefix,
    )

    # Response may not have a Contents field if there are no results
    # See https://docs.rustfs.com/developer/sdk/python.html#_4-4-list-objects
    if "Contents" in objects:
        return [obj["Key"] for obj in objects["Contents"]]
    else:
        return []


def get_text(
    object_key: str,
    bucket_name: str = default_bucket,
    encoding: str = "utf-8",
):
    s3_object = get_object(object_key, bucket_name)
    response = s3_object.get()
    object_content_bytes = response["Body"].read()
    return object_content_bytes.decode(encoding)


def put_text(
    text: str,
    object_key: str,
    bucket_name: str = default_bucket,
    encoding: str = "utf-8",
):
    s3_object = get_object(object_key, bucket_name)
    text_as_bytes = text.encode(encoding)
    s3_object.put(Body=text_as_bytes)


def put_dataframe(
    df: pd.DataFrame,
    object_key: str,
    bucket_name: str = default_bucket,
    format: str = "parquet",
):
    # Write DataFrame to buffer as Parquet
    buffer = io.BytesIO()
    df.to_parquet(buffer)

    # Get S3.Object and upload
    s3_object = get_object(object_key, bucket_name)
    s3_object.put(Body=buffer.getvalue())
    logger.info(f"Wrote DataFrame to object store, key {object_key}")
