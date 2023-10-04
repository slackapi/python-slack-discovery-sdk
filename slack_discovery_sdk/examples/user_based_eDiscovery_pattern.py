# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import logging, os, json
from slack_discovery_sdk import DiscoveryClient  # type: ignore
from utils import export_json_to_file  # type: ignore

logging.basicConfig(level=logging.DEBUG)

enterprise_token = os.environ["SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN"]

client = DiscoveryClient(token=enterprise_token)

CONVERSATIONS_HISTORY_FILENAME = "discovery_conversations_history"

# CALL PATTERN OVERVIEW - User Based Discovery
# Step 1 - We need a userID. This will be the user which we will query to see their conversations.
# Step 2 - Retrieve a list of conversation IDs a user is a member of using discovery.user.conversations
# Step 3 - Retrieve the message history for each conversation returned in Step 2 using discovery.conversations.history


# Step 1 - Get the user ID of the user you'd like to see conversation history from

auth_test = client.auth_test()

# At this point, you should change the user_id variable to be the user_id of whichever user
# you'd like to see the conversation of. The auth_test is just used for testing purposes here.
user_id = auth_test["user_id"]

# Step 2 - Use `discovery.user.conversations` to retrieve a list of conversation ID's
# a user is a member of. user_id should be set to something *other* than auth_test at this point.

list_of_conversations = client.discovery_user_conversations(user=user_id, limit=500)

for conversation in list_of_conversations["channels"]:
    channel_id = conversation["id"]
    team_id = conversation["team_id"]

    # Step 3 - Retrieve the message history for each conversation returned in Step 2
    # using discovery.conversations.history

    channel_conversation = client.discovery_conversations_history(
        channel=channel_id, team=team_id
    )
    channel_conversation_json = json.dumps(channel_conversation.body, indent=4)
    export_json_to_file(
        new_items=channel_conversation_json,
        base_dir="./example-outputs/",
        logs_type=CONVERSATIONS_HISTORY_FILENAME,
        channel_id=channel_id,
        user_id=user_id,
    )
