import os
from pathlib import Path

"""Root directory for local data storage. This can be overridden by setting the PIPELINES_DATA_DIR environment variable."""
DATA_DIR = Path(os.getenv("PIPELINES_DATA_DIR", "/data"))
