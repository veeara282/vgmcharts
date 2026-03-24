import os
from pathlib import Path
import tomllib

import musicbrainzngs as mbz
import pandas as pd


type ResultSet = dict[str, list[dict]]


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


def to_dataframes(result_set: ResultSet) -> dict[str, pd.DataFrame]:
    # Extracts all list-based result sets into separate DataFrames, and normalizes
    # nested objects into separate DataFrames with foreign key relationships.
    # Currently, this function only handles the "release-list" result set and its nested
    # "release-group" objects.
    normalized_dfs: dict[str, pd.DataFrame] = {}

    if "release-list" in result_set:
        release_list = result_set["release-list"]
        releases_df = pd.json_normalize(release_list, max_level=0)

        # Rename primary key now
        releases_df = releases_df.rename(columns={"id": "release_id"})

        # Check if release groups were returned in this result set
        if "release-group" in releases_df.columns:
            has_release_group = (
                releases_df["release-group"].apply(lambda x: isinstance(x, dict))
            )

            # Extract release groups into a separate DataFrame
            release_groups_df = pd.json_normalize(
                releases_df.loc[has_release_group, "release-group"]
            ).drop_duplicates(subset=["id"])

            release_groups_df = (
                release_groups_df
                .rename(columns={"id": "release_group_id"})
                .rename(columns=lambda x: x.replace("-", "_"))
            )
            normalized_dfs["release_groups"] = release_groups_df

            # Replace nested object with FK
            releases_df["release_group_id"] = releases_df["release-group"].apply(
                lambda x: x.get("id") if isinstance(x, dict) else pd.NA
            )

            releases_df = releases_df.drop(columns=["release-group"])

        releases_df = releases_df.rename(columns=lambda x: x.replace("-", "_"))
        normalized_dfs["releases"] = releases_df

    return normalized_dfs
