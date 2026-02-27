"""
This module provides a high-level interface to an S3-compatible object store such as RustFS.
"""

import io
import logging
import os

import boto3
import pandas as pd

"""Globally used S3 resource object"""
s3 = boto3.resource("s3")

"""The default bucket name provided by an environment variable"""
default_bucket = os.getenv("S3_BUCKET")

logger = logging.getLogger(__name__)


def get_object(key, bucket_name=default_bucket):
    """Return an S3.Object representing the given object.
    If no bucket name is provided, the default bucket will be used."""
    return s3.Object(bucket_name, key)


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
