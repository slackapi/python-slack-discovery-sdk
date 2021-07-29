"""Errors that can be raised by this SDK"""


class SlackClientError(Exception):
    """Base class for Client errors"""


class SlackRequestError(SlackClientError):
    """Error raised when there's a problem with the request that's being submitted."""


class SlackApiError(SlackClientError):
    """Error raised when Slack does not send the expected response.

    Attributes:
        response (SlackResponse): The SlackResponse object containing all of the data sent back from the API.

    Note:
        The message (str) passed into the exception is used when
        a user converts the exception to a str.
        i.e. str(SlackApiError("This text will be sent as a string."))
    """

    def __init__(self, message, response):
        msg = f"{message}\nThe server responded with: {response}"
        self.response = response
        super(SlackApiError, self).__init__(msg)
