import logging, os
from slack_bolt import App
from slack_discovery_sdk import WebClient

app = App()

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)
channelID = os.environ["CHANNEL_ID"]
teamID = os.environ["TEAM_ID"]

response = client.conversations_info(
    channel=channelID,
    team=teamID,
)

print(response)