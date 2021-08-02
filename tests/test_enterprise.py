import os
from slack_discovery_sdk import DiscoveryClient
from tests.env_variable_names import SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN


class TestEnterprise:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]
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
