"""
This module provides a high-level interface to an S3-compatible object store such as RustFS.
"""

import os

import boto3

"""Globally used S3 resource object"""
s3 = boto3.resource("s3")

"""The default bucket name provided by an environment variable"""
default_bucket = os.getenv("S3_BUCKET")

"""Return an S3.Object representing the given object.
If no bucket name is provided, the default bucket will be used."""


def get_object(key, bucket=default_bucket):
    return s3.Object(bucket, key)
