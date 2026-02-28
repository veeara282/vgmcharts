"""
Utility functions for extracting Bulbapedia content
"""

from dataclasses import dataclass
import datetime
import logging
import re
from urllib.parse import urlencode

import dateutil
import requests

from utils import object_store

logger = logging.getLogger(__name__)

# The classic MediaWiki Action API (https://www.mediawiki.org/wiki/API:Action_API)
API_BASE_URL = "https://bulbapedia.bulbagarden.net/w/api.php"

# The newer MediaWiki REST API (https://www.mediawiki.org/wiki/API:REST_API)
REST_API_BASE_URL = "https://bulbapedia.bulbagarden.net/w/rest.php/v1"


@dataclass
class RevisionID:
    """Contains basic metadata about a wiki page revision."""

    id: int
    dt: datetime.datetime


@dataclass
class StoredRevision:
    """Contains metadata about a wiki page revision stored in object storage."""

    page_title: str
    rev_id: int
    object_key: str


def bp_wikitext_api_params(page_title: str) -> dict:
    """
    This dict can optionally be passed to requests.get() as query params
    """
    return {
        "action": "expandtemplates",
        "text": "{{:" + page_title + "}}",
        "prop": "wikitext",
        "format": "json",
    }


def bp_wikitext_url(page_title: str) -> str:
    """
    Uses MediaWiki's expandtemplates functionality to return the expanded wikitext for a page on Bulbapedia.

    More info: https://www.mediawiki.org/wiki/API:Expandtemplates
    """
    query_string = urlencode(bp_wikitext_api_params(page_title))

    return API_BASE_URL + "?" + query_string


class BulbapediaPage:
    def __init__(self, title: str):
        self.title = title.replace(" ", "_")

    def get_title(self):
        return self.title

    def mw_get_latest_revision_metadata(self):
        # Fetch only the metadata (no wikitext)
        api_url = REST_API_BASE_URL + f"/page/{self.title}/bare"

        mw_output_response = requests.get(api_url)
        mw_output_json = mw_output_response.json()

        self.latest_rev = RevisionID(
            mw_output_json["latest"]["id"],
            dateutil.parser.parse(mw_output_json["latest"]["timestamp"]),
        )
        return self.latest_rev

    def mw_get_wikitext_expanded(self):
        """
        Retrieves the expanded wikitext for this page from Bulbapedia using the MediaWiki API.
        """
        api_url = bp_wikitext_url(self.title)

        # MediaWiki output will be wrapped in JSON object
        logger.info(f"Downloading page data from {api_url}...\n")
        mw_output_response = requests.get(api_url)

        # Parse JSON and get wikitext
        mw_output_json = mw_output_response.json()
        self.wikitext_expanded = mw_output_json["expandtemplates"]["wikitext"]

        return self.wikitext_expanded

    def s3_get_wikitext(self, rev_id: int):
        # Generate object key with version based on revision ID
        object_key = f"sources/bulbapedia/raw/{self.title}/revid={rev_id}.wikitext"
        return object_store.get_text(object_key)

    def s3_put_wikitext(self, wikitext: str, rev_id: int):
        # Generate object key with version based on revision ID
        object_key = f"sources/bulbapedia/raw/{self.title}/revid={rev_id}.wikitext"

        # Upload wikitext to object storage
        object_store.put_text(wikitext, object_key)
        logger.info(
            f"Successfully uploaded wikitext to object storage, key: {object_key}"
        )

    def s3_list_stored_revisions(self):
        key_prefix = f"sources/bulbapedia/raw/{self.title}"

        keys_list = object_store.list_objects_in_dir(key_prefix)

        logger.info(f"Found keys: {keys_list}")

        pattern = re.compile("revid=(\\d+)")
        revisions = []

        for key in keys_list:
            match = pattern.search(key)
            if match:
                logger.info(f"Match found: {key}")
                # revision ID is the first capture group
                rev_id = int(match.group(1))
                revisions.append(StoredRevision(self.title, rev_id, key))

        return revisions

    def get_wikitext_expanded(self):
        """
        Retrieves the expanded wikitext for this page from object storage, if we have it
        and it is current, otherwise from the MediaWiki API.
        """
        # First check if we have any saved revisions
        saved_revisions = self.s3_list_stored_revisions()

        if len(saved_revisions) > 0:
            latest_saved_rev = max(rev.rev_id for rev in saved_revisions)
            # Compare to latest offline page revision
            latest_online_rev = self.mw_get_latest_revision_metadata().id

            # If we have the latest revision, fetch it from object storage
            if latest_saved_rev >= latest_online_rev:
                logger.info(
                    f"Revision {latest_saved_rev} on object storage is current. Fetching from object storage..."
                )
                return self.s3_get_wikitext(latest_saved_rev)
            else:
                logger.info(
                    f"Revision {latest_saved_rev} is not current. Will fetch from the MediaWiki API."
                )
        else:
            logger.info("No saved revisions found. Will fetch from the MediaWiki API.")
            # Make sure to set latest_online_rev in BOTH branches
            latest_online_rev = self.mw_get_latest_revision_metadata().id

        # If the latest saved revision is not up to date, or we don't have any saved
        # revisions, fetch the latest revision from online and add it to object storage
        wikitext = self.mw_get_wikitext_expanded()
        self.s3_put_wikitext(wikitext, latest_online_rev)

        return wikitext
