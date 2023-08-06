from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class UserModel(BaseModel):
    """
    User model
    Attributes:
        name (str): Fully-qualified user ID (ex. @user:server.com).
        is_guest (bool): Status if that user is a guest account.
        admin (bool): Status if that user is an admin account.
        deactivated (bool): Status if that user has been marked as deactivated.
        shadow_banned (bool): Status if that user has been marked as shadow banned.
        displayname (str|None): The user's display name if they have set one.
        creation_ts (int): The user's creation timestamp in ms.
        avatar_url (str|None): he user's avatar URL if they have set one
        user_type (str|None): Type of the user. Normal users are type None.
            This allows user type specific behaviour. There are also types support and bot
    """

    name: str
    is_guest: bool
    admin: bool
    deactivated: bool
    shadow_banned: bool
    creation_ts: int
    displayname: Optional[str]
    avatar_url: Optional[str]
    user_type: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserModel":
        displayname = data.get("displayname")
        avatar_url = data.get("avatar_url")
        user_type = data.get("user_type")
        return cls(
            name=data["name"],
            is_guest=data["is_guest"],
            admin=data["admin"],
            deactivated=data["deactivated"],
            shadow_banned=data["shadow_banned"],
            creation_ts=data["creation_ts"],
            displayname=displayname,
            avatar_url=avatar_url,
            user_type=user_type,
        )


@dataclass
class ThreepidModel(BaseModel):
    medium: str
    address: str
    added_at: int
    validated_at: int


@dataclass
class ExternalId(BaseModel):
    auth_provider: str
    external_id: str


@dataclass
class UserDetailsModel(UserModel):
    threepids: List[ThreepidModel]
    appservice_id: Optional[str]
    consent_server_notice_sent: Optional[str]
    consent_version: Optional[str]
    external_ids: List[ExternalId]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserDetailsModel":
        user_data = asdict(UserModel.from_dict(data))
        user_data["threepids"] = [
            ThreepidModel.from_dict(i) for i in data.get("threepids", [])
        ]
        user_data["external_ids"] = [
            ExternalId.from_dict(i) for i in data.get("external_ids", [])
        ]
        user_data["consent_server_notice_sent"] = data.get(
            "consent_server_notice_sent", None
        )
        user_data["consent_version"] = data.get("consent_version", None)
        user_data["appservice_id"] = data.get("appservice_id", None)
        return cls(**user_data)


@dataclass
class UsersModel(BaseModel):
    """
    List of users
    Attributes:
        users (list[UserModel]): List of users
        total (int): total number of users
        next_token (str|None): next token

    """

    users: List[UserModel]
    total: int
    next_token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        users = [UserModel.from_dict(i) for i in data["users"]]
        return cls(users=users, total=data["total"], next_token=data.get("next_token"))
