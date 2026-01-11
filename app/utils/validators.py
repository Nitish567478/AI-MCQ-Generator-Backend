from urllib.parse import urlparse

def validate_wikipedia_url(url: str):
    parsed = urlparse(url)
    return "wikipedia.org" in parsed.netloc
