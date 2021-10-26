# Copyright 2021, Slack Technologies, LLC. All rights reserved.

#!/bin/sh

# run enterprise info
python3 slack_discovery_sdk/examples/get_enterprise_info.py

# run DLP
python3 slack_discovery_sdk/examples/DLP_call_pattern.py

# run eDiscovery without edits (commented out since we will be running pattern with edits)
# python3 slack_discovery_sdk/examples/user_based_eDiscovery_pattern.py

# run eDiscovery
python3 slack_discovery_sdk/examples/user_based_eDiscovery_with_edits.py

# run auditLogs
python3 slack_discovery_sdk/examples/audit_logs_pattern.py