# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import logging
from logging import NullHandler

# from .rtm import RTMClient  # noqa
from slack_discovery_sdk import DiscoveryClient  # noqa

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
