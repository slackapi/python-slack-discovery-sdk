# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import random
import time
from threading import Lock
from typing import List, Dict, Optional


class RateLimiter:
    # Requests are rate-limited across the org at around 30 requests per second
    # and each individual method is also limited to 1200 requests per minute.
    # That is, all tokens accessing Discovery API on a given org contribute toward this rate limit.
    # If there are two different tokens for a single team,
    # whether from a single app or two separate apps,
    # they must share the available 30 requests per second.

    MAX_REQUESTS_PER_SECOND_IN_ORG = 30
    MAX_REQUESTS_PER_MINUTE_FOR_API_METHOD = 1200
    DEFAULT_MAX_REQUESTS_PER_MINUTE_FOR_EACH_API_METHOD = {
        "discovery.conversations.search": 6  # as of 2021-08
    }

    enterprise_id: Optional[str]
    # list of timestamps
    org_call_histories_in_last_second: List[float]
    # key: method name (discovery.enterprise.info) to list of timestamps
    api_method_call_histories_in_last_minute: Dict[str, List[float]]
    # key: method name (discovery.enterprise.info) to count
    api_method_successful_call_counts: Dict[str, int]
    api_method_failed_call_counts: Dict[str, int]
    max_requests_per_minute_for_each_api_method: Dict[str, int]
    lock: Lock

    def __init__(
        self,
        *,
        enterprise_id: Optional[str] = None,
        max_requests_per_minute_for_each_api_method: Optional[Dict[str, int]] = None,
    ):
        self.enterprise_id = enterprise_id
        self.org_call_histories_in_last_second = []
        self.api_method_call_histories_in_last_minute = {}
        self.api_method_successful_call_counts = {}
        self.api_method_failed_call_counts = {}
        self.max_requests_per_minute_for_each_api_method = (
            max_requests_per_minute_for_each_api_method
            if max_requests_per_minute_for_each_api_method is not None
            else self.DEFAULT_MAX_REQUESTS_PER_MINUTE_FOR_EACH_API_METHOD
        )
        self.lock = Lock()

    def cleanup(self):
        with self.lock:
            org_call_histories = []
            one_second_ago = time.time() - 1
            for timestamp in self.org_call_histories_in_last_second:
                if timestamp > one_second_ago:
                    org_call_histories.append(timestamp)
            self.org_call_histories_in_last_second = org_call_histories

            one_minute_ago = time.time() - 60
            for (
                endpoint,
                histories,
            ) in self.api_method_call_histories_in_last_minute.items():
                new_histories = []
                for timestamp in histories:
                    if timestamp > one_minute_ago:
                        new_histories.append(timestamp)
                self.api_method_call_histories_in_last_minute[endpoint] = new_histories

    def append_api_call_timestamp(self, api_method: str):
        with self.lock:
            now = time.time()
            self.org_call_histories_in_last_second.append(now)
            api_method_histories = self.api_method_call_histories_in_last_minute.get(
                api_method, []
            )
            api_method_histories.append(now)
            self.api_method_call_histories_in_last_minute[
                api_method
            ] = api_method_histories

    def append_api_call_result(self, api_method: str, is_success: bool):
        with self.lock:
            if is_success is True:
                new_count = (
                    self.api_method_successful_call_counts.get(api_method, 0) + 1
                )
                self.api_method_successful_call_counts[api_method] = new_count
            else:
                new_count = self.api_method_failed_call_counts.get(api_method, 0) + 1
                self.api_method_failed_call_counts[api_method] = new_count

    def calculate_sleep_duration(self, api_method: str) -> float:
        self.cleanup()
        sleep_seconds = 0
        last_second_org_call_count = len(self.org_call_histories_in_last_second)
        if last_second_org_call_count >= 10:
            sleep_seconds = 0.02 + calculate_random_jitter(0.02)  # 1/20 - 1/30
        elif last_second_org_call_count >= 20:
            sleep_seconds = 0.05 + calculate_random_jitter(0.05)  # 1/10 - 1/20
        elif last_second_org_call_count >= 25:
            sleep_seconds = 0.1 + calculate_random_jitter(0.1)  # 1/5 - 1/10
        elif last_second_org_call_count >= 30:
            sleep_seconds = 0.5 + calculate_random_jitter(0.5)

        last_minutes_api_method_requests = (
            self.api_method_call_histories_in_last_minute.get(api_method, [])
        )
        last_minute_api_method_call_count = len(last_minutes_api_method_requests)
        max_requests_for_api_method = (
            self.max_requests_per_minute_for_each_api_method.get(
                api_method, self.MAX_REQUESTS_PER_MINUTE_FOR_API_METHOD
            )
        )
        denominator = max_requests_for_api_method / 15  # this value is usually 80
        if last_minute_api_method_call_count >= max_requests_for_api_method * 0.9:
            # Too fast paced:
            # Change the pace from 60 seconds to 120 seconds
            sleep_seconds = 120 / denominator
        elif last_minute_api_method_call_count >= max_requests_for_api_method * 0.6:
            # Optimal:
            sleep_seconds = 60 / denominator
        elif last_minute_api_method_call_count >= max_requests_for_api_method * 0.3:
            # Somewhat busy:
            # Change the pace from 60 seconds to 30 seconds
            sleep_seconds = 30 / denominator

        if (
            max_requests_for_api_method >= 120
            and last_minute_api_method_call_count >= max_requests_for_api_method / 120
        ):
            # Burst traffic:
            # Change the pace from 60 seconds to 180 seconds
            three_seconds_ago = time.time() - 3
            requests_in_last_three_seconds = [
                timestamp
                for timestamp in last_minutes_api_method_requests
                if timestamp >= three_seconds_ago
            ]
            if len(requests_in_last_three_seconds) >= max_requests_for_api_method / 120:
                sleep_seconds = 180 / denominator

        if sleep_seconds == 0:
            return 0

        return sleep_seconds + calculate_random_jitter(factor=0.05)

    def generate_metrics_report(self) -> Dict[str, str]:
        return {
            "last_second_requests": len(self.org_call_histories_in_last_second),
            "last_minute_requests_per_api_method": {
                k: len(v)
                for k, v in self.api_method_call_histories_in_last_minute.items()
            },
            "successful_call_counts": self.api_method_successful_call_counts,
            "failed_call_counts": self.api_method_failed_call_counts,
        }


def calculate_random_jitter(factor: float = 1.0) -> float:
    return random.random() * factor
