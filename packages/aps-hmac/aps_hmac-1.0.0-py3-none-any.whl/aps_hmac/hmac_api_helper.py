import base64
import hashlib
import hmac
import json
import time
import urllib.parse
import random
from hashlib import md5


class HmacApiHelper:

    def __init__(self, app_id, api_key):
        """
        Generates the value to use for the Authorization header when using the PaySuite Confirmation of Payee API.
        :param app_id: The unique ID for the client's app.
        :param api_key: The client's API key.
        """
        self._app_id = app_id
        self._api_key = api_key

    @staticmethod
    def _s4():
        return format(int((1 + random.random()) * 0x10000), "x")[1:]

    @staticmethod
    def _get_nonce():
        return "".join(HmacApiHelper._s4() for _ in range(8))

    @staticmethod
    def _get_timestamp():
        return str(round(time.time()))

    def get_auth_header(self, body, url, http_method="POST"):
        """
        Returns the Authorization header to use, as a string.
        :param body: The API payload, as a dictionary.
        :param url: The url the request will be sent to.
        :param http_method: The HTTP method to use. By default, this is 'POST'.
        :return:
        """
        request_content_base64_string = ""
        body = json.dumps(body).encode("utf-8")
        url = urllib.parse.quote(url.lower(), safe="")
        request_http_method = http_method
        request_timestamp = HmacApiHelper._get_timestamp()
        nonce = HmacApiHelper._get_nonce()

        if http_method == "GET" or body is None:
            body = ""
        else:
            request_content_hash = md5(body)
            request_content_base64_string = base64.b64encode(request_content_hash.digest()).decode()

        signature_raw_data = (self._app_id + request_http_method + url + request_timestamp + nonce +
                              request_content_base64_string)
        api_key_bytes = base64.b64decode(self._api_key)
        signed_hmac_sha256 = hmac.HMAC(api_key_bytes, signature_raw_data.encode(), hashlib.sha256)
        request_signature_base64_string = base64.b64encode(signed_hmac_sha256.digest()).decode()
        return "Hmac " + self._app_id + ":" + request_signature_base64_string + ":" + nonce + ":" + request_timestamp
