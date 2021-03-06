# Copyright 2021, Slack Technologies, LLC. All rights reserved.

"""Internal module for loading proxy-related env variables"""
import logging
import os
from typing import Optional

_default_logger = logging.getLogger(__name__)


def load_http_proxy_from_env(logger: logging.Logger = _default_logger) -> Optional[str]:
    proxy_url = (
        os.environ.get("HTTPS_PROXY")
        or os.environ.get("https_proxy")
        or os.environ.get("HTTP_PROXY")
        or os.environ.get("http_proxy")
    )
    if proxy_url is not None:
        logger.debug(
            f"HTTP proxy URL has been loaded from an env variable: {proxy_url}"
        )
    return proxy_url
