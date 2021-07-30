import os
from slack_sdk import WebClient
from slack_discovery_sdk import DiscoveryClient
from .env_variable_names import (
    SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_TEAM_ID,
)


class TestChat:
    def setup_method(self):
        pass

    def test_tombstone(self):
        team_id = os.environ[SLACK_DISCOVERY_SDK_TEST_TEAM_ID]
        web_client = WebClient(token=os.environ[SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN])
        conversations = web_client.users_conversations(team_id=team_id)
        assert conversations.get("error") is None

        channel = conversations["channels"][0]["id"]
        new_message = web_client.chat_postMessage(
            channel=channel, text="The Discovery API will find this message..."
        )
        assert new_message.get("error") is None

        discovery_client = DiscoveryClient(
            token=os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        )

        tombstone = discovery_client.discovery_chat_tombstone(
            team=new_message["message"]["team"],
            channel=channel,
            ts=new_message["ts"],
            content="This message is currently being reviewed by XYZ Company",
        )
        assert tombstone.get("error") is None
