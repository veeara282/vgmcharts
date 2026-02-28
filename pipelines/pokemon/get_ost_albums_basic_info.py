"""
Download the list of English OST releases from Bulbapedia and transform it into a usable CSV file.

Steps:

1. Extract
    - Download page wikitext from API endpoint: https://bulbapedia.bulbagarden.net/w/api.php?action=expandtemplates&text={{:List_of_Pok%C3%A9mon_music_CDs}}&prop=wikitext&format=json
    - Parse JSON and extract value from `$.expandtemplates.wikitext` (JSONPath)
    - Parse the table of English releases (it's actually a nested table, so parse the inner table - the syntax is simple)
    Note: for now, we won't parse the Japanese release table

The result should look like:

|-
| May 9, 2000
| ''[[Pokémon the First Movie (score)|Pokémon the First Movie]]''
| Score for ''[[M01|Mewtwo Strikes Back]]'' and ''[[PK01|Pikachu's Vacation]]''

2. Transform

We turn 3 columns into 4.

release_date: 2000-05-09
release_title: Pokémon the First Movie
bp_page_title: Pokémon the First Movie (score)
short_description: Score for ''[[M01|Mewtwo Strikes Back]]'' and ''[[PK01|Pikachu's Vacation]]''

3. Load

Output to CSV file (for now) or database (once set up).

"""

import logging

import pandas as pd
import wikitextparser as wtp

from pokemon import bulba_utils as bp
from utils import object_store

logger = logging.getLogger(__name__)


def extract_wikitables() -> dict:
    ost_list_page = bp.BulbapediaPage("List of Pokémon music CDs")

    # Get expanded page wikitext
    wikitext = ost_list_page.mw_get_wikitext_expanded()

    # Save to object store
    # TODO: Implement high-level interface with versioning
    object_key = "sources/bulbapedia/raw/" + ost_list_page.get_title()
    wikitext_obj = object_store.get_object(object_key)

    wikitext_obj.put(Body=wikitext)
    logger.info(f"Successfully uploaded wikitext to object storage, key: {object_key}")

    # Since the tables are nested, we extract the tables at indices 1 and 3.
    # The tables at indices 0 and 2 are tables that contain the main tables.
    parsed = wtp.parse(wikitext)

    en_release_table = parsed.tables[1].data()
    ja_release_table = parsed.tables[3].data()

    return {
        "en": en_release_table,
        "ja": ja_release_table,
    }


def make_dataframe(table: list[list[str]]) -> pd.DataFrame:
    # Table has header row
    return pd.DataFrame(data=table[1:], columns=table[0])


def transform_wikitables_to_df(releases_raw: dict) -> dict:
    en_releases_df = make_dataframe(releases_raw["en"])
    ja_releases_df = make_dataframe(releases_raw["ja"])

    logger.info("English releases:")
    logger.info(en_releases_df.head())
    logger.info("Japanese releases:")
    logger.info(ja_releases_df.head())

    object_root = "sources/bulbapedia/extracted_tables/"
    en_releases_object_key = object_root + "ost_releases_info.en.parquet"
    ja_releases_object_key = object_root + "ost_releases_info.ja.parquet"

    object_store.put_dataframe(en_releases_df, en_releases_object_key)
    object_store.put_dataframe(ja_releases_df, ja_releases_object_key)

    return {
        "en": en_releases_df,
        "ja": ja_releases_df,
    }


def main() -> None:
    releases_raw = extract_wikitables()
    transform_wikitables_to_df(releases_raw)


if __name__ == "__main__":
    main()
