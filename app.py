import logging, os
from slack_bolt import App
from slack_discovery_sdk import WebClient

app = App()

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)
channelID = os.environ["CHANNEL_ID"]
teamID = os.environ["TEAM_ID"]
bearerToken = os.environ["BEARER_TOKEN"]

print(bearerToken)
print(channelID)
print(teamID)

response = client.discovery_enterprise_info(
    token=bearerToken
)

print(response)