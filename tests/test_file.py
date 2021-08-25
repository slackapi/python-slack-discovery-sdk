# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import os
from slack_discovery_sdk import DiscoveryClient
from slack_discovery_sdk.response import DiscoveryResponse
from slack_sdk import WebClient
from tests.env_variable_names import (
    SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN,
    SLACK_DISCOVERY_SDK_TEST_TEAM_ID,
    SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID,
    SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN,
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

        test_upload_file_type = "text"
        file_upload = None

        try:

            file_upload = self.create_file()
            file_info_resp = self.client.discovery_file_info(
                file=file_upload["file"]["id"],
            )

            assert file_info_resp["error"] is None
            assert file_info_resp["file"]["filetype"] == test_upload_file_type

        finally:
            # clean up the test file
            self.web_client.files_delete(file=file_upload["file"]["id"])

    def test_file_tombstone(self):

        file_upload = None

        try:

            file_upload = self.create_file()
            file_id = file_upload["file"]["id"]

            file_tombstone_resp = self.client.discovery_file_tombstone(
                file=file_id,
            )
            assert (
                file_id == file_tombstone_resp["file"]["id"]
                and file_tombstone_resp["file"]["is_tombstoned"] == True
            )

        finally:
            # clean up the test file - first we have to restore, then we can delete
            self.client.discovery_file_restore(file=file_upload["file"]["id"])
            self.web_client.files_delete(file=file_upload["file"]["id"])

    def test_file_restore(self):

        file_upload = None

        try:

            file_upload = self.create_file()
            file_id = file_upload["file"]["id"]

            self.client.discovery_file_tombstone(file=file_id)

            file_restore_resp = self.client.discovery_file_restore(
                file=file_upload["file"]["id"]
            )

            assert (
                file_id == file_restore_resp["file"]["id"]
                and file_restore_resp["file"]["is_tombstoned"] == False
            )

        finally:
            # clean up the test file - first we have to restore, then we can delete
            self.web_client.files_delete(file=file_upload["file"]["id"])

    def test_file_delete(self):

        file_upload = None

        try:

            file_upload = self.create_file()
            file_id = file_upload["file"]["id"]
            file_delete_resp = self.client.discovery_file_delete(
                file=file_upload["file"]["id"]
            )

            assert (
                file_id == file_delete_resp["file"] and file_delete_resp["ok"] == True
            )

        finally:
            # can pass as we already delete file above
            pass

    # aux function which uploads a text-based file
    def create_file(self) -> DiscoveryResponse:
        test_content = "This is used to test file upload"

        file_upload = self.web_client.files_upload(
            channels=self.channel,
            content=test_content,
        )
        return file_upload
