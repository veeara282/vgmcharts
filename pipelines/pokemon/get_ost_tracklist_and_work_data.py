from datetime import datetime
import logging
from os import mkdir

import musicbrainzngs as mbz
import pandas as pd

from utils.local_io import DATA_DIR
import utils.musicbrainz_helpers as mbz_helpers

logger = logging.getLogger(__name__)

# Uncomment this line to show debug logs from musicbrainzngs
logging.basicConfig(level=logging.DEBUG)


def get_ost_releases():
    # Get MusicBrainz release entries linked to either The Pokémon Company as label
    # or Game Freak as artist.
    # We filter for official release entries on MusicBrainz as they have more complete
    # metadata (including ISRCs, underlying musical works, and composer credits), and
    # exclude "bootleg" releases such as gamerips.
    # We also query release groups as they may be helpful for matching English and
    # Japanese releases of the same game soundtrack.

    # The Pokémon Company (Japan)
    tpc_label = "e19f9e2b-4dd5-4f52-9e3c-46b678986698"

    tpc_releases = mbz.browse_releases(
        label=tpc_label,
        includes=["release-groups"],
        release_status="official",
        limit=100,  # the maximum size of a single API results page
    )  #: ReleaseList

    # Game Freak
    game_freak_artist = "88c8f9c2-763b-45c9-863f-da3c7c6c8fd1"

    game_freak_releases = mbz.browse_releases(
        artist=game_freak_artist,
        includes=["release-groups"],
        release_status="official",
        limit=100,
    )  #: ReleaseList

    tpc_data_normalized = mbz_helpers.to_dataframes(tpc_releases)
    game_freak_data_normalized = mbz_helpers.to_dataframes(game_freak_releases)

    combined_data = mbz_helpers.combine_datasets(
        tpc_data_normalized, game_freak_data_normalized
    )
    return combined_data


def filter_main_series(df: pd.DataFrame) -> pd.DataFrame:
    # Filter for main series Pokémon OSTs based on title and disambiguation fields.
    # This function can take either the releases or the release_groups DataFrame as
    # input, since they both have the same "title" field.
    return df[
        # Filter titles matching "Pokémon" and...
        df["title"].str.contains("Pok[eé]mon|ポケモン|ポケットモンスター")
        & (
            # either "Super Music [Collection/Complete]" (or similar) in the title,
            # or "Nintendo Music" in the disambiguation
            df["title"].str.contains("Super Music|スーパー|ミュージック")
            | (
                ~df["disambiguation"].isna()
                & df["disambiguation"].str.contains("Nintendo Music")
            )
        )
    ].reset_index(drop=True)


def main():
    mbz_helpers.setup()

    # Construct the directory path for this pipeline run using the current timestamp
    # in ISO 8601 format with milliseconds precision, e.g. "2026-03-05T12:34:56.789".
    dt = datetime.now().isoformat(timespec="milliseconds")
    data_dir_for_run = DATA_DIR / "pokemon_ost_data" / dt

    # First download all official release entries linked to The Pokémon Company or
    # Game Freak as label or artist, then filter for Pokémon main series relevance.
    combined_releases = get_ost_releases()
    mbz_helpers.write_dataset(combined_releases, data_dir_for_run / "all_releases")

    # Prepare directory for filtered datasets
    main_series_releases_dir = data_dir_for_run / "main_series_releases"
    main_series_releases_dir.mkdir(parents=True, exist_ok=True)

    # Note: This function returns a single DataFrame, so the standard to_parquet() method
    # is used here instead of the mbz_helpers.write_dataset() function.
    main_series_releases = filter_main_series(combined_releases["releases"])
    main_series_releases.to_parquet(
        main_series_releases_dir / "all.parquet", index=False
    )

    # Separate out English and Japanese releases based on country code ("XW", "JP").
    # The worldwide release entries on MusicBrainz (country code "XW") include English
    # track titles, which are useful for matching OST musical works to fan-made covers.
    english_releases = main_series_releases[main_series_releases["country"] == "XW"]
    japanese_releases = main_series_releases[main_series_releases["country"] == "JP"]

    english_releases.to_parquet(main_series_releases_dir / "en.parquet", index=False)
    japanese_releases.to_parquet(main_series_releases_dir / "ja.parquet", index=False)


if __name__ == "__main__":
    main()
