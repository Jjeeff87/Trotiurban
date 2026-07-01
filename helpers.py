import time

import requests


def is_url_reachable(url, timeout=10):
    """Verifica se uma URL está acessível (usada para checar se o servidor está no ar)."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code < 500
    except requests.RequestException:
        return False


def unique_login(prefix="qa"):
    """Gera um login único baseado no timestamp, evitando conflito de duplicidade entre execuções."""
    suffix = str(int(time.time() * 1000))[-8:]
    return f"{prefix}{suffix}"
