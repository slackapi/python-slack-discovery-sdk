import os, time
from slack_sdk import WebClient
from slack_discovery_sdk import DiscoveryClient
from tests.env_variable_names import (
    SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_TEAM_ID,
    SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID,
    SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN,
)


class TestConversations:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        self.team = os.environ[SLACK_DISCOVERY_SDK_TEST_TEAM_ID]
        self.channel = os.environ[SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID]
        self.client = DiscoveryClient(token=self.token)
        self.web_client = WebClient(
            token=os.environ[SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN]
        )

    def test_conversations_recent_limit(self):
        resp_limit = 2
        response = self.client.discovery_conversations_recent(limit=resp_limit)
        print(response)
        assert response["error"] is None
        # ensure limit parameter is working properly
        assert len(response["channels"]) <= resp_limit

    def test_conversations_list(self):
        response = self.client.discovery_conversations_list(limit=5)
        assert response["error"] is None

    def test_conversations_list_pagination(self):
        conversations = []
        limit_size = 2
        page_num = 0
        for page in self.client.discovery_conversations_list(limit=limit_size):
            conversations = conversations + page["channels"]
            page_num += 1
            if page_num > 5:
                break
        assert len(conversations) > limit_size

    def test_conversations_history_one_minute_old_messages_only(self):
        now = time.time()
        seconds_in_one_minue = 60
        one_minute_ago = now - seconds_in_one_minue
        first_msg = self.web_client.chat_postMessage(
            channel=self.channel,
            text="This first message will be used to make sure we can get messages in the last minute",
        )
        second_msg = self.web_client.chat_postMessage(
            channel=self.channel,
            text="This second message will be used to make sure we can get messages in the last minute",
        )
        # test to only get messages that are less than one hour old
        response = self.client.discovery_conversations_history(
            limit=2, team=self.team, channel=self.channel, oldest=one_minute_ago
        )
        assert response["error"] is None 
        assert len(response["messages"]) == 2
        # clean up the messages we posted in this test by deleting them

        self.client.discovery_chat_delete(
            team=first_msg["message"]["team"],
            channel=self.channel,
            ts=first_msg["ts"],
        )
        self.client.discovery_chat_delete(
            team=second_msg["message"]["team"],
            channel=self.channel,
            ts=second_msg["ts"],
        )


    def test_conversations_edits(self):
        response = self.client.discovery_conversations_edits(
            limit=5, team=self.team, channel=self.channel
        )
        assert response["error"] is None

    def test_conversations_info(self):
        response = self.client.discovery_conversations_info(
            team=self.team, channel=self.channel
        )
        assert response["error"] is None

    def test_conversations_members(self):
        response = self.client.discovery_conversations_members(
            team=self.team, channel=self.channel
        )
        assert response["error"] is None

    def test_conversations_renames(self):
        response = self.client.discovery_conversations_renames(
            team=self.team, private=False
        )
        assert response["error"] is None

    def test_conversations_reactions(self):
        response = self.client.discovery_conversations_renames(
            team=self.team, channel=self.channel
        )
        assert response["error"] is None

    def test_conversations_search(self):
        response = self.client.discovery_conversations_search(query="hello")
        assert response["error"] is None
