import logging

import musicbrainzngs as mbz
import pandas as pd

import utils.musicbrainz_helpers as mbz_helpers

logger = logging.getLogger(__name__)

# Uncomment this line to show debug logs from musicbrainzngs
# logging.basicConfig(level=logging.DEBUG)


def get_ost_releases():
    tpc_label = "e19f9e2b-4dd5-4f52-9e3c-46b678986698"  # The Pokémon Company (Japan)

    tpc_releases = mbz.browse_releases(
        label=tpc_label,
        includes=[
            "release-groups"
        ],  # use release groups to help identify releases of the same game soundtrack
    )  #: ReleaseList

    game_freak_artist = "88c8f9c2-763b-45c9-863f-da3c7c6c8fd1"  # Game Freak

    game_freak_releases = mbz.browse_releases(
        artist=game_freak_artist, includes=["release-groups"]
    )  #: ReleaseList

    tpc_data_normalized = mbz_helpers.to_dataframes(tpc_releases)
    game_freak_data_normalized = mbz_helpers.to_dataframes(game_freak_releases)

    combined_data = mbz_helpers.combine_datasets(
        tpc_data_normalized, game_freak_data_normalized
    )
    return combined_data


def filter_main_series(df: pd.DataFrame) -> pd.DataFrame:
    # Only keep titles matching "Pokemon" and "Super Music [Collection/Complete]"
    # (or their Japanese equivalents).
    # This function can take either the releases or the release_groups DataFrame as
    # input, since they both have the same "title" field.
    return df[
        df["title"].str.contains("Pok[eé]mon|ポケモン|ポケットモンスター")
        & df["title"].str.contains(
            "Super Music|スーパーミュージック|ミュージック・スーパー"
        )
    ].reset_index(drop=True)


def main():
    mbz_helpers.setup()
    combined_releases = get_ost_releases()
    main_series_releases = filter_main_series(combined_releases["releases"])


if __name__ == "__main__":
    main()
