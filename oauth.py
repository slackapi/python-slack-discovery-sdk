# This app serves the following endpoints:
# * GET http://localhost:3000/slack/install
# * GET http://localhost:3000/slack/oauth_redirect

# You can use ngrok or something similar to have public endpoints
# ngrok http 3000 --subdomain my-discovery-app

import logging, os

logging.basicConfig(level=logging.DEBUG)
from slack_discovery_sdk import DiscoveryOAuthApp

app = DiscoveryOAuthApp(
    client_id=os.environ["SLACK_CLIENT_ID"],
    client_secret=os.environ["SLACK_CLIENT_SECRET"],
)
app.start()
