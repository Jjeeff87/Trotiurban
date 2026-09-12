import time

import requests


def is_url_reachable(url, timeout=10):
    """Checks whether a URL is reachable (used to check if the server is up)."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code < 500
    except requests.RequestException:
        return False


def unique_login(prefix="qa"):
    """Generates a unique login from the timestamp, avoiding conflicts between repeated runs."""
    suffix = str(int(time.time() * 1000))[-8:]
    return f"{prefix}{suffix}"
