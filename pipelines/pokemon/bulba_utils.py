"""
Utility functions for extracting Bulbapedia content
"""

from urllib.parse import urlencode


API_BASE_URL = "https://bulbapedia.bulbagarden.net/w/api.php"

def bp_wikitext_url(page_title: str) -> str:
    """
    Uses MediaWiki's expandtemplates functionality to return the expanded wikitext for a page on Bulbapedia.

    More info: https://www.mediawiki.org/wiki/API:Expandtemplates
    """
    query_string = urlencode({
        "action": "expandtemplates",
        "text": "{{:" + page_title + "}}",
        "prop": "wikitext",
        "format": "json",
    })

    return API_BASE_URL + "?" + query_string
