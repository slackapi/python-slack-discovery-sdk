# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import logging, os, json
from slack_discovery_sdk import DiscoveryClient
from utils import export_json_to_file

from slack_sdk.audit_logs.v1.client import AuditLogsClient

from tests.env_variable_names import (
    SLACK_DISCOVERY_SDK_TEST_USER_TOKEN,
)

logging.basicConfig(level=logging.DEBUG)

AUDIT_LOG_ACTIONS_FILENAME = 'audit_log_actions'
AUDIT_LOG_CHANNEL_CREATED_FILENAME = 'audit_logs_public_channel_created'

enterprise_token = os.environ["SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN"]

client = DiscoveryClient(token=enterprise_token)

auth_test = client.auth_test()

audit_log_client = AuditLogsClient(token=os.environ[SLACK_DISCOVERY_SDK_TEST_USER_TOKEN])

audit_log_actions = audit_log_client.actions()

audit_log_actions_json = json.dumps(audit_log_actions.body, indent=4)
export_json_to_file(audit_log_actions_json, AUDIT_LOG_ACTIONS_FILENAME, 'AUDITLOGCHANNEL', auth_test["user_id"])

audit_logs = audit_log_client.logs(action="public_channel_created", actor=auth_test["user_id"])

audit_log_actions_json = json.dumps(audit_logs.body, indent=4)
export_json_to_file(audit_log_actions_json, AUDIT_LOG_CHANNEL_CREATED_FILENAME, 'AUDITLOGPUBLICCHANNEL', auth_test["user_id"])