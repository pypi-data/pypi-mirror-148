"""Base package."""

import requests


def get(url: str, kwargs: dict = {}) -> dict:
    """Test fn.

    Args:
        url (str): url to get
        kwargs (dict, optional): extra kwargs. Defaults to {}.

    Returns:
        dict: http json or exception
    """
    try:
        r = requests.get(url, **kwargs)
        r.raise_for_status()
        return r.json()
    except Exception as ex:
        return {'ex': str(ex)}
