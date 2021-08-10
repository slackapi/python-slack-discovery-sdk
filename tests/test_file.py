import os
from slack_discovery_sdk import DiscoveryClient
from tests.env_variable_names import SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN, SLACK_DISCOVERY_SDK_TEST_TEAM_ID, SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID

class TestFile:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        self.team = os.environ[SLACK_DISCOVERY_SDK_TEST_TEAM_ID]
        self.channel = os.environ[SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID]
        self.client = DiscoveryClient(token=self.token)

    def test_files_list(self):
        resp_limit = 2
        response = self.client.discovery_files_list(
            team=self.team, 
            limit=resp_limit
        )
        assert response["error"] is None
        #ensure limit parameter is working properly
        assert len(response["files"]) <= resp_limit

    def test_file_info(self):
        resp_limit = 2
        files_list_resp = self.client.discovery_files_list(
            team=self.team, 
            limit=resp_limit
        )
        assert files_list_resp["error"] is None
        #ensure limit parameter is working properly
        assert len(files_list_resp["files"]) <= resp_limit
        if len(files_list_resp["files"]) >= 1:
            first_file = files_list_resp["files"][0]["id"]
            file_info_resp = self.client.discovery_file_info(file=first_file)
            assert file_info_resp["error"] is None
 
    def test_file_tombstone(self):
        resp_limit = 2
        files_list_resp = self.client.discovery_files_list(
            team=self.team, 
            limit=resp_limit
        )
        assert files_list_resp["error"] is None
        #ensure limit parameter is working properly
        assert len(files_list_resp["files"]) <= resp_limit
        if len(files_list_resp["files"]) >= 1:
            first_file = files_list_resp["files"][0]["id"]
            file_tombstone_resp = self.client.discovery_file_tombstone(file=first_file)
            assert file_tombstone_resp["error"] is None

    def test_file_restore(self):
        resp_limit = 2
        files_list_resp = self.client.discovery_files_list(
            team=self.team, 
            limit=resp_limit
        )
        assert files_list_resp["error"] is None
        #ensure limit parameter is working properly
        assert len(files_list_resp["files"]) <= resp_limit
        if len(files_list_resp["files"]) >= 1:
            first_file = files_list_resp["files"][0]["id"]
            file_tombstone_resp = self.client.discovery_file_restore(file=first_file)
            assert file_tombstone_resp["error"] is None

    def test_file_delete(self):
        resp_limit = 2
        files_list_resp = self.client.discovery_files_list(
            team=self.team, 
            limit=resp_limit
        )
        assert files_list_resp["error"] is None
        #ensure limit parameter is working properly
        assert len(files_list_resp["files"]) <= resp_limit
        if len(files_list_resp["files"]) >= 1:
            first_file = files_list_resp["files"][0]["id"]
            file_delete_resp = self.client.discovery_file_delete(file=first_file)
            assert file_delete_resp["error"] is None