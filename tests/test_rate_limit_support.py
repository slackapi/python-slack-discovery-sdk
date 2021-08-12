import time

from slack_discovery_sdk.rate_limit_support import RateLimiter


class TestRateLimitSupport:
    def setup_method(self):
        pass

    def test_cleanup(self):
        rate_limiter = RateLimiter(enterprise_id="E111")
        now = time.time()
        rate_limiter.org_call_histories_in_last_second = [
            now,
            now - 0.01,
            now - 0.03,
            now - 1.5,
            now - 3,
        ]
        rate_limiter.api_method_call_histories_in_last_minute = {
            "discovery.enterprise.info": [
                now,
                now - 10,
                now - 30,
                now - 100,
                now - 300,
            ]
        }
        rate_limiter.cleanup()

        assert len(rate_limiter.org_call_histories_in_last_second) == 3
        assert (
            len(
                rate_limiter.api_method_call_histories_in_last_minute[
                    "discovery.enterprise.info"
                ]
            )
            == 3
        )
