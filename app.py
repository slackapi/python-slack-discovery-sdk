import logging, os
from slack_discovery_sdk import DiscoveryClient

logging.basicConfig(level=logging.DEBUG)

enterprise_token = os.environ["SLACK_ENTERPRISE_TOKEN"]

# The Bot Token is optional, some customers may not have one
# slack_token = os.environ["SLACK_BOT_TOKEN"]

client = DiscoveryClient(token=enterprise_token)
enterprise_info = client.discovery_enterprise_info()
print(enterprise_info)

# EXAMPLE USAGE BELOW

auth_test = client.auth_test()
user_conversations = client.discovery_user_conversations(
    user=auth_test["user_id"], limit=5
)
print(user_conversations)
