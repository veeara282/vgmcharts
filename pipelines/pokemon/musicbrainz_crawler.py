import logging
import os
from pathlib import Path
import tomllib

import musicbrainzngs as mbz

logger = logging.getLogger(__name__)

# Uncomment this line to show debug logs from musicbrainzngs
# logging.basicConfig(level=logging.DEBUG)


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


def main():
    setup()

    # TODO: Retrieve data on Pokémon-related releases, recordings, artists, and works
    # using the MusicBrainz API.
    # Start with seed data (known artists, soundtrack albums, etc.) and crawl adjacent
    # entities in the MusicBrainz graph, prioritizing relevant nodes using best-first search.
    # Store retrieved data in a structured format (preferably Parquet) for further processing and analysis.
    # MusicBrainz MBIDs are UUIDs and can be stored as `pyarrow.UuidType` or equivalent
    # in Parquet files for efficient joining.

    known_artists = [
        "42c981ec-aa76-43ee-bd60-dd8b2a3d8857",  # "Pokémon" artist profile
        "cbcafc6f-aa61-400b-9902-00fae1af4a91",  # GlitchxCity
        "b8e8e0aa-0945-47c0-9c27-1263975e63ae",  # Cindery
    ]


if __name__ == "__main__":
    main()
