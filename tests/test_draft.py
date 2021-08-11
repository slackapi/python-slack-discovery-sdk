import os
from slack_discovery_sdk import DiscoveryClient
from tests.env_variable_names import (
    SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_TEAM_ID,
    SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID,
)


class TestDraft:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        self.team = os.environ[SLACK_DISCOVERY_SDK_TEST_TEAM_ID]
        self.channel = os.environ[SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID]
        self.client = DiscoveryClient(token=self.token)

    def test_drafts_list(self):
        resp_limit = 3
        response = self.client.discovery_drafts_list(team=self.team, limit=resp_limit)
        assert response["error"] is None
        # ensure limit parameter is working properly
        assert len(response["drafts"]) <= resp_limit

    def test_draft_info(self):
        resp_limit = 2
        response = self.client.discovery_drafts_list(team=self.team, limit=resp_limit)
        assert response["error"] is None
        if len(response["drafts"]) > 1:
            user = response["drafts"][0]["user_id"]
            team = response["drafts"][0]["team_id"]
            draft = response["drafts"][0]["id"]
            info_response = self.client.discovery_draft_info(
                team=team, draft=draft, user=user, limit=resp_limit
            )
            assert info_response["error"] is None
