# Copyright 2021, Slack Technologies, LLC. All rights reserved.

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

        expected_message_subtype = "dlp_tombstone"

        try:

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

            assert tombstone_type == tombstone["message"]["subtype"]

        finally:
            # clean up the messages we posted in this test by deleting them
            if tombstone_msg is not None:
                self.client.discovery_chat_delete(
                    team=tombstone_msg["message"]["team"],
                    channel=self.channel,
                    ts=tombstone_msg["ts"],
                )

    def test_update(self):
        chat_update_text = "This message has been quarantined per DLP Policy 2.1.1"
        try:

            conversations = self.web_client.users_conversations(team_id=self.team)
            assert conversations.get("error") is None

            channel = conversations["channels"][0]["id"]
            message_to_update = self.web_client.chat_postMessage(
                channel=channel, text="The Discovery API will update this message soon."
            )
            assert message_to_update.get("error") is None

            update_msg_resp = self.client.discovery_chat_update(
                team=message_to_update["message"]["team"],
                channel=channel,
                ts=message_to_update["ts"],
                text=chat_update_text,
            )
            assert update_msg_resp["message"]["text"] == chat_update_text

        finally:

            # clean up the messages we posted in this test by deleting them
            if message_to_update is not None:
                self.client.discovery_chat_delete(
                    team=message_to_update["message"]["team"],
                    channel=self.channel,
                    ts=message_to_update["ts"],
                )

    def test_delete(self):
        try:

            conversations = self.web_client.users_conversations(team_id=self.team)
            assert conversations.get("error") is None

            channel = conversations["channels"][0]["id"]
            message_to_delete = self.web_client.chat_postMessage(
                channel=channel, text="The Discovery API will delete this message soon."
            )
            assert message_to_delete.get("error") is None

            delete_msg_resp = self.client.discovery_chat_delete(
                team=message_to_delete["message"]["team"],
                channel=channel,
                ts=message_to_delete["ts"],
            )
            assert delete_msg_resp.get("error") is None
            assert delete_msg_resp["ts"] == message_to_delete["ts"]

        finally:
            # clean up the messages we posted in this test by deleting them
            if message_to_delete is not None:
                self.client.discovery_chat_delete(
                    team=message_to_delete["message"]["team"],
                    channel=self.channel,
                    ts=message_to_delete["ts"],
                )

    def test_restore(self):
        restore_msg_text = (
            "The Discovery API will first tombstone this message and then restore it..."
        )
        try:

            conversations = self.web_client.users_conversations(team_id=self.team)
            assert conversations.get("error") is None

            tombstone_channel = conversations["channels"][0]["id"]
            message_to_restore = self.web_client.chat_postMessage(
                channel=tombstone_channel, text=restore_msg_text
            )
            assert message_to_restore.get("error") is None

            tombstone_msg_resp = self.client.discovery_chat_tombstone(
                team=message_to_restore["message"]["team"],
                channel=tombstone_channel,
                ts=message_to_restore["ts"],
                content="This message is currently being reviewed by XYZ Company",
            )
            assert tombstone_msg_resp.get("error") is None

            restore_msg = self.client.discovery_chat_restore(
                team=self.team,
                channel=tombstone_channel,
                ts=message_to_restore["ts"],
            )
            assert restore_msg.get("error") is None
            assert (
                restore_msg["message"]["ts"] == message_to_restore["ts"]
                and restore_msg["message"]["text"] == restore_msg_text
            )

        finally:
            # clean up the messages we posted in this test by deleting them
            if message_to_restore is not None:
                self.client.discovery_chat_delete(
                    team=message_to_restore["message"]["team"],
                    channel=self.channel,
                    ts=message_to_restore["ts"],
                )
