# Copyright 2021, Slack Technologies, LLC. All rights reserved.

import json
import logging
import os
from urllib.parse import parse_qs
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import Dict, Sequence, Union, Optional

from . import DiscoveryClient


class DiscoveryOAuthApp:
    def __init__(
        self,
        port: int = 3000,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        bot_scopes: str = "commands",
        user_scopes: str = "discovery:read,discovery:write",
        install_path: str = "/slack/install",
        redirect_path: str = "/slack/oauth_redirect",
    ):
        self.port: int = port
        self.logger = logging.getLogger(__name__)
        _logger = self.logger
        _client_id = client_id or os.environ["SLACK_CLIENT_ID"]
        _client_secret = client_secret or os.environ["SLACK_CLIENT_SECRET"]
        _bot_scopes = bot_scopes
        _user_scopes = user_scopes
        _install_path = install_path
        _redirect_path = redirect_path
        _client = DiscoveryClient()

        class DiscoveryOAuthAppHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                request_path, _, query = self.path.partition("?")
                if request_path == _install_path:
                    url = (
                        f"https://slack.com/oauth/v2/authorize"
                        f"?client_id={_client_id}"
                        f"&scope={_bot_scopes}"
                        f"&user_scope={_user_scopes}"
                    )
                    self._send_response(302, body="", headers={"Location": [url]})
                elif request_path == _redirect_path:
                    try:
                        oauth_v2_access = _client.oauth_v2_access(
                            client_id=_client_id,
                            client_secret=_client_secret,
                            code=parse_qs(query).get("code", [""])[0],
                        )
                        main = f"""
                        <h2>Here is your Discovery API access token:</h2>
                        <p>{oauth_v2_access.get("authed_user", {}).get("access_token")}</pre>
                        <hr/>
                        <p>Click <a href="{_install_path}">here</a> to install the app again.</p>
                        """  # noqa: E501
                        self._send_response(
                            200,
                            body=self._build_html_page(main),
                            headers={"Content-Type": ["text/html; charset=utf-8"]},
                        )
                    except Exception as _:
                        _logger.exception("Failed to perform oauth.v2.access API call")
                        main = f"""
                        <p>Click <a href="{_install_path}">here</a> to install the app again.</p>
                        """  # noqa: E501
                        self._send_response(
                            200,
                            body=self._build_html_page(main),
                            headers={"Content-Type": ["text/html; charset=utf-8"]},
                        )
                else:
                    self._send_response(404, headers={})

            def _build_html_page(self, main: str) -> str:
                return (
                    "<html>"
                    "<head>"
                    "<style>body {{ padding: 10px 15px; font-family: verdana; text-align: center; }}</style>"
                    "</head>"
                    "<body>"
                    f"{main}"
                    "</body>"
                    "</html>"
                )

            def _send_response(
                self,
                status: int,
                headers: Dict[str, Sequence[str]],
                body: Union[str, dict] = "",
            ):
                self.send_response(status)

                response_body = body if isinstance(body, str) else json.dumps(body)
                body_bytes = response_body.encode("utf-8")

                for k, vs in headers.items():
                    for v in vs:
                        self.send_header(k, v)
                self.send_header("Content-Length", len(body_bytes))
                self.end_headers()
                self.wfile.write(body_bytes)

        self._server = HTTPServer(("0.0.0.0", self.port), DiscoveryOAuthAppHandler)

    def _get_boot_message(self) -> str:
        return (
            "Access https://{your-domain}/slack/install "
            "after setting the Redirect URL to https://{your-domain}/slack/oauth_redirect"
        )

    def start(self) -> None:
        """Starts a new web server process."""
        if self.logger.level > logging.INFO:
            print(self._get_boot_message())
        else:
            self.logger.info(self._get_boot_message())

        try:
            self._server.serve_forever(0.05)
        finally:
            self._server.server_close()
