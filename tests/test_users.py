import os
from slack_discovery_sdk import DiscoveryClient
from tests.env_variable_names import SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN


class TestUsers:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
        self.client = DiscoveryClient(token=self.token)

    def test_pagination(self):
        users = []
        limit_size = 2
        page_num = 0
        for page in self.client.discovery_users_list(limit=limit_size):
            users = users + page["users"]
            page_num += 1
            if page_num > 5:
                break
        assert len(users) > limit_size

    def test_user_conversations(self):
        auth_test = self.client.auth_test()
        response = self.client.discovery_user_conversations(user=auth_test["user_id"])
        assert response["error"] is None

    def test_user_info(self):
        auth_test = self.client.auth_test()
        response = self.client.discovery_user_info(user=auth_test["user_id"])
        assert response["error"] is None