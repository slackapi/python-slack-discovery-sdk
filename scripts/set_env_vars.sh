# Copyright 2021, Slack Technologies, LLC. All rights reserved.

#!/bin/sh

# check to make sure Python version >= 3.6 is installed
echo "Your current Python version is: "
python3 --version

# setup virtual env
echo "Setting your virtual env."
python3 -m venv .venv
source .venv/bin/activate
echo "Success."

############# Needed to run SDK ####################################
echo "Setting your SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN."

# Set env variables. The enterprise token is needed to use the SDK.
# An admin user token with discovery:read, discovery:write
export SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN='xoxp-**********'
echo "Success."
############# Needed to run SDK ####################################


############# Needed to run examples ####################################
echo "Setting your SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN (this is needed if you want to run the examples)."
# A normal bot token with many scopes
export SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN='xoxb-*******'
echo "Success."

echo "Setting your SLACK_DISCOVERY_SDK_TEST_TEAM_ID (this is needed if you want to run the examples)."
# A test workspace ID in the Enterprise Org
# SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN should have the access to this workspace
export SLACK_DISCOVERY_SDK_TEST_TEAM_ID='T0********'
echo "Success."

echo "Setting your SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID (this is needed if you want to run the examples)."
# A test channel ID in the Enterprise Org
export SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID='C0******'
echo "Success."

echo "Setting your SLACK_DISCOVERY_SDK_TEST_USER_AUDIT_TOKEN (this is needed if you want to run the examples)."
# Used for audit logs API (examples/audit_logs_pattern.py)
# A User Token with auditlogs:read scopes, 
export SLACK_DISCOVERY_SDK_TEST_USER_AUDIT_TOKEN='xoxp-*************'
echo "Success."

############# Needed to run examples ####################################
