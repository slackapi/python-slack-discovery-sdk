"""A Python module for interacting and consuming responses from Slack."""

import logging
from typing import Optional

import slack_discovery_sdk.errors as e
from .internal_utils import _next_cursor_is_present


class DiscoveryResponse:
    """An iterable container of response data.
    Attributes:
        body (dict): The json-encoded content of the response. Along
            with the headers and status code information.
    Methods:
        validate: Check if the response from Slack was successful.
        get: Retrieves any key from the response data.
        next: Retrieves the next portion of results,
            if 'next_cursor' is present.
    Example:
    ```python
    import os
    from slack_discovery_sdk import DiscoveryClient
    client = DiscoveryClient(token=os.environ['SLACK_ORG_ADMIN_TOKEN'])
    users = []
    for page in client.discovery_users_list():
        users = users + page['members']
    ```
    Note:
        Some responses return collections of information
        like channel and user lists. If they do it's likely
        that you'll only receive a portion of results. This
        object allows you to iterate over the response which
        makes subsequent API requests until your code hits
        'break' or there are no more results to be found.
        Any attributes or methods prefixed with _underscores are
        intended to be "private" internal use only. They may be changed or
        removed at anytime.
    """

    def __init__(
        self,
        *,
        client: "BaseDiscoveryClient",
        http_verb: str,
        api_url: str,
        request_headers: dict,
        request_params: Optional[dict],
        raw_body: str,
        body: dict,
        headers: dict,
        status_code: int,
    ):
        self.http_verb = http_verb
        self.api_url = api_url
        self.request_headers = request_headers
        self.request_params = request_params
        self.raw_body = raw_body
        self.body = body
        self.headers = headers
        self.status_code = status_code
        self._initial_data = body
        self._iteration = None  # for __iter__ & __next__
        self._client = client
        self._logger = logging.getLogger(__name__)

    def __str__(self):
        """Return the Response data if object is converted to a string."""
        return f"{self.body}"

    def __getitem__(self, key):
        """Retrieves any key from the data store.
        Note:
            This is implemented so users can reference the
            SlackResponse object like a dictionary.
            e.g. response["ok"]
        Returns:
            The value from data or None.
        """
        return self.body.get(key, None)

    def __iter__(self):
        """Enables the ability to iterate over the response.
        It's required for the iterator protocol.
        Note:
            This enables Slack cursor-based pagination.
        Returns:
            (SlackResponse) self
        """
        self._iteration = 0
        self.body = self._initial_data
        return self

    def __next__(self):
        """Retrieves the next portion of results, if 'next_cursor' is present.
        Note:
            Some responses return collections of information
            like channel and user lists. If they do it's likely
            that you'll only receive a portion of results. This
            method allows you to iterate over the response until
            your code hits 'break' or there are no more results
            to be found.
        Returns:
            (SlackResponse) self
                With the new response data now attached to this object.
        Raises:
            SlackApiError: If the request to the Slack API failed.
            StopIteration: If 'next_cursor' is not present or empty.
        """
        self._iteration += 1
        if self._iteration == 1:
            return self
        if _next_cursor_is_present(self.body):  # skipcq: PYL-R1705
            params = self.request_params or {}
            # cursor
            next_cursor = self.body.get("response_metadata", {}).get("next_cursor")
            params.update({"cursor": next_cursor})
            # offset for https://api.slack.com/enterprise/discovery/methods#users_list etc.
            params.update({"offset": self.body.get("offset")})

            response = self._client.fetch_next_page(  # skipcq: PYL-W0212
                api_url=self.api_url,
                headers=self.request_headers,
                params=params,
            )
            self.status_code = response["status_code"]
            self.headers = response["headers"]
            self.body = response["body"]
            return self.validate()
        else:
            raise StopIteration

    def get(self, key, default=None):
        """Retrieves any key from the response data.
        Note:
            This is implemented so users can reference the
            SlackResponse object like a dictionary.
            e.g. response.get("ok", False)
        Returns:
            The value from data or the specified default.
        """
        return self.body.get(key, default)

    def validate(self):
        """Check if the response from Slack was successful.
        Returns:
            (SlackResponse)
                This method returns it's own object. e.g. 'self'
        Raises:
            SlackApiError: The request to the Slack API failed.
        """
        if self._logger.level <= logging.DEBUG:
            self._logger.debug(
                "Received the following response - "
                f"status: {self.status_code}, "
                f"headers: {dict(self.headers)}, "
                f"body: {self.body}"
            )
        if (
            self.status_code == 200
            and self.body is not None
            and self.body.get("ok", False)
        ):
            return self
        msg = "The request to the Slack API failed."
        raise e.SlackApiError(message=msg, response=self)
