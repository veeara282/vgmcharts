import logging

import musicbrainzngs as mbz

import utils.musicbrainz_helpers as mbz_helpers

logger = logging.getLogger(__name__)

# Uncomment this line to show debug logs from musicbrainzngs
# logging.basicConfig(level=logging.DEBUG)


def get_ost_releases():
    tpc_label = "e19f9e2b-4dd5-4f52-9e3c-46b678986698"  # The Pokémon Company (Japan)

    tpc_releases = mbz.browse_releases(
        label=tpc_label,
        includes=["release-groups"]  # use release groups to help identify releases of the same game soundtrack
    ) #: ReleaseList

    game_freak_artist = "88c8f9c2-763b-45c9-863f-da3c7c6c8fd1"  # Game Freak

    game_freak_releases = mbz.browse_releases(
        artist=game_freak_artist,
        includes=["release-groups"]
    ) #: ReleaseList

    # TODO Merge and deduplicate these release lists



def main():
    mbz_helpers.setup()
    combined_releases = get_ost_releases()


if __name__ == "__main__":
    main()
