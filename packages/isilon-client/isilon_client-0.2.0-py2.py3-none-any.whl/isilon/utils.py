import hmac
from hashlib import sha1
from time import time

from yarl import URL

from isilon import exceptions


def generate_presigned_uri(
    user_key: str, object_uri: str, method: str = "GET", duration: int = 60
) -> str:
    """Generate a presigned url to download objects.

    For more information, please see: https://docs.openstack.org/swift/latest/api/temporary_url_middleware.html
    """
    uri = URL(object_uri)
    if len(uri.parts) < 5 or "" in uri.parts:
        raise exceptions.InvalidObjectURI(
            f"Invalid URI format: {object_uri}. Please see: https://docs.openstack.org/swift/latest/api/temporary_url_middleware.html"
        )
    expires = int(time() + duration)
    hmac_body = f"{method}\n{expires}\n{uri.path}".encode("utf8")
    sig = hmac.new(user_key.encode("utf8"), hmac_body, sha1).hexdigest()
    return f"{str(uri.origin())}{uri.path}?temp_url_sig={sig}&temp_url_expires={expires}&filename={uri.name}"
