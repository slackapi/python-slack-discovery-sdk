import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from slack_discovery_sdk import DiscoveryClient
from slack_discovery_sdk.errors import DiscoveryApiError


class MockHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.respond(200, {"ok": True, "user_id": "U123"})

    def do_GET(self):
        self.respond(500, {"ok": False, "error": "fatal_error"})

    def respond(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode("utf-8"))

    def log_message(self, format, *args):
        pass


@pytest.fixture
def client():
    server = HTTPServer(("localhost", 0), MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield DiscoveryClient(
        token="xoxp-test",
        base_url=f"http://localhost:{server.server_port}/api/",
        rate_limit_error_prevention_enabled=False,
    )
    server.shutdown()
    server.server_close()


class TestBaseClient:
    def test_successful_response(self, client):
        response = client.auth_test()
        assert response.status_code == 200
        assert response["user_id"] == "U123"
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    def test_error_response(self, client):
        with pytest.raises(DiscoveryApiError) as e:
            client.discovery_enterprise_info()
        assert e.value.response.status_code == 500
        assert e.value.response["error"] == "fatal_error"
