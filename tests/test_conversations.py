# Copyright 2021, Slack Technologies, LLC. All rights reserved.
from typing import Any

import os, pytest, time, json
from slack_sdk import WebClient
from slack_discovery_sdk import DiscoveryClient
from slack_discovery_sdk.internal_utils import (
    get_random_string,
    get_timestamp_last_minute,
)
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

    def test_conversations_search(self):
        first_msg_text = "This message will test the search API"
        first_msg = None
        try:
            first_msg = self.web_client.chat_postMessage(
                channel=self.channel,
                text=first_msg_text,
            )
            # usually takes around 25 seconds for the conversations search to return this message as found
            time.sleep(25)

            # check for renames from the last minute, which should include the rename from above
            response = self.client.discovery_conversations_search(
                team=self.team,
                channel=self.channel,
                include_messages=True,
                query="search API",
            )

            while len(response["channels"]) <= 0:
                time.sleep(5)
                response = self.client.discovery_conversations_search(
                    team=self.team,
                    channel=self.channel,
                    include_messages=True,
                    query="search API",
                )

            assert (
                response["channels"][0]["message"]["text"] == first_msg_text
                and response["channels"][0]["message"]["ts"] == first_msg["ts"]
            )

        finally:
            # delete message from above
            if first_msg is not None:
                self.client.discovery_chat_delete(
                    team=first_msg["message"]["team"],
                    channel=self.channel,
                    ts=first_msg["ts"],
                )
                assert response["error"] is None

    def test_conversations_recent_limit(self):
        resp_limit = 2
        response = self.client.discovery_conversations_recent(limit=resp_limit)
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

    def test_conversations_history_pagination(self):
        conversations = []
        limit_size = 1
        page_num = 0
        for page in self.client.discovery_conversations_history(
            channel=self.channel, team=self.team, limit=limit_size
        ):
            for message in page["messages"]:
                conversations.append(json.dumps(message))
            page_num += 1
            if page_num > 5:
                break

        assert len(conversations) > limit_size
        # ensure we are getting different messages for each page
        assert sorted(set(conversations)) == sorted(conversations)

    def test_conversations_history_from_one_minute_ago(self):
        test_text = "This first message will be used to test getting conversation history from the last minute"
        first_msg = None
        try:
            first_msg = self.web_client.chat_postMessage(
                channel=self.channel,
                text=test_text,
            )

            # buffer time between posting messages and getting message history
            time.sleep(3)
            # test to only get messages that are less than one minute old
            response = self.client.discovery_conversations_history(
                limit=2,
                team=self.team,
                channel=self.channel,
                oldest=get_timestamp_last_minute(),
            )
            assert response["error"] is None

            # if there are multiple messages in the last minute, one of them should be the one from above
            found = next(
                (
                    message["text"]
                    for message in response["messages"]
                    if message["text"] == test_text
                ),
                None,
            )
            assert found == test_text

        finally:
            # clean up the messages we posted in this test by deleting them
            if first_msg is not None:
                self.client.discovery_chat_delete(
                    team=first_msg["message"]["team"],
                    channel=self.channel,
                    ts=first_msg["ts"],
                )

    def test_conversations_edits_from_one_minute_ago(self):
        # this test will create a message, edit it, and find edited messgages in the last minute
        updated_text = (
            "this message has been edited via chat_updateMessage API in a test"
        )
        msg_to_edit = None
        try:
            msg_to_edit = self.web_client.chat_postMessage(
                channel=self.channel,
                text="This message will be edited to test getting conversation history from the last minute",
            )
            self.web_client.chat_update(
                channel=self.channel,
                ts=msg_to_edit["ts"],
                text=updated_text,
            )
            time.sleep(1)
            # sleep for one second to make sure conversation_edits has time to see the latest chat_update
            # test to only get edited messages that are less than one minute old
            response = self.client.discovery_conversations_edits(
                limit=1,
                team=self.team,
                channel=self.channel,
                oldest=get_timestamp_last_minute(),
            )
            assert response["error"] is None
            # if there are more than one edits, one of them should be the one from above
            found = next(
                (
                    edit["text"]
                    for edit in response["edits"]
                    if edit["text"] == updated_text
                ),
                None,
            )
            assert found == updated_text
            # if there is only one message in the last minute, it should be the one we created above

        finally:
            # clean up message we posted in this test by deleting them
            if msg_to_edit is not None:
                self.client.discovery_chat_delete(
                    team=msg_to_edit["message"]["team"],
                    channel=self.channel,
                    ts=msg_to_edit["ts"],
                )

    def test_conversations_info_for_private_channel(self):
        test_channel = None
        try:
            # create channel for testing purposes - make sure we can get info on this channel
            test_channel = self.create_channel()
            test_channel_creation_time = test_channel["channel"]["created"]
            response = self.client.discovery_conversations_info(
                team=self.team, channel=test_channel["channel"]["id"]
            )
            assert response["error"] is None
            # if there are multiple channels, ensure we can find the one we created above
            found = next(
                (
                    info["created"]
                    for info in response["info"]
                    if info["created"] == test_channel_creation_time
                ),
                None,
            )
            assert found == test_channel_creation_time

        finally:
            # delete the test channel we created above
            if test_channel is not None:
                self.web_client.conversations_archive(
                    channel=test_channel["channel"]["id"]
                )

    def test_conversations_members_new_channel(self):
        test_channel = None
        try:
            test_channel = self.create_channel()
            convo_join_resp = self.web_client.conversations_join(
                channel=test_channel["channel"]["id"]
            )
            channel_creator = convo_join_resp["channel"]["creator"]
            response = self.client.discovery_conversations_members(
                team=self.team, channel=test_channel["channel"]["id"]
            )
            assert response["error"] is None

            # loop through members to ensure the creator is one of the members of the channel
            found = next(
                (
                    member["id"]
                    for member in response["members"]
                    if member["id"] == channel_creator
                ),
                None,
            )
            assert found == channel_creator

        finally:
            # delete the test channel we created above
            if test_channel is not None:
                self.web_client.conversations_archive(
                    channel=test_channel["channel"]["id"]
                )

    def test_conversations_renames(self):
        test_channel = None
        try:
            test_channel = self.create_channel()
            new_channel_name = get_random_string()

            self.web_client.conversations_rename(
                channel=test_channel["channel"]["id"], name=new_channel_name
            )

            # check for renames from the last minute, which should include the rename from above
            response = self.client.discovery_conversations_renames(
                team=self.team, oldest=get_timestamp_last_minute()
            )

            assert response["error"] is None
            # if there are multiple renames, one of them should be the one from above
            found = next(
                (
                    rename["new_name"]
                    for rename in response["renames"]
                    if rename["new_name"] == new_channel_name
                ),
                None,
            )
            assert found == new_channel_name

        finally:
            # delete the test channel we created above
            if test_channel is not None:
                self.web_client.conversations_archive(
                    channel=test_channel["channel"]["id"]
                )

    def test_conversations_reactions(self):
        test_text = "This message will test reactions"
        thumbs_reaction = "thumbsup"
        smile_reaction = "smile"
        limit_only_two = 2
        first_msg = None
        try:
            first_msg = self.web_client.chat_postMessage(
                channel=self.channel,
                text=test_text,
            )

            # add two reactions to the message sent above
            self.web_client.reactions_add(
                name=thumbs_reaction,
                channel=self.channel,
                timestamp=first_msg["ts"],
            )

            self.web_client.reactions_add(
                name=smile_reaction,
                channel=self.channel,
                timestamp=first_msg["ts"],
            )

            # check for renames from the last minute, which should include the rename from above
            response = self.client.discovery_conversations_reactions(
                team=self.team,
                channel=self.channel,
                oldest=get_timestamp_last_minute(),
                limit=limit_only_two,
            )

            assert response["error"] is None
            # if we have more than one reaction (which we should) check to make sure we have thumbs reaction
            found = next(
                (
                    reaction["name"]
                    for reaction in response["reactions"]
                    if reaction["name"] == smile_reaction
                ),
                None,
            )
            assert found == smile_reaction

        finally:
            # delete message from above
            if first_msg is not None:
                response = self.client.discovery_chat_delete(
                    team=first_msg["message"]["team"],
                    channel=self.channel,
                    ts=first_msg["ts"],
                )
                assert response["error"] is None

    def create_channel(self) -> any:
        test_channel = self.web_client.conversations_create(
            name=get_random_string(),
            team_id=self.team,
        )
        return test_channel
