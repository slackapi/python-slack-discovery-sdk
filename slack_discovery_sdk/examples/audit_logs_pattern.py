# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import logging, os, json
from slack_discovery_sdk import DiscoveryClient  # type: ignore
import utils

from slack_sdk.audit_logs.v1.client import AuditLogsClient

# Constants for filenames
AUDIT_LOG_ACTIONS_FILENAME = "actions"
AUDIT_LOG_CHANNEL_CREATED_FILENAME = "public_channel_created"

logging.basicConfig(level=logging.DEBUG)

# Initialize the discovery client
# An admin user token with discovery:read, discovery:write
enterprise_token = os.environ["SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN"]
client = DiscoveryClient(token=enterprise_token)

# Get the current user ID via auth_test
auth_test = client.auth_test()

# At this point, you should change the user_id variable to be the user_id of whichever user
# you'd like to see the conversation of. The auth_test is just used for testing purposes here.
user_id = auth_test["user_id"]

# Initialize the audit log client
audit_log_client = AuditLogsClient(
    # A User Token with auditlogs:read scopes, used for audit logs API
    token=os.environ["SLACK_DISCOVERY_SDK_TEST_USER_AUDIT_TOKEN"]
)

# Call audit_logs_actions(), convert it into json, and export json to a file
audit_log_actions = audit_log_client.actions()
audit_log_actions_json = json.dumps(audit_log_actions.body, indent=4)
utils.export_json_to_file(
    audit_log_actions_json,
    AUDIT_LOG_ACTIONS_FILENAME,
    "audit_logs",
    user_id,
)

# Call audit_logs() to look for any public channel created event, and export json to a file
audit_logs = audit_log_client.logs(action="public_channel_created", actor=user_id)
audit_log_channel_created_json = json.dumps(audit_logs.body, indent=4)
utils.export_json_to_file(
    audit_log_channel_created_json,
    AUDIT_LOG_CHANNEL_CREATED_FILENAME,
    "audit_logs",
    user_id,
)
