"""
Utility functions for extracting Bulbapedia content
"""

import json
import logging
import os
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import requests

logger = logging.getLogger(__name__)

# The classic MediaWiki Action API (https://www.mediawiki.org/wiki/API:Action_API)
API_BASE_URL = "https://bulbapedia.bulbagarden.net/w/api.php"

# The newer MediaWiki REST API (https://www.mediawiki.org/wiki/API:REST_API)
REST_API_BASE_URL = "https://bulbapedia.bulbagarden.net/w/rest.php/v1"


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


def get_bp_data_path() -> Path:
    """
    The expected path for downloaded Bulbapedia data
    
    :return: a Path object representing the data location
    :rtype: Path
    """
    return Path(os.getcwd(), "data", "bulbapedia")


def get_bp_page_current_revision_metadata(page_title: str) -> dict:
    """
    Returns metadata about the current revision of a given wiki page.
    This is used to determine when to refresh datasets that depend on the page.

    :param page_title: The wiki page title on Bulbapedia
    :type page_title: str
    :return: Revision metadata as returned by the MediaWiki API
    :rtype: dict
    """
    api_url = REST_API_BASE_URL + f"/page/{page_title}/history"

    logger.info(
        f'Downloading revision history for page "{page_title}" from {api_url}...'
    )
    mw_output_response = requests.get(api_url)

    mw_output_json = mw_output_response.json()
    return mw_output_json["revisions"][0]


def did_page_change(page_title: str) -> bool:
    file_path = get_bp_data_path() / "revinfo.json"
    revinfo = json.load(file_path)

    if page_title in revinfo:
        # Get cached revision record for the page if it exists
        page_rev_record = revinfo[page_title]

        # Get current revision info from online
        current_revision_info = get_bp_page_current_revision_metadata(page_title)

        # If the online revision is newer than the current cached revision ID, or the record does not exist, return True
        return current_revision_info["id"] > page_rev_record.get("id", -1)
    else:
        # Return true if we have not cached revision data for this page before
        return True
