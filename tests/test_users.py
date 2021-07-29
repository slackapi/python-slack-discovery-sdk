import logging
import os
from slack_discovery_sdk import DiscoveryClient


class TestUsers:
    def setup_method(self):
        logging.basicConfig(level=logging.DEBUG)
        self.token = os.environ["SLACK_ENTERPRISE_TOKEN"]
        self.client = DiscoveryClient(token=self.token)

    def test_pagination(self):
        users = []
        limit_size = 10
        for page in self.client.discovery_users_list(limit=limit_size):
            print(page)
            users = users + page["users"]
        assert len(users) > limit_size
