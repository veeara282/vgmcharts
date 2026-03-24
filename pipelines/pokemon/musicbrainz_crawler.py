import logging

import musicbrainzngs as mbz

import utils.musicbrainz_helpers as mbz_helpers

logger = logging.getLogger(__name__)

# Uncomment this line to show debug logs from musicbrainzngs
# logging.basicConfig(level=logging.DEBUG)


def main():
    mbz_helpers.setup()

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
