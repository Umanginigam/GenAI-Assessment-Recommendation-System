import re

def normalize_url(url: str) -> str:
    """
    Extract a canonical assessment identifier from SHL URLs
    """
    if not isinstance(url, str):
        return ""

    # Remove query params
    url = url.split("?")[0].rstrip("/")

    # Take last path segment
    slug = url.split("/")[-1]

    return slug.lower()
