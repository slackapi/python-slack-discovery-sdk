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

        try:
            first_msg = self.web_client.chat_postMessage(
                channel=self.channel,
                text="This first message will be used to test getting conversation history from the last minute",
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
            assert len(response["messages"]) >= 1

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

        try:

            msg_to_edit = self.web_client.chat_postMessage(
                channel=self.channel,
                text="This message will be edited to test getting conversation history from the last minute",
            )

            self.web_client.chat_update(
                channel=self.channel,
                ts=msg_to_edit["ts"],
                text="this message has been edited via chat_updateMessage API in a test",
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
            print(response)
            # timestamp of the edits response should be the same as the msg we created
            assert response["edits"][0]["original_ts"] == msg_to_edit["ts"]

        finally:
            # clean up message we posted in this test by deleting them
            self.client.discovery_chat_delete(
                team=msg_to_edit["message"]["team"],
                channel=self.channel,
                ts=msg_to_edit["ts"],
            )

    # @pytest.mark.skip
    def test_conversations_info_for_private_channel(self):
        test_channel_name = get_random_string()

        try:
            # create channel for testing purposes - make sure we can get info on this channel
            test_channel = self.web_client.conversations_create(
                name=test_channel_name, team_id=self.team
            )

            response = self.client.discovery_conversations_info(
                team=self.team, channel=test_channel["channel"]["id"]
            )

            assert response["info"][0]["name"] == test_channel_name

        finally:
            # delete the test channel we created above
            self.web_client.admin_conversations_delete(
                token=self.token, channel_id=test_channel["channel"]["id"]
            )

    def test_conversations_members_new_channel(self):

        try:
            # create channel for testing purposes - make sure we can get info on this channel
            test_channel = self.create_channel()

            self.web_client.conversations_join(
                token=self.token,
                channel=test_channel["channel"]["id"],
            )

            response = self.client.discovery_conversations_members(
                team=self.team, channel=test_channel["channel"]["id"]
            )
            assert response["error"] is None

        finally:
            # delete the test channel we created above
            self.web_client.admin_conversations_delete(
                token=self.token, channel_id=test_channel["channel"]["id"]
            )

    @pytest.mark.skip
    def test_conversations_renames(self):

        test_channel = self.web_client.conversations_create(
            name=get_random_string(),
            team_id=self.team,
        )

        response = self.client.discovery_conversations_renames(
            team=self.team, private=False
        )
        assert response["error"] is None

    @pytest.mark.skip
    def test_conversations_reactions(self):
        response = self.client.discovery_conversations_renames(
            team=self.team, channel=self.channel
        )
        assert response["error"] is None

    @pytest.mark.skip
    def test_conversations_search(self):
        response = self.client.discovery_conversations_search(query="hello")
        assert response["error"] is None

    def create_channel(self) -> any:
        test_channel = self.web_client.conversations_create(
            name=get_random_string(),
            team_id=self.team,
        )
        return test_channel
