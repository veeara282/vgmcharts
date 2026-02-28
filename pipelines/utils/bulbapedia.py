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

        # The time at which the request began according to the client.
        # These timestamps help us estimate when the page revision was current, in the
        # rare event that it changes during the execution of this method.
        self.mw_request_client_dt = datetime.now(datetime.UTC)
        mw_output_response = requests.get(api_url)

        # Parse server-side datetime in response headers.
        # Note: The server is always required to provide a date header in HTTP responses
        # unless it cannot determine the time. We collect client-side timestamps in case
        # the server does not provide one.
        # Note: the header dict accepts case-insensitive keys.
        response_dt_str = mw_output_response.headers.get("date")
        if response_dt_str:
            self.mw_response_server_dt = dateutil.parser.parse(response_dt_str)

        # Compute client-side response time, the time at which the client finished
        # reading the response (= datetime + timedelta)
        self.mw_response_client_dt = (
            self.mw_request_client_dt + mw_output_response.elapsed
        )

        # Parse JSON and get wikitext
        mw_output_json = mw_output_response.json()
        self.wikitext_expanded = mw_output_json["expandtemplates"]["wikitext"]

        return self.wikitext_expanded
    
    def s3_get_wikitext(self, rev_id: int):
        # Generate object key with version based on revision ID
        object_key = (
            f"sources/bulbapedia/raw/{self.title}/revid={rev_id}.wikitext"
        )
        return object_store.get_text(object_key)

    def s3_put_wikitext(self):
        # Generate object key with version based on revision ID
        object_key = (
            f"sources/bulbapedia/raw/{self.title}/revid={self.latest_rev.id}.wikitext"
        )

        # Upload wikitext to object storage
        object_store.put_text(self.wikitext_expanded, object_key)
        logger.info(
            f"Successfully uploaded wikitext to object storage, key: {object_key}"
        )

    def s3_list_stored_revisions(self):
        key_prefix = f"sources/bulbapedia/raw/{self.title}"

        keys_list = object_store.list_objects_in_dir(key_prefix)

        pattern = re.compile("revid=(\\d+)")
        revisions = []

        for key in keys_list:
            match = pattern.match(key)
            if match:
                # revision ID is the first capture group
                rev_id = int(match.group(1))
                revisions.append(StoredRevision(self.title, rev_id, key))

        return revisions
    
    def get_wikitext_expanded(self):
        # First check if we have any saved revisions
        saved_revisions = self.s3_list_stored_revisions()

        if len(saved_revisions) > 0:
            latest_saved_rev = max(rev.rev_id for rev in saved_revisions)
            # Compare to latest offline page revision
            latest_online_rev = self.mw_get_latest_revision_metadata()

            # If we have the latest revision, fetch it from object storage
            if latest_saved_rev >= latest_online_rev:
                return self.s3_get_wikitext(latest_saved_rev)
