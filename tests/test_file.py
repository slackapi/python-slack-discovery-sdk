import os
from slack_discovery_sdk import DiscoveryClient
from slack_sdk import WebClient
from tests.env_variable_names import (
    SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_TEAM_ID,
    SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID,
    SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN
)


class TestFile:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        self.team = os.environ[SLACK_DISCOVERY_SDK_TEST_TEAM_ID]
        self.channel = os.environ[SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID]
        self.client = DiscoveryClient(token=self.token)
        self.web_client = WebClient(
            token=os.environ[SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN]
        )
    def test_files_list(self):
        resp_limit = 2
        response = self.client.discovery_files_list(team=self.team, limit=resp_limit)
        assert response["error"] is None
        # ensure limit parameter is working properly
        assert len(response["files"]) <= resp_limit

    def test_files_list_pagination(self):
        files = []
        limit_size = 2
        page_num = 0
        for page in self.client.discovery_files_list(limit=limit_size):
            files = files + page["files"]
            page_num += 1
            if page_num > 5:
                break
        assert len(files) > limit_size

    def test_file_info_for_text_file(self):
        test_content = "This is used to test file upload"
        test_upload_file_type = 'text'

        try: 
            
            file_upload = self.web_client.files_upload(
                channels=self.channel,
                content=test_content,
            )

            file_info_resp = self.client.discovery_file_info(
                file=file_upload["file"]["id"],
            )
            
            assert file_info_resp["error"] is None
            assert file_info_resp["file"]["filetype"] == test_upload_file_type
        
        finally:
            # clean up the test file
            self.web_client.files_delete(file=file_upload["file"]["id"])

    def test_file_tombstone(self):
        resp_limit = 2
        files_list_resp = self.client.discovery_files_list(
            team=self.team, limit=resp_limit
        )
        assert files_list_resp["error"] is None
        # ensure limit parameter is working properly
        assert len(files_list_resp["files"]) <= resp_limit
        if len(files_list_resp["files"]) >= 1:
            first_file = files_list_resp["files"][0]["id"]
            file_tombstone_resp = self.client.discovery_file_tombstone(file=first_file)
            assert file_tombstone_resp["error"] is None

    def test_file_restore(self):
        resp_limit = 2
        files_list_resp = self.client.discovery_files_list(
            team=self.team, limit=resp_limit
        )
        assert files_list_resp["error"] is None
        # ensure limit parameter is working properly
        assert len(files_list_resp["files"]) <= resp_limit
        if len(files_list_resp["files"]) >= 1:
            first_file = files_list_resp["files"][0]["id"]
            file_restore_resp = self.client.discovery_file_restore(file=first_file)
            assert file_restore_resp["error"] is None

    def test_file_delete(self):
        resp_limit = 2
        files_list_resp = self.client.discovery_files_list(
            team=self.team, limit=resp_limit
        )
        assert files_list_resp["error"] is None
        # ensure limit parameter is working properly
        assert len(files_list_resp["files"]) <= resp_limit
        if len(files_list_resp["files"]) >= 1:
            first_file = files_list_resp["files"][0]["id"]
            file_delete_resp = self.client.discovery_file_delete(file=first_file)
            assert file_delete_resp["error"] is None
