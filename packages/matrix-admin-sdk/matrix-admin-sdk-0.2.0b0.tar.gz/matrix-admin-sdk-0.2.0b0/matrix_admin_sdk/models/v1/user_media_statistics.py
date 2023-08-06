from dataclasses import dataclass
from typing import Any, Dict, List

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class UserMediaStatisticsModel(BaseModel):
    """
    User media statistics model.
    Attributes:
        displayname (str): Displayname of this user
        media_count (int): Number of uploaded media by this user
        media_lengt (int): Size of uploaded media in bytes by this user
        user_id (int): Fully-qualified user ID (ex. @user:server.com)
    """

    displayname: str
    media_count: int
    media_length: int
    user_id: int


@dataclass
class UsersMediaStatisticsModel(BaseModel):
    """
    This class is used to store the response of the UsersMediaStatistics endpoint.
    Attributes:
        users (list[UserMediaStatisticsModel]): An array of objects, each containing
            information about the user and their local media
        next_token (int): Opaque value used for pagination.
        total (int): Total number of users after filtering
    """

    users: List[UserMediaStatisticsModel]
    next_token: int
    total: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsersMediaStatisticsModel":
        data = data.copy()
        users = [UserMediaStatisticsModel.from_dict(user) for user in data["users"]]
        del data["users"]
        return cls(users=users, **data)
