"""A Python module for interacting with Slack's Web API."""
from typing import Optional

from .base_client import BaseDiscoveryClient, DiscoveryResponse


class DiscoveryClient(BaseDiscoveryClient):
    """A WebClient allows apps to communicate with the Slack Platform's Discovery APIs.
    https://api.slack.com/enterprise/discovery/methods
    The Slack Web API is an interface for querying information from
    and enacting change in a Slack workspace.
    This client handles constructing and sending HTTP requests to Slack
    as well as parsing any responses received into a `SlackResponse`.
    Attributes:
        token (str): A string specifying an xoxp or xoxb token.
        base_url (str): A string representing the Slack API base URL.
            Default is 'https://www.slack.com/api/'
        timeout (int): The maximum number of seconds the client will wait
            to connect and receive a response from Slack.
            Default is 30 seconds.
    Methods:
        api_call: Constructs a request and executes the API call to Slack.
    Example of recommended usage:
    ```python
        import os
        from slack_sdk import WebClient
        client = WebClient(token=os.environ['SLACK_API_TOKEN'])
        response = client.chat_postMessage(
            channel='#random',
            text="Hello world!")
        assert response["ok"]
        assert response["message"]["text"] == "Hello world!"
    ```
    Example manually creating an API request:
    ```python
        import os
        from slack_sdk import WebClient
        client = WebClient(token=os.environ['SLACK_API_TOKEN'])
        response = client.api_call(
            api_method='chat.postMessage',
            json={'channel': '#random','text': "Hello world!"}
        )
        assert response["ok"]
        assert response["message"]["text"] == "Hello world!"
    ```
    Note:
        Any attributes or methods prefixed with _underscores are
        intended to be "private" internal use only. They may be changed or
        removed at anytime.
    """

    def discovery_conversations_info(
        self, *, token: Optional[str] = None, channel: str, team: str, **kwargs
    ) -> DiscoveryResponse:
        """Retrieve information about a conversation.
        Args:
        channel (str): The channel id. e.g. 'C1234567890'
        """
        kwargs.update({"token": token, "channel": channel, "team": team})
        return self.api_call("discovery.conversations.info", params=kwargs)

    def discovery_enterprise_info(
        self, *, token: Optional[str] = None, **kwargs
    ) -> DiscoveryResponse:
        """This method returns basic information about the Enterprise Grid org where the app is installed,
        including all workspaces (teams). The teams array is paged at 1000 items by default, but this can
        also be shortened with the limit parameter.
        Args:
            token (str): Authentication token bearing Org Owner and Admin scopes
                e.g. 'xoxp-2275769437943-*****64595c4'
        """
        kwargs.update({"token": token})
        return self.api_call("discovery.enterprise.info", params=kwargs)

    def discovery_users_list(
        self, *, token: Optional[str] = None, **kwargs
    ) -> DiscoveryResponse:
        """Very similar to regular users.list method. Includes an array of workspace IDs that the user belongs
        to on a Grid org (teams). Currently this method does not return names of custom profile fields.
        Args:
            token (str): Authentication token bearing Org Owner and Admin scopes
                e.g. 'xoxp-2275769437943-*****64595c4'
        """
        kwargs.update({"token": token})
        return self.api_call("discovery.users.list", params=kwargs)

    def discovery_user_info(
        self, *, token: Optional[str] = None, email: str, **kwargs
    ) -> DiscoveryResponse:
        """Get information on a single user in an Enterprise. The processes for getting info about internal
        and external users are slightly different. For internal users you must user either
        userID or email to search for a particular user.
        Args:
            token (str): Authentication token bearing discovery:read scope
                e.g. 'xoxp-2275769437943-*****64595c4'
        """
        kwargs.update({"token": token, "email": email})
        return self.api_call("discovery.user.info", params=kwargs)

    def discovery_user_conversations(
        self, *, token: Optional[str] = None, user: str, **kwargs
    ) -> DiscoveryResponse:
        """This method lists IDs for all conversations (channels and DMs, including public, private,
            org-wide, and shared) a user is in. With the optional include_historical argument, it will
            also return any conversation this user was in at some point and left.
        Args:
            token (str): xoxp token authorized with discovery:read scope
                e.g. 'xoxp-2275769437943-*****64595c4'
            user (str): Encoded user ID for the user whose channels you want to retrieve
                e.g. 'W0MLS084A'
        """
        kwargs.update({"token": token, "user": user})
        return self.api_call("discovery.user.conversations", params=kwargs)

    def discovery_conversations_recent(
        self, *, token: Optional[str] = None, **kwargs
    ) -> DiscoveryResponse:
        """By default this method will return all updated conversations (including org-shared and
        externally-shared conversations) from the entire Grid org for the 24 hours preceding the call.
        Args:
            token (str): xoxp token authorized with discovery:read scope
                e.g. 'xoxp-2275769437943-*****64595c4'
            team (str): When team is specified, we will return only conversations from that workspace.
                e.g. 'T1234567890'
        """
        kwargs.update({"token": token})
        return self.api_call("discovery.conversations.recent", params=kwargs)
