from enum import Enum
from typing import Any, Dict, Optional

from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.user import (
    CurrentSessionsModel,
    DeletedMediaModel,
    MediaListModel,
    PushersModel,
    RoomModel,
)

from .endpoint import Endpoint


class OrderByMedia(Enum):
    """
    Enum for the order by media parameter.
    """

    MEDIA_ID = "media_id"
    UPLOAD_NAME = "upload_name"
    CREATED_TS = "created_ts"
    LAST_ACCESS_TS = "last_access_ts"
    MEDIA_LENGTH = "media_length"
    MEDIA_TYPE = "media_type"
    QUARANTINED_BY = "quarantined_by"
    SAFE_FROM_QUARANTINE = "safe_from_quarantine"


class User(Endpoint):
    """
    User endpoint
    """

    def __int__(self, user_id: str, **kwargs):
        """
        Initialize User endpoint
        Args:
            user_id: fully-qualified user id: for example, @user:server.com
            **kwargs: keyword arguments to pass to Endpoint

        Returns: None

        """
        self.user_id = user_id
        super().__init__(**kwargs)

    async def query_current_sessions(self) -> CurrentSessionsModel:
        """
        This API returns information about the active sessions for a specific user
        Returns:

        """
        url = self.url(f"whois/{self.user_id}")
        result = await self.request(RequestMethods.GET, url)
        res: CurrentSessionsModel = CurrentSessionsModel.from_dict(result)
        return res

    async def deactivate_account(self) -> Dict[str, bool]:
        """
        This API deactivates an account. It removes active access tokens, resets
        the password, and deletes third-party IDs (to prevent the user requesting
        a password reset).

        It can also mark the user as GDPR-erased. This means messages sent by
        the user will still be visible by anyone that was in the room when these
        messages were sent, but hidden from users joining the room afterwards.

        Returns: {"erase": True}

        """
        url = self.url(f"deactivate/{self.user_id}")
        data: Dict[str, str] = {}
        result = await self.request(RequestMethods.POST, url, json=data)
        return result

    async def reset_password(
        self, new_password: str, logout_devices: bool = True
    ) -> None:
        """
        Changes the password of another user. This will automatically log the
        user out of all their devices
        Args:
            new_password: new user's password
            logout_devices: logout all devices, Default: True

        Returns: None

        """
        url = self.url(f"reset_password/{self.user_id}")
        data = {"new_password": new_password, "logout_devices": logout_devices}
        await self.request(RequestMethods.POST, url, json=data)

    async def is_admin(self) -> bool:
        """
        Get whether a user is a server administrator or not

        Returns: True if user is admin, False otherwise

        """
        url = self.url(f"users/{self.user_id}/admin")
        result = await self.request(RequestMethods.GET, url)
        res: bool = result["admin"]
        return res

    async def set_admin(self, admin: bool) -> None:
        """
        Change whether a user is a server administrator or not
        **NOTE**: you cannot demote yourself

        Args:
            admin: True to make user admin, False to remove admin

        Returns: None

        """
        url = self.url(f"users/{self.user_id}/admin")
        data = {"admin": admin}
        await self.request(RequestMethods.POST, url, data=data)

    async def get_rooms(self) -> RoomModel:
        """
        Gets a list of all room_id that a specific user_id is member.
        Returns: list of rooms

        """
        url = self.url(f"users/{self.user_id}/joined_rooms")
        result = await self.request(RequestMethods.GET, url)
        res: RoomModel = RoomModel.from_dict(result)
        return res

    async def get_data(self) -> Dict[str, Any]:
        """
        Gets information about account data for a specific user_id.

        Returns: See response example here https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#account-data
        """

        url = self.url(f"users/{self.user_id}/accountdata")
        result = await self.request(RequestMethods.GET, url)
        return result

    async def get_media(
        self,
        limit: int = 100,
        from_: int = 0,
        order_by: Optional[OrderByMedia] = None,
        dir_: str = "f",
    ) -> MediaListModel:
        """
        List media uploaded by a user

        Gets a list of all local media that a specific user_id has created.
        These are media that the user has uploaded themselves (local media),
        as well as URL preview images requested by the user if the feature is enabled.

        By default, the response is ordered by descending creation date and
        ascending media ID. The newest media is on top. You can change the order
        with parameters order_by and dir

        Args:
            limit: Is optional but is used for pagination, denoting the maximum
                number of items to return in this call. Defaults to 100
            from_: Is optional but used for pagination, denoting the offset in
                the returned results. This should be treated as an opaque value and
                not explicitly set to anything other than the return value of
                next_token from a previous call. Defaults to 0
            order_by: The method by which to sort the returned list of media.
                If the ordered field has duplicates, the second order
                is always by ascending OrderByMedia.MEDIA_ID, which guarantees a
                stable ordering
            dir_: Direction of media order. Either f for forwards or b for
                backwards. Setting this value to b will reverse the above sort order.
                Defaults to f

        Returns: MediaModel

        """
        url = self.url(f"users/{self.user_id}/media")
        if order_by is None:
            order_by = OrderByMedia.MEDIA_ID
        params = {
            "limit": limit,
            "from": from_,
            "order_by": order_by.value,
            "dir": dir_,
        }
        result = await self.request(RequestMethods.GET, url, params=params)
        res: MediaListModel = MediaListModel.from_dict(result)
        return res

    async def delete_media(self) -> DeletedMediaModel:
        """
        This API deletes the local media from the disk of your own server that
        a specific user_id has created. This includes any local thumbnails.

        This API will not affect media that has been uploaded to external media
        repositories (e.g https://github.com/turt2live/matrix-media-repo/).

        By default, the API deletes media ordered by descending creation date
        and ascending media ID. The newest media is deleted first. You
        can change the order with parameters order_by and dir. If no limit is
        set the API deletes 100 files per request.

        Returns:

        """
        url = self.url(f"users/{self.user_id}/media")
        result = await self.request(RequestMethods.DELETE, url)
        res: DeletedMediaModel = DeletedMediaModel.from_dict(result)
        return res

    async def login_as_user(
        self, valid_until_ms: Optional[int] = None
    ) -> Dict[str, str]:
        """
        Get an access token that can be used to authenticate as that user.

        Useful for when admins wish to do actions on behalf of a user.

        This API does not generate a new device for the user, and so will not appear their /devices list, and in general the target user should not be able to tell they have been logged in as.

        To expire the token call the standard /logout API with the token.

        **Note**: The token will expire if the admin user calls /logout/all from
        any of their devices, but the token will not expire if the target user
        does the same.


        Args:
            valid_until_ms: An optional valid_until_ms field can be specified
                in the request body as an integer timestamp that specifies when the
                token should expire. By default tokens do not expire.

        Returns: {"access_token": "<opaque_access_token_string>"}

        """
        url = self.url(f"users/{self.user_id}/login")
        data = {"valid_until_ms": valid_until_ms}
        result = await self.request(RequestMethods.POST, url, json=data)
        return result

    async def get_all_pushers(self) -> PushersModel:
        """
        Gets information about all pushers for a specific user_id.
        Returns: PushersModel

        """
        url = self.url(f"users/{self.user_id}/pushers")
        result = await self.request(RequestMethods.GET, url)
        res: PushersModel = PushersModel.from_dict(result)
        return res

    async def shadow_bann(self, bann_user: bool) -> None:
        """
        Shadow-banning is a useful tool for moderating malicious or egregiously
        abusive users. A shadow-banned users receives successful responses to
        their client-server API requests, but the events are not propagated
        into rooms. This can be an effective tool as it (hopefully) takes
        longer for the user to realise they are being moderated before pivoting
        to another account.

        Shadow-banning a user should be used as a tool of last resort and may
        lead to confusing or broken behaviour for the client. A shadow-banned
        user will not receive any notification and it is generally more
        appropriate to ban or kick abusive users. A shadow-banned user will be
        unable to contact anyone on the server.

        Args:
            bann_user: True to shadow-ban the user, False to un-shadow-ban the user.

        Returns: None

        """
        url = self.url(f"users/{self.user_id}/shadow_ban")
        if bann_user:
            method = RequestMethods.POST
        else:
            method = RequestMethods.DELETE

        await self.request(method, url)
