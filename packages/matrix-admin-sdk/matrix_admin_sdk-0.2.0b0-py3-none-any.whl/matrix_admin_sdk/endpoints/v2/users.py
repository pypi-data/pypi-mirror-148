from dataclasses import asdict, dataclass
from enum import Enum
from typing import List, Optional

from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v2.users import UserDetailsModel, UsersModel

from .endpoint import Endpoint


@dataclass
class Threepid:
    medium: str
    address: str


@dataclass
class ExternalId:
    auth_provider: str
    external_id: str


class OrderBy(Enum):
    """
    Enum for order by options
    Attributes:
        NAME (str): Users are ordered alphabetically by name. This is the default.
        IS_GUEST (str): Users are ordered by is_guest status.
        ADMIN (str): Users are ordered by admin status.
        USER_TYPE (str): Users are ordered alphabetically by user_type.
        DEACTIVATED (str): Users are ordered by deactivated status.
        SHADOW_BANNED (str): Users are ordered by shadow_banned status.
        DISPLAYNAME (str): Users are ordered alphabetically by displayname
        AVATAR_URL (str): Users are ordered alphabetically by avatar URL.
        CREATION_TS (str): Users are ordered by when the users was created in ms.
    """

    NAME = "name"
    IS_GUEST = "is_guest"
    ADMIN = "admin"
    USER_TYPE = "user_type"
    DEACTIVATED = "deactivated"
    SHADOW_BANNED = "shadow_banned"
    DISPLAYNAME = "displayname"
    AVATAR_URL = "avatar_url"
    CREATION_TS = "creation_ts"


class Users(Endpoint):
    async def get_all(
        self,
        user_id: Optional[str] = None,
        name: Optional[str] = None,
        guests: bool = True,
        deactivated: bool = False,
        limit: int = 100,
        from_: int = 0,
        order_by: Optional[OrderBy] = None,
        dir_: str = "f",
    ) -> UsersModel:
        order_by = OrderBy.NAME if order_by is None else order_by

        url = self.url("users")
        params = {
            "user_id": user_id,
            "name": name,
            "guests": guests,
            "deactivated": deactivated,
            "limit": limit,
            "from": from_,
            "order_by": order_by.value,
            "dir": dir_,
        }
        result = await self.request(RequestMethods.GET, url, params=params)
        res: UsersModel = UsersModel.from_dict(result)
        return res

    async def query_user_account(self, user_id: str) -> UserDetailsModel:
        """
        This API returns information about a specific user account.
        Args:
            user_id: fully-qualified user id: for example, @user:server.com

        Returns: UserDetailsModel

        """
        url = self.url(f"users/{user_id}")
        result = await self.request(RequestMethods.GET, url)
        res: UserDetailsModel = UserDetailsModel.from_dict(result)
        return res

    async def create_or_modify_account(
        self,
        user_id: str,
        password: Optional[str] = None,
        displayname: Optional[str] = None,
        avatar_url: Optional[str] = None,
        admin: bool = False,
        deactivated: bool = False,
        user_type: Optional[str] = None,
        threepids: Optional[List[Threepid]] = None,
        external_ids: Optional[List[ExternalId]] = None,
    ) -> None:
        """
        This API allows an administrator to create or modify a user account with
        a specific user_id.

        If the user already exists then optional parameters default to the current value.

        In order to re-activate an account deactivated must be set to false. If
        users do not login via single-sign-on, a new password must be provided.

        Args:
            user_id: fully-qualified user id: for example, @user:server.com.
            password:  If provided, the user's password is updated and all
                devices are logged out.
            displayname: defaults to the value of user_id.
            avatar_url: must be a MXC URI
            admin: is user an admin
            deactivated: If unspecified, deactivation state will be left unchanged
                on existing accounts and set to false for new accounts. A user cannot
                be erased by deactivating with this API. For details on deactivating
                users see Deactivate Account.
            user_type: If provided, the user type will be adjusted. If null given,
                the user type will be cleared. Other allowed options are: bot and support
            threepids: allows setting the third-party IDs (email, msisdn)
            external_ids: Allow setting the identifier of the external identity
                provider for SSO (Single sign-on). Details in Sample Configuration
                File section sso and oidc_providers

        Returns: None

        """
        if threepids is None:
            threepids = []
        if external_ids is None:
            external_ids = []
        if displayname is None:
            displayname = user_id

        threepids_list = [asdict(i) for i in threepids]
        external_ids_list = [asdict(i) for i in external_ids]

        data = {
            "displayname": displayname,
            "threepids": threepids_list,
            "external_ids": external_ids_list,
            "avatar_url": avatar_url,
            "admin": admin,
            "deactivated": deactivated,
            "user_type": user_type,
        }
        if password is not None:
            data["password"] = password

        url = self.url(f"users/{user_id}")

        await self.request(RequestMethods.PUT, url, data=data)
