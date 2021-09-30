# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import logging, os, json
from slack_discovery_sdk import DiscoveryClient
from utils import is_credit_card_number

logging.basicConfig(level=logging.DEBUG)

enterprise_token = os.environ["SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN"]

client = DiscoveryClient(token=enterprise_token)

# CALL PATTERN - Data Loss Prevention
## Step 1 - Retrieve a list of the most recent conversations in the last 24 hours.
auth_test = client.auth_test()

# change parameters to run the function every 10 seconds (or desired interval)
# using the latest params

last_24_hour_conversations = client.discovery_conversations_recent(
    user=auth_test["user_id"], limit=500
)

## Step 2 - Call conversations_history on each of the previous conversations, to grab the text from each
# conversation from each channel

for conversation in last_24_hour_conversations["channels"]:
    channel_conversation = client.discovery_conversations_history(
        channel=conversation["id"], team=conversation["team"]
    )

    for message in channel_conversation["messages"]:

## Step 3 - check each message and see if it contains a credit card number. If it does, tombstone the message.
## A valid credit card for our logic is something like the following: '5122-2368-7954-3214'
## Please note this is just example logic, to help you understand how to use the Discovery APIs.

        if is_credit_card_number(message["text"]):
            client.discovery_chat_tombstone(
                ts=message["ts"],
                channel=conversation["id"],
            )