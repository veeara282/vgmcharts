import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def create_bucket_if_not_exists(s3_client, bucket_name):
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


def main() -> None:
    try:
        # Initialize the Boto3 client - should automagically read the `AWS_*` environment
        # variables in `docker-compose.yml` and authenticate
        s3_client = boto3.client("s3")

        # Create the bucket if it doesn't exist
        bucket_name = os.getenv("S3_BUCKET")
        create_bucket_if_not_exists(s3_client, bucket_name)

        # Put a test object
        s3_client.put_object(
            Body=b"Hello, and welcome to the VGMCharts data lake. We hope to see you again!",
            Bucket=bucket_name,
            Key="hello",  # Caution: keys should not have leading slashes
        )
        logger.info(f"Added test object to bucket {bucket_name}")
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
