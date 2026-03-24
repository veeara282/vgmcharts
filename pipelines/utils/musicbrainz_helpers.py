import os
from pathlib import Path
import tomllib

import musicbrainzngs as mbz


def get_package_version():
    # Read the package version from pyproject.toml to include in the MusicBrainz API
    # user agent string (in accordance with the DRY principle).
    path = Path("pyproject.toml")
    with path.open("rb") as f:
        data = tomllib.load(f)
        version = data.get("project", {}).get("version")
    return version


def setup():
    # Set up MusicBrainz API client with appropriate user agent and rate limiting.
    # See https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting for details.
    # The queries made by this crawler do not require authentication.
    package_version = get_package_version()
    useragent_contact = os.getenv(
        "PIPELINES_CRAWLER_CONTACT", default="https://github.com/veeara282/vgmcharts"
    )
    mbz.set_useragent("VGMCharts", package_version, contact=useragent_contact)

    # Set default rate limit (1 request per second)
    mbz.set_rate_limit(limit_or_interval=1.0, new_requests=1)
