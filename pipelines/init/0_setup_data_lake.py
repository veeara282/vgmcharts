import logging
import os

from utils import object_store

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        # Create the bucket if it doesn't exist
        bucket_name = os.getenv("S3_BUCKET")
        if bucket_name:
            object_store.create_bucket_if_not_exists()

            # Put a test object
            object_store.put_text(
                "Hello, and welcome to the VGMCharts data lake. We hope to see you again!",
                "hello",
            )
            logger.info(f"Added test object to bucket {bucket_name}")
        else:
            raise ValueError(
                "Environment variable S3_BUCKET is not set. Please see instructions in pipelines/README.md for troubleshooting instructions."
            )
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
