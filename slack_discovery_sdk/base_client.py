"""A Python module for interacting with Slack's Discovery API."""

import json
import logging
import urllib
from base64 import b64encode
from http.client import HTTPResponse
from ssl import SSLContext
from typing import Dict
from typing import Optional
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen, OpenerDirector, ProxyHandler, HTTPSHandler

from slack_discovery_sdk.errors import DiscoveryRequestError, DiscoveryApiError
from .internal_utils import (
    convert_bool_to_0_or_1,
    get_user_agent,
    _get_url,
    _build_unexpected_body_error_message,
)
from .response import DiscoveryResponse
from .proxy_support import load_http_proxy_from_env


class BaseDiscoveryClient:
    BASE_URL = "https://slack.com/api/"

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: str = BASE_URL,
        timeout: int = 30,
        ssl: Optional[SSLContext] = None,
        proxy: Optional[str] = None,
        headers: Optional[dict] = None,
        user_agent_prefix: Optional[str] = None,
        user_agent_suffix: Optional[str] = None,
        # for Org-Wide App installation
        team_id: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.token = None if token is None else token.strip()
        self.base_url = base_url
        self.timeout = timeout
        self.ssl = ssl
        self.proxy = proxy
        self.headers = headers or {}
        self.headers["User-Agent"] = get_user_agent(
            user_agent_prefix, user_agent_suffix
        )
        self.default_params = {}
        if team_id is not None:
            self.default_params["team_id"] = team_id
        self._logger = logger if logger is not None else logging.getLogger(__name__)

        if self.proxy is None or len(self.proxy.strip()) == 0:
            env_variable = load_http_proxy_from_env(self._logger)
            if env_variable is not None:
                self.proxy = env_variable

    def api_call(  # skipcq: PYL-R1710
        self,
        api_method: str,
        *,
        http_method: str = "POST",
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        auth: Optional[dict] = None,
    ) -> DiscoveryResponse:
        """Create a request and execute the API call to Slack.
        Args:
            api_method (str): The target Slack API method.
                e.g. 'discovery.enterprise.info'
            http_method (str): The HTTP method
                e.g. POST, GET
            params (dict): The URL parameters to append to the URL.
                e.g. {'key1': 'value1', 'key2': 'value2'}
            headers (dict): Additional request headers
            auth (dict): A dictionary that consists of client_id and client_secret
        Returns:
            (DiscoveryResponse)
                The server's response to an HTTP request. Data
                from the response can be accessed like a dict.
                If the response included 'next_cursor' it can
                be iterated on to execute subsequent requests.
        Raises:
            SlackApiError: The following Slack API call failed:
                'discovery.enterprise.info'.
        """

        api_url = _get_url(self.base_url, api_method)
        headers = headers or {}
        headers.update(self.headers)

        # Basic Auth for oauth.v2.access
        if auth is not None:
            if isinstance(auth, str):
                headers["Authorization"] = auth
            elif isinstance(auth, dict):
                client_id, client_secret = auth["client_id"], auth["client_secret"]
                value = b64encode(
                    f"{client_id}:{client_secret}".encode("utf-8")
                ).decode("ascii")
                headers["Authorization"] = f"Basic {value}"
            else:
                self._logger.warning(
                    f"As the auth: {auth}: {type(auth)} is unsupported, skipped"
                )

        token = self.token
        params = params or {}
        if "token" in params:
            param_token = params.pop("token")
            if param_token is not None:
                token = param_token
        cleansed_params = { k:v for k, v in params.items() if v is not None }
        return self._urllib_api_call(
            token=token,
            http_method=http_method,
            url=api_url,
            params=cleansed_params or {},
            additional_headers=headers or {},
        )

    def fetch_next_page(
        self,
        http_method: str,
        api_url: str,
        headers: Dict[str, str],
        params: Dict[str, str],
    ) -> Dict[str, any]:
        """This method is supposed to be used only for DiscoveryResponse pagination
        You can paginate using Python's for iterator as below:
          for response in client.conversations_list(limit=100):
              # do something with each response here
        """
        response = self._perform_urllib_http_request(
            http_method=http_method,
            url=api_url,
            headers=headers or {},
            params=params or {},
        )
        return {
            "status_code": int(response["status"]),
            "headers": dict(response["headers"]),
            "body": json.loads(response["body"]),
        }

    def _urllib_api_call(
        self,
        *,
        token: Optional[str] = None,
        http_method: str,
        url: str,
        params: Dict[str, str],
        additional_headers: Dict[str, str],
    ) -> DiscoveryResponse:
        """Performs a Slack API request and returns the result.
        Args:
            token: Slack API Token (either bot token or user token)
            url: Complete URL (e.g., https://slack.com/api/discovery.enterprise.info)
            params: Form body params
            additional_headers: Request headers to append
        Returns:
            API response
        """

        # True/False -> "1"/"0"
        params = convert_bool_to_0_or_1(params)

        if self._logger.level <= logging.DEBUG:

            def convert_params(values: dict) -> dict:
                if not values or not isinstance(values, dict):
                    return {}
                return {
                    k: ("(bytes)" if isinstance(v, bytes) else v)
                    for k, v in values.items()
                }

            headers = {
                k: "(redacted)" if k.lower() == "authorization" else v
                for k, v in additional_headers.items()
            }
            self._logger.debug(
                f"Sending a request - {http_method} {url}, "
                f"params: {convert_params(params)}, "
                f"headers: {headers}"
            )

        request_headers = self._build_urllib_request_headers(
            token=self.token if token is None else token,
            additional_headers=additional_headers,
        )
        response = self._perform_urllib_http_request(
            http_method=http_method,
            url=url,
            headers=request_headers,
            params=params,
        )
        raw_body = response.get("body", "")
        parsed_body: Optional[dict] = None
        if len(raw_body) > 0:
            try:
                parsed_body = json.loads(raw_body)
            except json.decoder.JSONDecodeError:
                message = _build_unexpected_body_error_message(raw_body)
                raise DiscoveryApiError(message, response)

        return DiscoveryResponse(
            client=self,
            http_method=http_method,
            api_url=url,
            request_headers=request_headers,
            request_params=params,
            raw_body=raw_body,
            body=parsed_body,
            headers=dict(response["headers"]),
            status_code=response["status"],
        ).validate()

    def _perform_urllib_http_request(
        self,
        *,
        http_method: str = "POST",
        url: str,
        headers: Dict[str, str],
        params: Dict[str, str],
    ) -> Dict[str, any]:
        """Performs an HTTP request and parses the response.
        Args:
            url: Complete URL (e.g., https://slack.com/api/discovery.enterprise.info)
            args: args has "headers" and "params"
                "headers": Dict[str, str]
                "params": Dict[str, str],
        Returns:
            dict {status: int, headers: Headers, body: str}
        """
        url_encoded_params: str = urlencode(params or {})
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        # NOTE: Intentionally ignore the `http_verb` here
        # Slack APIs accepts any API method requests with POST methods
        try:
            # urllib not only opens http:// or https:// URLs, but also ftp:// and file://.
            # With this it might be possible to open local files on the executing machine
            # which might be a security risk if the URL to open can be manipulated by an external user.
            # (BAN-B310)
            if url.lower().startswith("http"):
                if http_method == "POST":
                    req = Request(
                        method="POST",
                        url=url,
                        data=url_encoded_params.encode("utf-8"),
                        headers=headers,
                    )
                elif http_method == "GET":
                    url = (
                        f"{url}&{url_encoded_params}"
                        if "?" in url
                        else f"{url}?{url_encoded_params}"
                    )
                    req = Request(method="GET", url=url, headers=headers)
                else:
                    raise DiscoveryRequestError(
                        f"Unsupported HTTP method: {http_method}"
                    )

                opener: Optional[OpenerDirector] = None
                if self.proxy is not None:
                    if isinstance(self.proxy, str):
                        opener = urllib.request.build_opener(
                            ProxyHandler({"http": self.proxy, "https": self.proxy}),
                            HTTPSHandler(context=self.ssl),
                        )
                    else:
                        raise DiscoveryRequestError(
                            f"Invalid proxy detected: {self.proxy} must be a str value"
                        )

                # NOTE: BAN-B310 is already checked above
                resp: Optional[HTTPResponse] = None
                if opener:
                    resp = opener.open(req, timeout=self.timeout)  # skipcq: BAN-B310
                else:
                    resp = urlopen(  # skipcq: BAN-B310
                        req, context=self.ssl, timeout=self.timeout
                    )

                charset = resp.headers.get_content_charset() or "utf-8"
                url_encoded_params: str = resp.read().decode(
                    charset
                )  # read the response body here
                return {
                    "status": resp.code,
                    "headers": resp.headers,
                    "body": url_encoded_params,
                }
            raise DiscoveryRequestError(f"Invalid URL detected: {url}")
        except HTTPError as e:
            resp = {"status": e.code, "headers": e.headers}
            if e.code == 429:
                # for compatibility with aiohttp
                resp["headers"]["Retry-After"] = resp["headers"]["retry-after"]

            # read the response body here
            charset = e.headers.get_content_charset() or "utf-8"
            url_encoded_params: str = e.read().decode(charset)
            resp["body"] = url_encoded_params
            return resp

        except Exception as err:
            self._logger.error(f"Failed to send a request to Slack API server: {err}")
            raise err

    def _build_urllib_request_headers(
        self, token: str, additional_headers: dict
    ) -> Dict[str, str]:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        headers.update(self.headers)
        if token:
            headers.update({"Authorization": "Bearer {}".format(token)})
        if additional_headers:
            headers.update(additional_headers)
        return headers
