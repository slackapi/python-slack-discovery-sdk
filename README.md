# discovery-sdk

To get this app to work follow the instructions below:

1. Ensure you have > Python 3.6
2. `pip install -r requirements.txt`
3. export your enterprise token, and userID as follows: (Note you will need to have an org wide level token to be able to access the discovery APIs). 

```
export ENTERPRISE_TOKEN='xoxb-22**************************'
export USER_ID='U028JEZZCKU'
```

4. Run the app: `python3 app.py`

5. You should see a response like the following:

```python
{'ok': True, 'channels': [{'id': 'D028****MK0W', 'team_id': 'E****NMCVTR', 'date_joined': 1626724524, 'date_left': 0, 'is_private': True, 'is_im': True, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'C028BN****D4', 'team_id': 'T028QM7****U', 'date_joined': 1626724525, 'date_left': 0, 'is_private': False, 'is_im': False, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'D0****EKV', 'team_id': 'E0283NMCVTR', 'date_joined': 1626724524, 'date_left': 0, 'is_private': True, 'is_im': True, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'C028R2**TY', 'team_id': 'T02****U', 'date_joined': 1626983537, 'date_left': 0, 'is_private': False, 'is_im': False, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'C0298**TTJ', 'team_id': 'T028QM79BGU', 'date_joined': 1626724525, 'date_left': 0, 'is_private': False, 'is_im': False, 'is_mpim': False, 'is_ext_shared': False}, {'id': 'C029****PEF2', 'team_id': 'T028Q****BGU', 'date_joined': 1626896861, 'date_left': 0, 'is_private': False, 'is_im': False, 'is_mpim': False, 'is_ext_shared': True}]}
```