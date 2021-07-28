import logging
from logging import NullHandler

# from .rtm import RTMClient  # noqa
from slack_discovery_sdk import WebClient  # noqa

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())