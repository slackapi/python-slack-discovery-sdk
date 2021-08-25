# ------------------------------------------------
# discovery.conversations.recent
# ------------------------------------------------


# def test_chat_info(self):
#     response = self.client.discovery_chat_info(team=self.team, channel=self.channel, ts='1626983542.000400')
#     assert response["error"] is None

import os
from slack_discovery_sdk import DiscoveryClient
from tests.env_variable_names import (
    SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_TEAM_ID,
    SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID,
)


class TestConversations:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        self.team = os.environ[SLACK_DISCOVERY_SDK_TEST_TEAM_ID]
        self.channel = os.environ[SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID]
        self.client = DiscoveryClient(token=self.token)

    def test_conversations_recent(self):
        resp_limit = 2
        response = self.client.discovery_conversations_recent(limit=resp_limit)
        print(response)
        assert response["error"] is None
        # ensure limit parameter is working properly
        assert len(response["channels"]) <= resp_limit

    def test_conversations_list(self):
        response = self.client.discovery_conversations_list(limit=5)
        assert response["error"] is None

    def test_conversations_history(self):
        response = self.client.discovery_conversations_history(
            limit=5, team=self.team, channel=self.channel
        )
        assert response["error"] is None

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

    # def test_conversations_search(self):
    #     response = self.client.discovery_conversations_search(query='hello')
    #     assert response["error"] is None

          two_min_ago_ts = get_timestamp_last_minute() - 60
            # time.sleep(16)
            print(self.team)
            print(get_timestamp_last_minute())

            found = False
            count = 0
            while found != True:
                print('inside while')
                time.sleep(5)
                response = self.client.discovery_conversations_search(
                    query=' getting conversation history', team=self.team, include_messages=True, oldest=two_min_ago_ts
                )
                print(response)

                if len(response["channels"]) < 1:
                    print(count)
                    count = count + 1
                    continue
                else:
                    found=True
                    break
            
            print('after break')
            for response in response["channels"]:
                        if response["message"]["text"] == 'This message will be edited to test getting conversation history from the last minute':
                            found=True
                            assert response["message"]["text"] == 'This message will be edited to test getting conversation history from the last minute'
