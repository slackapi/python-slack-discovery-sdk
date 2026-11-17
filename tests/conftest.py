import os

import pytest

from tests.env_variable_names import SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN


def pytest_collection_modifyitems(items):
    if os.environ.get(SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN):
        return
    skip_live = pytest.mark.skip(reason=f"{SLACK_DISCOVERY_SDK_TEST_ENTERPRISE_TOKEN} is not set")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)
