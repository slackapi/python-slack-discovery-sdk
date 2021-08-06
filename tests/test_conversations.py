import os
from slack_discovery_sdk import DiscoveryClient
from tests.env_variable_names import SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN, SLACK_DISCOVERY_SDK_TEST_TEAM_ID, SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID

class TestConversations:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        self.team = os.environ[SLACK_DISCOVERY_SDK_TEST_TEAM_ID]
        self.channel = os.environ[SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID]
        self.client = DiscoveryClient(token=self.token)

    def test_conversations_recent(self):
        response = self.client.discovery_conversations_recent(limit=2)
        assert response["error"] is None

    def test_conversations_list(self):
        response = self.client.discovery_conversations_list(limit=5)
        assert response["error"] is None
    
    def test_conversations_history(self):
        response = self.client.discovery_conversations_history(limit=5, team=self.team, channel=self.channel)
        assert response["error"] is None

    def test_conversations_edits(self):
        response = self.client.discovery_conversations_edits(limit=5, team=self.team, channel=self.channel)
        assert response["error"] is None
    
    def test_conversations_info(self):
        response = self.client.discovery_conversations_info(team=self.team, channel=self.channel)
        assert response["error"] is None
    
    def test_conversations_members(self):
        response = self.client.discovery_conversations_members(team=self.team, channel=self.channel)
        assert response["error"] is None

    def test_conversations_renames(self):
        response = self.client.discovery_conversations_renames(team=self.team, private=False)
        assert response["error"] is None

    def test_conversations_reactions(self):
        response = self.client.discovery_conversations_renames(team=self.team, channel=self.channel)
        assert response["error"] is None

    def test_conversations_search(self):
        response = self.client.discovery_conversations_search(query='hello')
        assert response["error"] is None
