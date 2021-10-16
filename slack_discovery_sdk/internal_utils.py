# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import platform, string, random, time
import sys
from typing import Dict, Union, Optional, Any
from urllib.parse import urljoin

from .version import __version__  # type:ignore


def convert_bool_to_0_or_1(
    params: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Converts all bool values in dict to "0" or "1".
    Slack APIs safely accept "0"/"1" as boolean values.
    Using True/False (bool in Python) doesn't work with aiohttp.
    This method converts only the bool values in top-level of a given dict.
    Args:
        params: params as a dict
    Returns:
        Modified dict
    """
    if params:
        return {k: _to_0_or_1_if_bool(v) for k, v in params.items()}
    return None


def get_user_agent(prefix: Optional[str] = None, suffix: Optional[str] = None):
    """Construct the user-agent header with the package info,
    Python version and OS version.
    Returns:
        The user agent string.
        e.g. 'Python/3.6.7 slack_discovery_sdk/1.0.0 Darwin/17.7.0'
    """
    # __name__ returns all classes, we only want the client
    client = "{0}/{1}".format("slack_discovery_sdk", __version__)
    python_version = "Python/{v.major}.{v.minor}.{v.micro}".format(v=sys.version_info)
    system_info = "{0}/{1}".format(platform.system(), platform.release())
    user_agent_string = " ".join([python_version, client, system_info])
    prefix = f"{prefix} " if prefix else ""
    suffix = f" {suffix}" if suffix else ""
    return prefix + user_agent_string + suffix


def _get_url(base_url: str, api_method: str) -> str:
    """Joins the base Slack URL and an API method to form an absolute URL.
    Args:
        base_url (str): The base URL
        api_method (str): The Slack Web API method. e.g. 'discovery.chat.delete'
    Returns:
        The absolute API URL.
            e.g. 'https://slack.com/api/discovery.chat.delete'
    """
    return urljoin(base_url, api_method)


def _next_cursor_is_present(data) -> bool:
    """Determine if the response contains 'next_cursor'
    and 'next_cursor' is not empty.
    Returns:
        A boolean value.
    """
    # Only admin.conversations.search returns next_cursor at the top level
    present = ("offset" in data and data["offset"] != "") or (
        "response_metadata" in data
        and "next_cursor" in data["response_metadata"]
        and data["response_metadata"]["next_cursor"] != ""
    )
    return present


def _to_0_or_1_if_bool(v: Any) -> Union[Any, str]:
    if isinstance(v, bool):
        return "1" if v else "0"
    return v


def _build_unexpected_body_error_message(body: str) -> str:
    body_for_logging = "".join(
        [line.strip() for line in body.replace("\r", "\n").split("\n")]
    )
    if len(body_for_logging) > 100:
        body_for_logging = body_for_logging[:100] + "..."
    message = f"Received a response in a non-JSON format: {body_for_logging}"
    return message


def get_random_string(length: int = 10) -> str:
    all_ascii_lowercase_chars = string.ascii_lowercase
    random_string = "".join(
        random.choice(all_ascii_lowercase_chars) for _ in range(length)
    )
    return random_string


def get_timestamp_last_minute() -> int:
    now = time.time()
    seconds_in_one_minute = 60
    one_minute_ago = now - seconds_in_one_minute
    return int(one_minute_ago)
