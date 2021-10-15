# Copyright 2021, Slack Technologies, LLC. All rights reserved.

#!/bin/sh

# check to make sure Python version >= 3.6 is installed
python3 --version

# setup virtual env
python3 -m venv .venv
source .venv/bin/activate

# Upgrade to latest pip verison
pip install -U pip
# install required packages (testing package needed to run examples)
pip install -e ".[testing]"

############# Needed to run Discovery SDK ####################################

# Set env variables. The enterprise token is needed to use the SDK.
# An admin user token with discovery:read, discovery:write
export SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN='xoxp-**********'

############# Needed to run Discovery SDK ####################################


############# Needed to run examples #########################################

# A normal bot token with many scopes
export SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN = "xoxb-*******"

# A test workspace ID in the Enterprise Org
# SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN should have the access to this workspace
export SLACK_DISCOVERY_SDK_TEST_TEAM_ID='T0********'

# A test channel ID in the Enterprise Org
export SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID='C0******'

# Used for audit logs API (examples/audit_logs_pattern.py)
# A User Token with auditlogs:read scopes, 
export SLACK_DISCOVERY_SDK_TEST_USER_AUDIT_TOKEN='xoxp-*************'

############# Needed to run examples #########################################
