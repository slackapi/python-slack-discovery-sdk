# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import logging, os, re, json
from slack_discovery_sdk import DiscoveryClient
from utils import export_json_to_file

logging.basicConfig(level=logging.DEBUG)

enterprise_token = os.environ["SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN"]

client = DiscoveryClient(token=enterprise_token)

DLP_LOGS_FILENAME = 'dlp_logs_output_'
EDISCOVERY_LOGS_FILENAME = 'ediscovery_logs_output_'
AUDIT_LOGS_FILENAME = 'audit_logs_output_'
CONVERSATIONS_RECENT_FILENAME = 'discovery_conversations_recent'
CONVERSATIONS_HISTORY_FILENAME = 'discovery_conversations_history'
EDITS_HISTORY_FILENAME = 'discovery_conversations_edits'

### CALL PATTERN OVERVIEW - User Based Discovery 
## Step 1 - We need a userID. This will be the user which we will query to see their conversations.
## Step 2 - Retrieve a list of conversation IDs a user is a member of using discovery.user.conversations
## Step 3 - Retrieve the message history for each conversation returned in Step 2 using discovery.conversations.history


## Step 1 - Get the user ID of the user you'd like to see conversation history from

auth_test = client.auth_test()
user_id = auth_test["user_id"]

## Step 2 - Use `discovery.user.conversations` to retrieve a list of conversation ID's 
# a user is a member of. We use limit of 500 here. 

list_of_conversations = client.discovery_user_conversations(
    user=user_id, limit=500
)

## Step 3 - Retrieve the message history for each conversation returned in Step 2 using discovery.conversations.history

print('listing convos')
print(list_of_conversations)

output_info = []

for conversation in list_of_conversations["channels"]:
    # print(conversation)
    #{'id': 'D02EZ1KTRF0', 'team_id': 'T02752RBD2R', 'date_joined': 1632242279, 'date_left': 0,
    # 'is_private': True, 'is_im': True, 'is_mpim': False, 'is_ext_shared': False}
    
    channel_id = conversation["id"]
    team_id = conversation["team_id"]
    output_info.append((channel_id, team_id))

    channel_conversation = client.discovery_conversations_history(
        channel=channel_id, team=team_id
    )
    channel_conversation_json = json.dumps(channel_conversation.body, indent=4)
    export_json_to_file(channel_conversation_json, CONVERSATIONS_HISTORY_FILENAME, channel_id, user_id)
    
    #print(channel_conversation)
    ##{'ok': True, 'messages': 
    # [{'client_msg_id': '6d917772-0b8a-4621-902c-ef85d9fd9987', 'type': 'message', 'text': 'affff', 'user': 'U0271AV54NS',
    # 'ts': '1627515227.000200', 'team': 'T02752RBD2R', 'blocks': 
    # [{'type': 'rich_text', 'block_id': 'YIj', 'elements': [{'type': 'rich_text_section', 'elements': 
    # [{'type': 'text', 'text': 'affff'}]}]}]}, {'client_msg_id': 'fbdaaba7-0abb-4323-8e02-7e7bc92c50ca', 
    # 'type': 'message', 'text': 'hello', 'user': 'U0271AV54NS', 'ts': '1625604656.000200', 'team': 'T02752RBD2R', 
    # 'blocks': [{'type': 'rich_text', 'block_id': 'WbOSU', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'hello'}]}]}]}], 'has_edits': False}

    