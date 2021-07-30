"""Errors that can be raised by this SDK"""


class DiscoveryClientError(Exception):
    """Base class for Client errors"""


class DiscoveryRequestError(DiscoveryClientError):
    """Error raised when there's a problem with the request that's being submitted."""


class DiscoveryApiError(DiscoveryClientError):
    """Error raised when Slack does not send the expected response.

    Attributes:
        response (DiscoveryResponse): The SlackResponse object containing all of the data sent back from the API.

    Note:
        The message (str) passed into the exception is used when
        a user converts the exception to a str.
        i.e. str(DiscoveryApiError("This text will be sent as a string."))
    """

    def __init__(self, message, response):
        msg = f"{message}\nThe server responded with: {response}"
        self.response = response
        super(DiscoveryApiError, self).__init__(msg)
