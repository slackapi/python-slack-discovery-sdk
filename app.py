import logging, os
from slack_discovery_sdk import DiscoveryClient

logging.basicConfig(level=logging.DEBUG)

enterprise_token = os.environ["ENTERPRISE_TOKEN"]

# The Bot Token is optional, some customers may not have one
# slack_token = os.environ["SLACK_BOT_TOKEN"]

client = DiscoveryClient(token=enterprise_token)

channelID = os.environ["CHANNEL_ID"]
teamID = os.environ["TEAM_ID"]
userID = os.environ["USER_ID"]

print(channelID)
print(teamID)

# EXAMPLE USAGE BELOW

response = client.discovery_user_conversations(token=enterprise_token, user=userID)

print(response)
