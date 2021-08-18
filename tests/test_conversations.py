import os, pytest, time
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

    # @pytest.mark.skip
    def test_conversations_recent_limit(self):
        resp_limit = 2
        response = self.client.discovery_conversations_recent(limit=resp_limit)
        assert response["error"] is None
        # ensure limit parameter is working properly
        assert len(response["channels"]) <= resp_limit

    # @pytest.mark.skip
    def test_conversations_list(self):
        response = self.client.discovery_conversations_list(limit=5)
        assert response["error"] is None

    # @pytest.mark.skip
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

    # @pytest.mark.skip
    def test_conversations_history_from_one_minute_ago(self):

        test_text = "This first message will be used to test getting conversation history from the last minute"

        try:
            first_msg = self.web_client.chat_postMessage(
                channel=self.channel,
                text=test_text,
            )

            # buffer time between posting messages and getting message history
            time.sleep(3)
            # test to only get messages that are less than one hour old
            response = self.client.discovery_conversations_history(
                limit=2,
                team=self.team,
                channel=self.channel,
                oldest=get_timestamp_last_minute(),
            )
            assert response["error"] is None
            # check to see if there are multiple messages in the last minute
            if len(response["messages"]) > 1 & len(response["messages"]) != 0:
                for message in response["messsages"]:
                    if message["text"] == test_text:
                        assert message["text"] == test_text
            # if there is only one message in the last minute, it should be the one we created above
            else:
                assert response["messages"][0]["text"] == test_text

        finally:
            # clean up the messages we posted in this test by deleting them
            self.client.discovery_chat_delete(
                team=first_msg["message"]["team"],
                channel=self.channel,
                ts=first_msg["ts"],
            )

    # @pytest.mark.skip
    def test_conversations_edits_from_one_minute_ago(self):
        # this test will create a message, edit it, and find edited messgages in the last minute

        updated_text = (
            "this message has been edited via chat_updateMessage API in a test"
        )
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
            # sleep for two seconds to make sure conversation_edits has time to see the latest chat_update
            # test to only get edited messages that are less than one minute old
            response = self.client.discovery_conversations_edits(
                limit=1,
                team=self.team,
                channel=self.channel,
                oldest=get_timestamp_last_minute(),
            )
            assert response["error"] is None
            # check the array of edits, and ensure we can find our message we edited from above
            if len(response["edits"]) > 1 & len(response["edits"]) != 0:
                for edit in response["edits"]:
                    if edit["text"] == updated_text:
                        assert edit["text"] == updated_text
            # if there is only one message in the last minute, it should be the one we created above
            else:
                assert response["edits"][0]["text"] == updated_text

        finally:
            # clean up message we posted in this test by deleting them
            self.client.discovery_chat_delete(
                team=msg_to_edit["message"]["team"],
                channel=self.channel,
                ts=msg_to_edit["ts"],
            )

    # @pytest.mark.skip
    def test_conversations_info_for_private_channel(self):

        try:
            # create channel for testing purposes - make sure we can get info on this channel
            test_channel = self.create_channel()
            test_channel_creation_time = test_channel["channel"]["created"]

            response = self.client.discovery_conversations_info(
                team=self.team, channel=test_channel["channel"]["id"]
            )

            if len(response["info"]) > 1 & len(response["info"]) != 0:
                for info in response["info"]:
                    if info["created"] == test_channel_creation_time:
                        assert info["created"] == test_channel_creation_time
            # if there is only one channel to get info on, it should be the one we created above
            else:
                assert response["info"][0]["created"] == test_channel_creation_time

        finally:
            # delete the test channel we created above
            self.web_client.conversations_archive(
                token=self.token, channel=test_channel["channel"]["id"]
            )

    # @pytest.mark.skip
    def test_conversations_members_new_channel(self):

        try:
            # create channel for testing purposes - make sure we can get info on this channel
            test_channel = self.create_channel()

            convo_join_resp = self.web_client.conversations_join(
                token=self.token,
                channel=test_channel["channel"]["id"],
            )

            channel_creator = convo_join_resp["channel"]["creator"]

            response = self.client.discovery_conversations_members(
                team=self.team, channel=test_channel["channel"]["id"]
            )

            assert response["error"] is None

            # loop through members to ensure the creator is one of the members of the channel
            if len(response["members"]) > 1 & len(response["members"]) != 0:
                for member in response["members"]:
                    if member["id"] == channel_creator:
                        assert member["id"] == channel_creator
            # if there is only one member it should be channel_creator
            else:
                assert response["members"][0]["id"] == channel_creator

        finally:
            # delete the test channel we created above
            self.web_client.conversations_archive(
                token=self.token, channel=test_channel["channel"]["id"]
            )

    # @pytest.mark.skip
    def test_conversations_renames(self):

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
            if len(response["renames"]) > 1:
                for rename in response["renames"]:
                    if rename == new_channel_name:
                        assert rename == new_channel_name
            else:
                assert response["renames"][0]["new_name"] == new_channel_name

        finally:
            # delete the test channel we created above
            self.web_client.conversations_archive(
                token=self.token, channel=test_channel["channel"]["id"]
            )

    # @pytest.mark.skip
    def test_conversations_reactions(self):

        test_text = "This message will test reactions"
        thumbs_reaction = "thumbsup"
        smile_reaction = "smile"
        limit_only_two = 2

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

            # if we have more than one reaction (which we should) check to make sure we have thumbs reaciton
            if len(response["reactions"]) > 1 & len(response["reactions"]) != 0:
                for reaction in response["reactions"]:
                    if reaction["name"] == thumbs_reaction:
                        assert (
                            reaction["name"] == thumbs_reaction
                            and reaction["ts"] == first_msg["ts"]
                        )
            # if there is only one reaction for some reason, it should be smile or thumbs
            else:
                assert (
                    response["reactions"][0]["name"] == smile_reaction
                    or thumbs_reaction
                )

        finally:
            # delete message from above
            self.client.discovery_chat_delete(
                team=first_msg["message"]["team"],
                channel=self.channel,
                ts=first_msg["ts"],
            )
            assert response["error"] is None

    @pytest.mark.skip
    def test_conversations_search(self):
        pass

    def create_channel(self) -> any:
        test_channel = self.web_client.conversations_create(
            name=get_random_string(),
            team_id=self.team,
        )
        return test_channel
