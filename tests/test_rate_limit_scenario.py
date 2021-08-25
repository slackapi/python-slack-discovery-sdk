# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import os
import pytest

from slack_discovery_sdk import DiscoveryClient
from tests.env_variable_names import SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN
from concurrent.futures.thread import ThreadPoolExecutor


class TestEnterprise:
    def setup_method(self):
        self.token = os.environ[SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN]

    @pytest.mark.skip
    def test_discovery_users(self):
        executor = ThreadPoolExecutor(max_workers=100)
        client = DiscoveryClient(
            token=self.token, rate_limit_error_prevention_enabled=True
        )

        def run():
            for i in range(10):
                for page in client.discovery_users_list(limit=1):
                    assert page.status_code == 200
                    for user in page.get("users"):
                        response = client.discovery_user_info(user=user.get("id"))
                        assert response.status_code == 200

        try:
            for i in range(100):
                executor.submit(run)
        finally:
            executor.shutdown()

    @pytest.mark.skip
    def test_discovery_conversations_search(self):
        # Very strict rate limit
        client = DiscoveryClient(
            token=self.token, rate_limit_error_prevention_enabled=True
        )
        for i in range(10):
            for search_result in client.discovery_conversations_search(
                query=str(i),
                limit=1,
            ):
                assert search_result.status_code == 200

    @pytest.mark.skip
    def test_discovery_conversations_list(self):
        executor = ThreadPoolExecutor(max_workers=100)
        client = DiscoveryClient(
            token=self.token, rate_limit_error_prevention_enabled=True
        )

        def run():
            for i in range(10):
                for page in client.discovery_conversations_list(limit=10):
                    assert page.status_code == 200
                    for channel in page.get("channels"):
                        response = client.discovery_conversations_info(
                            channel=channel.get("id")
                        )
                        assert response.status_code == 200

        try:
            for i in range(100):
                executor.submit(run)
        finally:
            executor.shutdown()

    @pytest.mark.skip
    def test_discovery_conversations_history(self):
        executor = ThreadPoolExecutor(max_workers=20)
        client = DiscoveryClient(
            token=self.token, rate_limit_error_prevention_enabled=True
        )

        def run():
            for i in range(10):
                for page in client.discovery_conversations_list(limit=1):
                    assert page.status_code == 200
                    for channel in page.get("channels"):
                        for history in client.discovery_conversations_history(
                            channel=channel.get("id"),
                            limit=1,
                        ):
                            assert history.status_code == 200

        try:
            for i in range(20):
                executor.submit(run)
        finally:
            executor.shutdown()
