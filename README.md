# discovery-sdk

To get this app to work follow the instructions below:

1. Ensure you have > Python 3.6
2. `pip install -r requirements.txt`
3. export your bot token, channel ID, and team ID as follows

```
export SLACK_BOT_TOKEN='xoxb-22**************************'
export CHANNEL_ID='C027EHGFC'
export TEAM_ID='T02112BBD2R'
```

4. Run the app: `python3 app.py`

5. You should see a response like the following:

```json
{'ok': True, 'channel': {'id': 'C027EHGFC', 'name': 'random', 'is_channel': True, 'is_group': False, 'is_im': False, 'created': 1625594757, 'is_archived': False, 'is_general': False, 'unlinked': 0, 'name_normalized': 'random', 'is_shared': False, 'parent_conversation': None, 'creator': '********', 'is_ext_shared': False, 'is_org_shared': False, 'shared_team_ids': ['T234*311'], 'pending_shared': [], 'pending_connected_team_ids': [], 'is_pending_ext_shared': False, 'is_member': False, 'is_private': False, 'is_mpim': False, 'topic': {'value': '', 'creator': '', 'last_set': 0}, 'purpose': {'value': 'This channel is for... well, everything else. It’s a place for team jokes, spur-of-the-moment ideas, and funny GIFs. Go wild!', 'creator': '******', 'last_set': 1625594757}, 'previous_names': []}}
```