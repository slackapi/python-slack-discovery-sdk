"""A Python module for interacting with Slack's Discovery APIs."""
from typing import Optional

from .base_client import BaseDiscoveryClient, DiscoveryResponse


class DiscoveryClient(BaseDiscoveryClient):
    """A DiscoveryClient allows apps to communicate with the Slack Platform's Discovery APIs.
    https://api.slack.com/enterprise/discovery/methods
    """

    def auth_test(self, **kwargs) -> DiscoveryResponse:
        """Checks authentication & identity.
        Refer to https://api.slack.com/methods/auth.test for more details.
        """
        return self.api_call("auth.test", http_method="POST", params=kwargs)

    def oauth_v2_access(
        self,
        *,
        client_id: str,
        client_secret: str,
        # This field is required when processing the OAuth redirect URL requests
        # while it's absent for token rotation
        code: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        # This field is required for token rotation
        grant_type: Optional[str] = None,
        # This field is required for token rotation
        refresh_token: Optional[str] = None,
        **kwargs
    ) -> DiscoveryResponse:
        """Exchanges a temporary OAuth verifier code for an access token.
        Refer to https://api.slack.com/methods/oauth.v2.access for more details.
        """
        if redirect_uri is not None:
            kwargs.update({"redirect_uri": redirect_uri})
        if code is not None:
            kwargs.update({"code": code})
        if grant_type is not None:
            kwargs.update({"grant_type": grant_type})
        if refresh_token is not None:
            kwargs.update({"refresh_token": refresh_token})
        return self.api_call(
            "oauth.v2.access",
            http_method="POST",
            params=kwargs,
            auth={"client_id": client_id, "client_secret": client_secret},
        )

    # ------------------------------------------------
    # discovery.chat
    # ------------------------------------------------

    def discovery_chat_tombstone(
        self,
        *,
        token: Optional[str] = None,
        ts: str,
        channel: str,
        team: Optional[str] = None,
        content: str,
        **kwargs
    ) -> DiscoveryResponse:
        """Use this method to update and or obscure a message in the event that the message violated policy.
        Refer to https://api.slack.com/enterprise/discovery/methods#chat_tombstone for more details.
        """
        kwargs.update(
            {
                "token": token,
                "ts": ts,
                "channel": channel,
                "team": team,
                "content": content,
            }
        )
        return self.api_call(
            "discovery.chat.tombstone", http_method="POST", params=kwargs
        )

    # ------------------------------------------------
    # discovery.enterprise
    # ------------------------------------------------

    def discovery_enterprise_info(
        self, *, token: Optional[str] = None, **kwargs
    ) -> DiscoveryResponse:
        """This method returns basic information about the Enterprise Grid org
        where the app is installed, including all workspaces (teams).
        The teams array is paged at 1000 items by default, but this can also be shortened with the limit parameter.
        Refer to https://api.slack.com/enterprise/discovery/methods#enterprise_info for more details.
        """
        kwargs.update({"token": token})
        return self.api_call(
            "discovery.enterprise.info", http_method="GET", params=kwargs
        )

    # ------------------------------------------------
    # discovery.conversations
    # ------------------------------------------------

    def discovery_conversations_info(
        self, *, token: Optional[str] = None, channel: str, team: str, **kwargs
    ) -> DiscoveryResponse:
        """This method provides a comprehensive overview of a single channel outside of its message history.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_info for more details.
        """
        kwargs.update({"token": token, "channel": channel, "team": team})
        return self.api_call(
            "discovery.conversations.info", http_method="GET", params=kwargs
        )

    def discovery_conversations_recent(
        self, *, token: Optional[str] = None, **kwargs
    ) -> DiscoveryResponse:
        """By default this method will return all updated conversations
        (including org-shared and externally-shared conversations)
        from the entire Grid org for the 24 hours preceding the call.
        You can restrict it to a specific workspace within an org, a smaller timespan,
        or to return data for the last 7 days by using the optional parameters.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_recent for more details.
        """
        kwargs.update({"token": token})
        return self.api_call(
            "discovery.conversations.recent", http_method="GET", params=kwargs
        )

    # ------------------------------------------------
    # discovery.users
    # ------------------------------------------------

    def discovery_users_list(
        self, *, token: Optional[str] = None, **kwargs
    ) -> DiscoveryResponse:
        """Very similar to regular users.list method. Includes an array of workspace IDs
        that the user belongs to on a Grid org (teams).
        Refer to https://api.slack.com/enterprise/discovery/methods#users_list for more details.
        """
        kwargs.update({"token": token})
        return self.api_call("discovery.users.list", http_method="GET", params=kwargs)

    def discovery_user_info(
        self, *, token: Optional[str] = None, email: str, **kwargs
    ) -> DiscoveryResponse:
        """Get information on a single user in an Enterprise.
        The processes for getting info about internal and external users are slightly different.
        Refer to https://api.slack.com/enterprise/discovery/methods#user_info for more details.
        """
        kwargs.update({"token": token, "email": email})
        return self.api_call("discovery.user.info", http_method="GET", params=kwargs)

    def discovery_user_conversations(
        self, *, token: Optional[str] = None, user: str, **kwargs
    ) -> DiscoveryResponse:
        """This method lists IDs for all conversations (channels and DMs, including public, private,
        org-wide, and shared) a user is in.
        Refer to https://api.slack.com/enterprise/discovery/methods#user_conversations for more details.
        """
        kwargs.update({"token": token, "user": user})
        return self.api_call(
            "discovery.user.conversations", http_method="GET", params=kwargs
        )
