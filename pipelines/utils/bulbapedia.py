"""
Utility functions for extracting Bulbapedia content
"""

from dataclasses import dataclass
import datetime
import logging
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

    def s3_put_wikitext(self):
        # Generate object key with version based on timestamp
        object_key = f"sources/bulbapedia/raw/{self.title}/dt={self.mw_response_server_dt.isoformat()}.wikitext"

        # Upload wikitext to object storage
        remote_object = object_store.get_object(object_key)
        remote_object.put(Body=self.wikitext_expanded)
        logger.info(
            f"Successfully uploaded wikitext to object storage, key: {object_key}"
        )
