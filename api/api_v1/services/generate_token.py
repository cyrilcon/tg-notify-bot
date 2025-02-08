import hashlib
import hmac
import time

from config import config


def generate_token() -> str:
    """
    Generate a token for the API request.

    :return: A token for the API request.
    """
    current_time = str(int(time.time()))
    return hmac.new(
        config.api.access_token.encode(),
        current_time.encode(),
        hashlib.sha256,
    ).hexdigest()
