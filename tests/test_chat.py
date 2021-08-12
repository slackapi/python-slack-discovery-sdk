import os
from slack_sdk import WebClient
from slack_discovery_sdk import DiscoveryClient
from .env_variable_names import (
    SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_TEAM_ID,
    SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID,
)


class TestChat:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        self.team = os.environ[SLACK_DISCOVERY_SDK_TEST_TEAM_ID]
        self.channel = os.environ[SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID]
        self.client = DiscoveryClient(token=self.token)
        self.web_client = WebClient(
            token=os.environ[SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN]
        )

    def test_tombstone(self):
        conversations = self.web_client.users_conversations(team_id=self.team)
        assert conversations.get("error") is None

        tombstone_channel = conversations["channels"][0]["id"]
        tombstone_msg = self.web_client.chat_postMessage(
            channel=tombstone_channel,
            text="The Discovery API will find this message...",
        )
        assert tombstone_msg.get("error") is None

        tombstone = self.client.discovery_chat_tombstone(
            team=tombstone_msg["message"]["team"],
            channel=tombstone_channel,
            ts=tombstone_msg["ts"],
            content="This message is currently being reviewed by XYZ Company",
        )
        assert tombstone.get("error") is None

    def test_update(self):
        conversations = self.web_client.users_conversations(team_id=self.team)
        assert conversations.get("error") is None

        channel = conversations["channels"][0]["id"]
        new_message = self.web_client.chat_postMessage(
            channel=channel, text="The Discovery API will update this message soon."
        )
        assert new_message.get("error") is None

        update_msg_resp = self.client.discovery_chat_update(
            team=new_message["message"]["team"],
            channel=channel,
            ts=new_message["ts"],
            text="This message has been quarantined per DLP Policy 2.1.1",
        )
        assert update_msg_resp.get("error") is None

    def test_delete(self):
        conversations = self.web_client.users_conversations(team_id=self.team)
        assert conversations.get("error") is None

        channel = conversations["channels"][0]["id"]
        new_message = self.web_client.chat_postMessage(
            channel=channel, text="The Discovery API will delete this message soon."
        )
        assert new_message.get("error") is None

        delete_msg_resp = self.client.discovery_chat_delete(
            team=new_message["message"]["team"],
            channel=channel,
            ts=new_message["ts"],
        )
        assert delete_msg_resp.get("error") is None

    def test_restore(self):
        conversations = self.web_client.users_conversations(team_id=self.team)
        assert conversations.get("error") is None

        tombstone_channel = conversations["channels"][0]["id"]
        tombstone_msg = self.web_client.chat_postMessage(
            channel=tombstone_channel,
            text="The Discovery API will first tombstone this message and then restore it...",
        )
        assert tombstone_msg.get("error") is None

        tombstone_msg_resp = self.client.discovery_chat_tombstone(
            team=tombstone_msg["message"]["team"],
            channel=tombstone_channel,
            ts=tombstone_msg["ts"],
            content="This message is currently being reviewed by XYZ Company",
        )
        assert tombstone_msg_resp.get("error") is None

        restore_msg = self.client.discovery_chat_restore(
            team=self.team,
            channel=tombstone_channel,
            ts=tombstone_msg["ts"],
        )

        assert restore_msg.get("error") is None
