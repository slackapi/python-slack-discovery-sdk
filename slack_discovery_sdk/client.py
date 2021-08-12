"""A Python module for interacting with Slack's Discovery APIs."""
from typing import Optional, Union

from .base_client import BaseDiscoveryClient, DiscoveryResponse
from .errors import DiscoveryRequestError


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
        **kwargs,
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
    # discovery.enterprise
    # ------------------------------------------------

    def discovery_enterprise_info(
        self,
        *,
        token: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        include_deleted: Optional[bool] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """This method returns basic information about the Enterprise Grid org
        where the app is installed, including all workspaces (teams).
        The teams array is paged at 1000 items by default, but this can also be shortened with the limit parameter.
        Refer to https://api.slack.com/enterprise/discovery/methods#enterprise_info for more details.
        """
        kwargs.update(
            {
                "token": token,
                "curosr": cursor,
                "limit": limit,
                "include_deleted": include_deleted,
            }
        )
        return self.api_call(
            "discovery.enterprise.info", http_method="GET", params=kwargs
        )

    # ------------------------------------------------
    # discovery.users
    # ------------------------------------------------

    def discovery_users_list(
        self,
        *,
        token: Optional[str] = None,
        limit: Optional[int] = None,
        include_deleted: Optional[bool] = None,
        offset: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """Very similar to regular users.list method. Includes an array of workspace IDs
        that the user belongs to on a Grid org (teams).
        Refer to https://api.slack.com/enterprise/discovery/methods#users_list for more details.
        """
        kwargs.update(
            {
                "token": token,
                "limit": limit,
                "include_deleted": include_deleted,
                "offset": offset,
            }
        )
        return self.api_call("discovery.users.list", http_method="GET", params=kwargs)

    def discovery_user_info(
        self,
        *,
        token: Optional[str] = None,
        user: Optional[str] = None,
        email: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """Get information on a single user in an Enterprise.
        The processes for getting info about internal and external users are slightly different.
        Refer to https://api.slack.com/enterprise/discovery/methods#user_info for more details.
        """
        kwargs.update({"token": token, "user": user, "email": email})
        return self.api_call("discovery.user.info", http_method="GET", params=kwargs)

    def discovery_user_conversations(
        self,
        *,
        token: Optional[str] = None,
        user: str,
        offset: Optional[str] = None,
        include_historical: Optional[bool] = None,
        only_im: Optional[bool] = None,
        only_mpim: Optional[bool] = None,
        only_private: Optional[bool] = None,
        only_public: Optional[bool] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """This method lists IDs for all conversations (channels and DMs, including public, private,
        org-wide, and shared) a user is in.
        Refer to https://api.slack.com/enterprise/discovery/methods#user_conversations for more details.
        """
        kwargs.update(
            {
                "token": token,
                "user": user,
                "include_historical": include_historical,
                "only_im": only_im,
                "only_mpim": only_mpim,
                "only_private": only_private,
                "only_public": only_public,
                "limit": limit,
            }
        )
        if offset != None:
            kwargs.update({"offset": offset})

        return self.api_call(
            "discovery.user.conversations", http_method="GET", params=kwargs
        )

    # ------------------------------------------------
    # discovery.conversations
    # ------------------------------------------------

    def discovery_conversations_recent(
        self,
        *,
        token: Optional[str] = None,
        team: Optional[str] = None,
        latest: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """By default this method will return all updated conversations
        (including org-shared and externally-shared conversations)
        from the entire Grid org for the 24 hours preceding the call.
        You can restrict it to a specific workspace within an org, a smaller timespan,
        or to return data for the last 7 days by using the optional parameters.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_recent for more details.
        """
        kwargs.update({"token": token, "team": team, "latest": latest, "limit": limit})
        return self.api_call(
            "discovery.conversations.recent", http_method="GET", params=kwargs
        )

    def discovery_conversations_list(
        self,
        *,
        token: Optional[str] = None,
        offset: Optional[str] = None,
        team: Optional[str] = None,
        only_public: Optional[bool] = None,
        only_private: Optional[bool] = None,
        only_im: Optional[bool] = None,
        only_mpim: Optional[bool] = None,
        only_ext_shared: Optional[bool] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """This method provides a paginated list of all conversations (channels, private channels/groups, DMs),
        with just a subset of the channel information.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_list for more details.
        """
        kwargs.update(
            {
                "token": token,
                "offset": offset,
                "team": team,
                "only_public": only_public,
                "only_private": only_private,
                "only_im": only_im,
                "only_mpim": only_mpim,
                "only_ext_shared": only_ext_shared,
                "limit": limit,
            }
        )
        return self.api_call(
            "discovery.conversations.list", http_method="GET", params=kwargs
        )

    def discovery_conversations_history(
        self,
        *,
        token: Optional[str] = None,
        channel: Optional[str] = None,
        team: Optional[str] = None,
        latest: Optional[float] = None,
        oldest: Optional[float] = None,
        reactions: Optional[Union[bool, int, str]] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """Retrieves the history of the channel-object.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_history for more details.
        """
        if reactions is not None:
            if isinstance(reactions, (int, str)):
                reactions = int(reactions) == 1
            if not isinstance(reactions, bool):
                raise DiscoveryRequestError(
                    f"Unexpected value type for reactions {type(reactions).__name__}"
                )
        kwargs.update(
            {
                "token": token,
                "channel": channel,
                "team": team,
                "latest": latest,
                "oldest": oldest,
                "reactions": reactions,
                "limit": limit,
            }
        )
        return self.api_call(
            "discovery.conversations.history", http_method="GET", params=kwargs
        )

    def discovery_conversations_edits(
        self,
        *,
        token: Optional[str] = None,
        channel: str,
        team: Optional[str] = None,
        oldest: Optional[float] = None,
        latest: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """This method will only return edit and delete records of messages.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_edits for more details.
        """
        kwargs.update(
            {
                "token": token,
                "channel": channel,
                "team": team,
                "latest": latest,
                "oldest": oldest,
                "limit": limit,
            }
        )
        return self.api_call(
            "discovery.conversations.edits", http_method="GET", params=kwargs
        )

    def discovery_conversations_info(
        self,
        *,
        token: Optional[str] = None,
        channel: str,
        team: Optional[str] = None,
        offset: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """This method provides a comprehensive overview of a single channel outside of its message history.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_info for more details.
        """
        kwargs.update(
            {
                "token": token,
                "channel": channel,
                "team": team,
                "offset": offset,
            }
        )
        return self.api_call(
            "discovery.conversations.info", http_method="GET", params=kwargs
        )

    def discovery_conversations_members(
        self,
        *,
        token: Optional[str] = None,
        channel: str,
        team: Optional[str] = None,
        include_member_left: Optional[bool] = None,
        offset: Optional[str] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """This method provides a list of everyone in a given channel, private channel, MDPM or DM.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_members for more details.
        """
        kwargs.update(
            {
                "token": token,
                "channel": channel,
                "team": team,
                "include_member_left": include_member_left,
                "offset": offset,
                "limit": limit,
            }
        )
        return self.api_call(
            "discovery.conversations.members", http_method="GET", params=kwargs
        )

    def discovery_conversations_renames(
        self,
        *,
        token: Optional[str] = None,
        team: Optional[str] = None,
        latest: Optional[float] = None,
        oldest: Optional[float] = None,
        private: Optional[bool] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """You can use this endpoint to gather all channel renames that have occured for an org,
        without having to call the discovery.conversations.info endpoint for each channel.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_renames for more details.
        """
        kwargs.update(
            {
                "token": token,
                "team": team,
                "latest": latest,
                "oldest": oldest,
                "private": private,
            }
        )
        return self.api_call(
            "discovery.conversations.renames", http_method="GET", params=kwargs
        )

    def discovery_conversations_reactions(
        self,
        *,
        token: Optional[str] = None,
        team: Optional[str] = None,
        channel: str,
        latest: Optional[float] = None,
        oldest: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """Use this method to gather detailed information about current message reactions in a channel.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_reactions for more details.
        """
        kwargs.update(
            {
                "token": token,
                "team": team,
                "channel": channel,
                "latest": latest,
                "oldest": oldest,
                "limit": limit,
            }
        )
        return self.api_call(
            "discovery.conversations.reactions", http_method="GET", params=kwargs
        )

    def discovery_conversations_search(
        self,
        *,
        token: Optional[str] = None,
        team: Optional[str] = None,
        query: str,
        include_messages: Optional[bool] = None,
        limit: Optional[int] = None,
        latest: Optional[float] = None,
        oldest: Optional[float] = None,
        offset: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """The discovery.conversations.search endpoint can be used to find channels and messages within an
        instance that contain the provided search term.
        Refer to https://api.slack.com/enterprise/discovery/methods#conversations_search for more details.
        """
        kwargs.update(
            {
                "token": token,
                "team": team,
                "query": query,
                "include_messages": include_messages,
                "limit": limit,
                "latest": latest,
                "oldest": oldest,
                "offset": offset,
            }
        )
        return self.api_call(
            "discovery.conversations.search", http_method="GET", params=kwargs
        )

    # ------------------------------------------------
    # discovery.chat
    # ------------------------------------------------

    def discovery_chat_info(
        self,
        *,
        token: Optional[str] = None,
        ts: str,
        channel: str,
        team: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """This endpoint returns a single message. If the message has been edited (or deleted),
        this method returns the current, edited (or deleted) message.
        Refer to https://api.slack.com/enterprise/discovery/methods#chat_info for more details.
        """

        kwargs.update(
            {
                "token": token,
                "ts": ts,
                "channel": channel,
                "team": team,
            }
        )
        return self.api_call("discovery.chat.info", http_method="GET", params=kwargs)

    def discovery_chat_update(
        self,
        *,
        token: Optional[str] = None,
        channel: str,
        ts: str,
        text: str,
        team: Optional[str] = None,
        attachments: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """Use this method for quarantine and restoration. This method specifies text or attachments that
        should be included in place of the message.
        Refer to https://api.slack.com/enterprise/discovery/methods#chat_update for more details.
        """

        kwargs.update(
            {
                "token": token,
                "channel": channel,
                "ts": ts,
                "text": text,
                "team": team,
                "attachments": attachments,
            }
        )
        return self.api_call("discovery.chat.update", http_method="POST", params=kwargs)

    def discovery_chat_delete(
        self,
        *,
        token: Optional[str] = None,
        channel: str,
        ts: str,
        team: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """Deletes a message. This method purges the history, edits, and message from the Slack databases.
        Refer to https://api.slack.com/enterprise/discovery/methods#chat_delete for more details.
        """

        kwargs.update(
            {
                "token": token,
                "channel": channel,
                "ts": ts,
                "team": team,
            }
        )
        return self.api_call("discovery.chat.delete", http_method="POST", params=kwargs)

    def discovery_chat_tombstone(
        self,
        *,
        token: Optional[str] = None,
        ts: str,
        channel: str,
        team: Optional[str] = None,
        content: Optional[str] = None,
        **kwargs,
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

    def discovery_chat_restore(
        self,
        *,
        token: Optional[str] = None,
        ts: str,
        channel: str,
        team: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """Use this method to restore a tombstoned message to the client.
        Refer to https://api.slack.com/enterprise/discovery/methods#chat_restore for more details.
        """

        kwargs.update(
            {
                "token": token,
                "ts": ts,
                "channel": channel,
                "team": team,
            }
        )
        return self.api_call(
            "discovery.chat.restore", http_method="POST", params=kwargs
        )

    # ------------------------------------------------
    # discovery.draft
    # ------------------------------------------------

    def discovery_drafts_list(
        self,
        *,
        token: Optional[str] = None,
        team: str,
        offset: Optional[Union[int, float]] = None,
        oldest: Optional[float] = None,
        latest: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """The discovery.drafts.list method returns a list of drafts created upon the specified team.
        Refer to https://api.slack.com/enterprise/discovery/methods#drafts_list for more details.
        """

        kwargs.update(
            {
                "token": token,
                "team": team,
                "offset": offset,
                "oldest": oldest,
                "latest": latest,
                "limit": limit,
            }
        )
        return self.api_call("discovery.drafts.list", http_method="GET", params=kwargs)

    def discovery_draft_info(
        self,
        *,
        token: Optional[str] = None,
        team: str,
        draft: str,
        user: str,
        offset: Optional[int] = None,
        oldest: Optional[float] = None,
        latest: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """The discovery.draft.info endpoint provides information associated with a singular draft.
        Refer to https://api.slack.com/enterprise/discovery/methods#drafts_info for more details.
        """

        kwargs.update(
            {
                "token": token,
                "team": team,
                "draft": draft,
                "user": user,
                "offset": offset,
                "oldest": oldest,
                "latest": latest,
                "limit": limit,
            }
        )
        return self.api_call("discovery.draft.info", http_method="GET", params=kwargs)

    # ------------------------------------------------
    # discovery.file
    # ------------------------------------------------

    def discovery_files_list(
        self,
        *,
        token: Optional[str] = None,
        offset: Optional[int] = None,
        oldest: Optional[float] = None,
        latest: Optional[float] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """This method returns files uploaded within a specified timeframe.
        Refer to https://api.slack.com/enterprise/discovery/methods#files_list for more details.
        """

        kwargs.update(
            {
                "token": token,
                "offset": offset,
                "oldest": oldest,
                "latest": latest,
                "limit": limit,
            }
        )
        return self.api_call("discovery.files.list", http_method="GET", params=kwargs)

    def discovery_file_info(
        self, *, token: Optional[str] = None, file: str, **kwargs
    ) -> DiscoveryResponse:
        """All file comments are shown here. File comments are Slack's odd message type.
        Refer to https://api.slack.com/enterprise/discovery/methods#file_info for more details.
        """

        kwargs.update({"token": token, "file": file})
        return self.api_call("discovery.file.info", http_method="GET", params=kwargs)

    def discovery_file_tombstone(
        self,
        *,
        token: Optional[str] = None,
        file: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        **kwargs,
    ) -> DiscoveryResponse:
        """Tombstone a file, making it inaccessible. Download the file in advance for inspection,
        because it will not be accessible after tombstoning.
        Refer to https://api.slack.com/enterprise/discovery/methods#file_tombstone for more details.
        """

        kwargs.update(
            {"token": token, "file": file, "title": title, "content": content}
        )
        return self.api_call(
            "discovery.file.tombstone", http_method="POST", params=kwargs
        )

    def discovery_file_restore(
        self, *, token: Optional[str] = None, file: str, **kwargs
    ) -> DiscoveryResponse:
        """Restores a tombstoned file, making it accessible again.
        Refer to https://api.slack.com/enterprise/discovery/methods#file_restore for more details.
        """
        kwargs.update(
            {
                "token": token,
                "file": file,
            }
        )
        return self.api_call(
            "discovery.file.restore", http_method="POST", params=kwargs
        )

    def discovery_file_delete(
        self, *, token: Optional[str] = None, file: str, **kwargs
    ) -> DiscoveryResponse:
        """Deletes a file.
        Refer to https://api.slack.com/enterprise/discovery/methods#file_delete for more details.
        """
        kwargs.update(
            {
                "token": token,
                "file": file,
            }
        )
        return self.api_call("discovery.file.delete", http_method="POST", params=kwargs)
