import os

import musicbrainzngs as mbz


def setup():
    # Set up MusicBrainz API client with appropriate user agent and rate limiting.
    # See https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting for details.
    # The queries made by this crawler do not require authentication.
    useragent_contact = os.getenv(
        "PIPELINES_CRAWLER_CONTACT", default="https://github.com/veeara282/vgmcharts"
    )
    mbz.set_useragent("VGMCharts", "0.1.0", contact=useragent_contact)
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
