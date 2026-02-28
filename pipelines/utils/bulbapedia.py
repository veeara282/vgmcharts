"""
Utility functions for extracting Bulbapedia content
"""

import datetime
import logging
from urllib.parse import urlencode

import dateutil
import requests

logger = logging.getLogger(__name__)

API_BASE_URL = "https://bulbapedia.bulbagarden.net/w/api.php"


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
        # Note: The HTTP specification requires the server to provide a date header in
        # HTTP responses unless the server cannot determine the time.
        # Note: the header dict accepts case-insensitive keys.
        response_dt_str = mw_output_response.headers.get("date")
        if response_dt_str:
            self.mw_response_server_dt = dateutil.parser.parse(response_dt_str)

        # Compute client-side response time, the time at which the client finished
        # reading the response (= datetime + timedelta)
        self.mw_response_client_dt = self.mw_request_client_dt + mw_output_response.elapsed

        # Parse JSON and get wikitext
        mw_output_json = mw_output_response.json()
        return mw_output_json["expandtemplates"]["wikitext"]
