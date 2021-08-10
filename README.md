# Python-slack-discovery-sdk

Welcome! This is the Python-slack-discovery-sdk. 

**Note: You need a token with `discovery:read` and `discovery:write` scopes to use all of the methods in the SDK.** 

To get this app to work follow the instructions below:

1. Ensure you have > Python 3.6

2. Install dependencies and required packages  
```bash
pip install -e .
```
3. Set your enterprise level token, which should have `discovery:read` and `discovery:write` scopes:
```bash
export SLACK_ENTERPRISE_TOKEN='xoxp-2243093387093-2239369144111....' 
```

4. Run the app: 

```python
python3 app.py
```

5. You should see a response like the following:

```python
{'ok': True, 'channels': [{'id': 'D028****MK0W', 'team_id': 'E****NMCVTR', 'date_joined': 1626724524, 'date_left': 0, 'is_private': True, 'is_im': True, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'C028BN****D4', 'team_id': 'T028QM7****U', 'date_joined': 1626724525, 'date_left': 0, 'is_private': False, 'is_im': False, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'D0****EKV', 'team_id': 'E0283NMCVTR', 'date_joined': 1626724524, 'date_left': 0, 'is_private': True, 'is_im': True, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'C028R2**TY', 'team_id': 'T02****U', 'date_joined': 1626983537, 'date_left': 0, 'is_private': False, 'is_im': False, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'C0298**TTJ', 'team_id': 'T028QM79BGU', 'date_joined': 1626724525, 'date_left': 0, 'is_private': False, 'is_im': False, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'C029****PEF2', 'team_id': 'T028Q****BGU', 'date_joined': 1626896861, 'date_left': 0, 'is_private': False, 'is_im': False, 'is_mpim': False, 'is_ext_shared': True}]}
```

## Running tests

```bash
# Setup your virtual environment
python --version  # make sure if you're using Python 3.6+
pyton -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[testing]"

# Set required env variables
# 1. An admin user token with discovery:read, discovery:write
export SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN=xoxp-xxx
# 2. A normal bot token with chat:write, channels:read
export SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN=xoxb-xxxx
# 3. A test workspace ID in the Enterprise Org
#    SLACK_DISCOVERY_SDK_TEST_BOT_TOKEN should have the access to this workspace
export SLACK_DISCOVERY_SDK_TEST_TEAM_ID=T1234567890

pytest tests/

# You can check logs/pytest.log for trouble shooting
```