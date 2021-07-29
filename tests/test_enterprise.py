import logging
import os
from slack_discovery_sdk import DiscoveryClient


class TestEnterprise:
    def setup_method(self):
        logging.basicConfig(level=logging.DEBUG)
        self.token = os.environ["SLACK_ENTERPRISE_TOKEN"]
        self.client = DiscoveryClient(token=self.token)

    def test_enterprise_info(self):
        response = self.client.discovery_enterprise_info()
        assert response.status_code == 200
        assert response.body.get("enterprise").get("id") is not None

    def test_enterprise_info_token_override(self):
        client = DiscoveryClient(token="xoxp-invalid")
        response = client.discovery_enterprise_info(token=self.token)
        assert response.status_code == 200
        assert response.body.get("enterprise").get("id") is not None
