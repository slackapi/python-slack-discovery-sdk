import logging, os
from slack_bolt import App
from slack_discovery_sdk import WebClient

app = App()

enterpriseToken = os.environ["ENTERPRISE_TOKEN"]

# The Bot Token is optional, some customers may not have one
# slack_token = os.environ["SLACK_BOT_TOKEN"]

client = WebClient(token=enterpriseToken)

channelID = os.environ["CHANNEL_ID"]
teamID = os.environ["TEAM_ID"]
userID = os.environ["USER_ID"]

print(channelID)
print(teamID)

# EXAMPLE USAGE BELOW

response = client.discovery_user_conversations(
    token=enterpriseToken,
    user=userID
)

print(response)