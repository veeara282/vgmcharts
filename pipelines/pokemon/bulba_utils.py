"""
Utility functions for extracting Bulbapedia content
"""

import logging
from urllib.parse import urlencode

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


def get_bp_wikitext(page_title: str) -> str:
    api_url = bp_wikitext_url(page_title)

    # MediaWiki output will be wrapped in JSON object
    logger.info(f"Downloading page data from {api_url}...\n")
    mw_output_response = requests.get(api_url)

    # Parse JSON and get wikitext
    mw_output_json = mw_output_response.json()
    return mw_output_json["expandtemplates"]["wikitext"]
