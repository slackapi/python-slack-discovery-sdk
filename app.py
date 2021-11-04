# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import logging, os
from slack_discovery_sdk import DiscoveryClient

logging.basicConfig(level=logging.DEBUG)

enterprise_token = os.environ["SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN"]

client = DiscoveryClient(token=enterprise_token)
enterprise_info = client.discovery_enterprise_info()
print(enterprise_info.body)

# EXAMPLE USAGE BELOW

auth_test = client.auth_test()
user_conversations = client.discovery_user_conversations(
    user=auth_test["user_id"], limit=5
)
print(user_conversations)