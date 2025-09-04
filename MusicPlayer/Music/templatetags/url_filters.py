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

    parsed_url = urlparse(url)
    # Check if the URL is HTTP and points to Cloudinary
    if parsed_url.scheme == 'http' and 'cloudinary.com' in parsed_url.netloc:
        # Rebuild the URL with the 'https' scheme
        secure_url = urlunparse(('https', parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        return secure_url
    # Return the original URL for any other cases (https, relative paths, etc.)
    return url