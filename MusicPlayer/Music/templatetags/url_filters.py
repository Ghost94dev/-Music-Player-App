# music/templatetags/url_filters.py
from django import template
from urllib.parse import urlparse, urlunparse

register = template.Library()


@register.filter
def make_secure(url):
    """
    Converts an HTTP URL to HTTPS.
    If it's already HTTPS or not a URL, returns it unchanged.
    """
    if not url or not isinstance(url, str):
        return url

    # Check if the URL is HTTP (and is a full URL, not a relative path)
    if url.startswith('http://'):
        # Simply replace http:// with https://
        return url.replace('http://', 'https://', 1)

    # Return the original URL for any other cases (https, relative paths, etc.)
    return url