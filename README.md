# Python-Slack-Discovery-SDK

👋🏼 Welcome to the Python-Slack-Discovery-SDK! This project aims to make using the Slack Discovery APIs easier.

> 🚨 Note: This SDK is only accessible to customer developers with access to the Discovery API (Enterprise accounts) or partners who have been onboarded to the Security and Compliance partner program. To learn more about the Discovery APIs, please [visit our help center](https://slack.com/help/articles/360002079527-A-guide-to-Slacks-Discovery-APIs). 🚨

# Using the SDK

First, you must download the SDK. Please go to the [Releases section](https://github.com/slackapi/python-slack-discovery-sdk/releases). Go ahead and find the latest stable release, and click on the Assets tab to unfurl the assets. Go ahead and download the Source code (either in tar.gz or zip). Go to your Downloads folder, and unzip the source code. Next, open the source code in an editor of your choice, and proceed to the following steps to install the required dependencies.

# 👨🏻‍💻 Understanding the Setup Script 👩🏻‍💻

In order to speed up the development process, we've provided you with a script called 
`set_env_vars.sh` in the scripts folder to automate a few things needed to run the SDK. 
The script accomplishes the following things using the following code:
* Prints your current Python version (**you will need Python version 3.6 or greater for this SDK**) 
  ```bash
  python3 --version
  ```
* Sets your Virtual Environment
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
* Ensures pip is updated to the latest version
  ```bash
  pip install -U pip
  ```
* Installs required packages and dependencies
  ```bash
  pip install -e ".[testing]"
  ```

## 👨🏻‍💻 Adding Env Variables to Setup Script 👩🏻‍💻

🚨 At this point, you'll need to edit the `scripts/set_env_vars.sh` script in an editor of your choice 🚨

Edit the line below, and add in your token with `discovery:read` and `discovery:write` scopes.
```bash
export SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN='xoxp-**********'
```

Now, if you want to run the examples in the `slack_discovery_sdk/examples` directory, you'll need to set 
a few other additional environmental variables.  

Edit the lines below, and add in the appropriate tokens:

```bash
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
```

🚨 Once you are done adding in your tokens, save the file 🚨

> Note: before you can run this script, you will need to mark the file as executable with the following command:
```bash
chmod +x scripts/set_env_vars.sh
```

## 👩🏻‍💻 Run the Setup Script 👨🏻‍💻
Use the following command to run the script:

> Note: you must use the `source` command so that the env variables are set properly.

```bash
source ./scripts/set_env_vars.sh
```

If all went well, you should see the following output:
```bash
Your current Python version is: 
Python 3.10.0
Setting your virtual env.
Success.
Setting your SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN.
Success.
Setting your SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN (this is needed if you want to run the examples).
Success.
Setting your SLACK_DISCOVERY_SDK_TEST_TEAM_ID (this is needed if you want to run the examples).
Success.
Setting your SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID (this is needed if you want to run the examples).
Success.
Setting your SLACK_DISCOVERY_SDK_TEST_USER_AUDIT_TOKEN (this is needed if you want to run the examples).
Success.
```

## Running the Examples
Use the following command to run a script which calls the `discovery.enterprise.info` endpoint. This endpoint returns basic information about the Enterprise Grid org where the app is installed, including all workspaces (teams). 

```python
python3 slack_discovery_sdk/examples/get_enterprise_info.py
```

You should see a response similar to the following (note the result below has been truncated for readability):

```python
DEBUG:slack_discovery_sdk.base_client:Rate limit metrics: DEBUG:slack_discovery_sdk.base_client:Received the following response - status: 200, headers: {'date': 'Wed, 13 Oct 2021 22:09:57 GMT',..., body: {"ok":true,"enterprise":{"id":"T027****D2R","name":"Enterprise-****-Sandbox","domain":"test-****","email_domain":"","icon":...,"image_default":true},"is_verified":false,"teams":[{"id":"****","name":"Enterprise-****-Sandbox","domain":"test-****","email_domain":"","icon":{"image_102":"https:\/\/a...avatars-teams\/ava_0021-88.png","image_default":true},"is_verified":false,"enterprise_id":"E**","is_enterprise":0,"created":1625594757,"archived":false,"deleted":false,"discoverable":"unlisted"}]}}
```

If you want to run all of the examples at once, you can use the `run_all.sh` script.

> Note: before you can run this script, you will need to mark the file as executable with the following command:

```bash
chmod +x scripts/run_all.sh
```

Then, run the script:

```bash
./scripts/run_all.sh
```

This will run all of the examples in the `slack_discovery_sdk/examples` folder, and 
you should see debug output in your terminal once the script has finished running.

Continue reading below to learn what each example does:

💳 **`DLP_call_pattern.py`** 💳
* This script involves using the tombstoning capabilities of the Discovery SDK to check for messages that contain sensitive information. If sensitive information is detected by our script (for example a credit card number), the message is tombstoned, and the user is notified that their message is being reviewed.
* Once you run this script, you should see that one of your 
messages in the channel which you set in your env variable (SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID) should have been tombstoned. The message should now say `This message is being scanned to make sure it complies with your team’s data security policies.`

🙋🏾‍♀️ **`user_based_eDiscovery_with_edits.py`** 👩🏻‍🏫
* This script retrieves all of the conversations (channels) and messages a particular user is in. It then outputs those 
conversations to a file, and stores them in the following format: `YYYY/MM/DD/user_id/channel_id/discovery_conversations.json`. If the `has_edits` flag is true 
for a certain conversation, all edited messages will be found in the `edits` field.

👩🏻‍🏫 **`audit_logs_pattern.py`** 👩🏻‍🏫
* This script will use the [Audit Logs API](https://api.slack.com/admins/audit-logs) to find all of the
channels that a particular user has created. As is the 
case with the `user_based_eDiscovery` script, it will only
be useful if you have a paricular user which you want to see details about. This script will output the channel creation events associated with a particular user_id to in the following format: `YYYY/MM/DD/user_id/audit_logs/public_channel_created.json`.

🙋🏾‍♀️ **`user_based_eDiscovery_pattern.py`** 👩🏻‍🏫
* This is the same as the `user_based_eDiscovery_with_edits.py` script, except it 
doesn't capture edits. 

## Considerations
The SDK and examples are to aid in your development process. Please feel free to use this as a learning exercise, and to build on top of these examples, but the examples shown above are by no means a complete solution. 

## Running tests

To run the unit tests in this repository, creating a Discovery API enabled app is required.

```yaml
_metadata:
  major_version: 1
  minor_version: 1
display_information:
  name: discovery-api-test
features:
  bot_user:
    display_name: discovery-api-test
oauth_config:
  redirect_urls:
    - https://your-own-domain.ngrok.io/slack/oauth_redirect
  scopes:
    user:
      - discovery:read
      - discovery:write
    bot:
      - channels:manage
      - channels:read
      - chat:write
      - commands
      - groups:write
      - im:write
      - mpim:write
      - reactions:write
      - channels:join
      - files:write
settings:
  org_deploy_enabled: true
  socket_mode_enabled: false
  token_rotation_enabled: false
```

And then, setting the bot / user tokens in the env variables as below:

```bash
# Setup your virtual environment
python --version  # make sure if you're using Python 3.6+
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[testing]"

# Set required env variables
# 1. An admin user token with discovery:read, discovery:write
export SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN=xoxp-xxx
# 2. A normal bot token with many scopes
export SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN=xoxb-xxxx
# 3. A test workspace ID in the Enterprise Org
#    SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN should have the access to this workspace
export SLACK_DISCOVERY_SDK_TEST_TEAM_ID=T1234567890
# 4. A test channel ID in the Enterprise Org
#    SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN should have the access to this channel
export SLACK_DISCOVERY_SDK_TEST_CHANNEL_ID=C1234567890
pytest tests/

# You can check logs/pytest.log for trouble shooting
```

## Feedback

For feedback, please use [this feedback form](https://forms.gle/B2PRF9HQheRgQdo7A). 

## Issues and Troubleshooting
For issues, please use [this issue form](https://forms.gle/jHS17eYEYAtcXA96A).
