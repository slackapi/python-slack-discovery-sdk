# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import logging, os
from slack_discovery_sdk import DiscoveryClient

from tests.env_variable_names import (
    # An admin user token with discovery:read, discovery:write
    SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

enterprise_token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]

# Example usage of discovery.enterprise.info method below

client = DiscoveryClient(token=enterprise_token)
enterprise_info = client.discovery_enterprise_info()
logger.info(enterprise_info)
