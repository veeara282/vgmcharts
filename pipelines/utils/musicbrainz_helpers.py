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
            has_release_group = releases_df["release-group"].apply(
                lambda x: isinstance(x, dict)
            )

            # Extract release groups into a separate DataFrame
            release_groups_df = (
                pd.json_normalize(releases_df.loc[has_release_group, "release-group"])
                .drop_duplicates(subset=["id"], ignore_index=True)
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


def combine_datasets(*dfs: list[dict[str, pd.DataFrame]]) -> dict[str, pd.DataFrame]:
    # Combines multiple normalized datasets into a single dataset, merging DataFrames
    # with the same name and concatenating rows.
    if len(dfs) == 1:
        return dfs[0]
    if len(dfs) == 0:
        raise ValueError("At least one dataset expected")

    combined_dfs: dict[str, pd.DataFrame] = {}
    grouped_dfs: dict[str, list[pd.DataFrame]] = {}

    # Group DataFrames by name across all datasets
    for dataset in dfs:
        for name, df in dataset.items():
            # Append DataFrame to the list if it exists, otherwise append to empty list
            grouped_dfs.setdefault(name, []).append(df)

    for name, frames in grouped_dfs.items():
        # If there is only one DataFrame for this name, no need to do anything
        if len(frames) == 1:
            combined_dfs[name] = frames[0]
            continue

        # First combine all rows into a new DataFrame
        merged_df = pd.concat(frames, ignore_index=True, sort=False)

        # DataFrame may contain multiple "id" columns (primary and foreign keys), so we
        # deduplicate based on all of them. There should always be at least one "id"
        # column, but we implement a fallback just in case.
        keys = [
            column
            for column in merged_df.columns
            if column == "id" or column.endswith("_id")
        ]

        if keys:
            merged_df = merged_df.drop_duplicates(subset=keys, ignore_index=True)
        else:
            # Fallback behavior (if no "id" columns found): just drop duplicate rows
            merged_df = merged_df.drop_duplicates(ignore_index=True)

        combined_dfs[name] = merged_df

    return combined_dfs
