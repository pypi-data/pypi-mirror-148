from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class ConnectionModel(BaseModel):
    ip: str
    last_seen: int
    user_agent: str


@dataclass
class CurrentSessionsModel(BaseModel):
    user_id: str
    devices: Dict[str, List[ConnectionModel]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CurrentSessionsModel":
        devices = {}
        for k, v in data["devices"].items():
            for session in v["sessions"]:
                devices[k] = [ConnectionModel(**i) for i in session["connections"]]
        return cls(
            user_id=data["user_id"],
            devices=devices,
        )


@dataclass
class RoomModel(BaseModel):
    """
    Room model
    Attributes:
        joined_rooms (list[str]): An array of room_id
        total (int): Number of rooms
    """

    joined_rooms: List[str]
    total: int


@dataclass
class MediaModel(BaseModel):
    created_ts: int
    media_id: str
    media_length: int
    media_type: str
    safe_from_quarantine: bool
    upload_name: str
    last_access_ts: Optional[int] = None
    quarantined_by: Optional[str] = None


@dataclass
class MediaListModel(BaseModel):
    media: List[MediaModel]
    next_token: Optional[int]
    total: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MediaListModel":
        media = [MediaModel.from_dict(i) for i in data["media"]]
        return cls(
            media=media,
            next_token=data.get("next_token"),
            total=data["total"],
        )


@dataclass
class DeletedMediaModel(BaseModel):
    """
    Deleted media model
    Attributes:
        deleted_media (list[str]): List of deleted media_id
        total (int): Total number of deleted media
    """

    deleted_media: List[str]
    total: int


@dataclass
class PusherDataModel(BaseModel):
    """
    Pusher data model
    Attributes:
        url (str): Required if kind is http. The URL to use to send notifications to
        format (str): The format to use when sending notifications to the Push Gateway.
    """

    url: str
    format: Optional[str] = None


@dataclass
class PusherModel(BaseModel):
    """
    Pusher model
    Attributes:
        app_display_name (str): A string that will allow the user to identify what
            application owns this pusher.
        app_id (str): This is a reverse-DNS style identifier for the application.
            Max length, 64 chars.
        data (PusherDataModel): information for the pusher implementation itself
        device_display_name (str): A string that will allow the user to identify
            what device owns this pusher.
        profile_tag (str): This string determines which set of device specific
            rules this pusher executes.
        kind (str): The kind of pusher. "http" is a pusher that sends HTTP pokes.
        lang (str): The preferred language for receiving notifications
            (e.g. 'en' or 'en-US')
        pushkey (str): This is a unique identifier for this pusher. Max length,
            512 bytes.

    """

    app_display_name: str
    app_id: str
    data: PusherDataModel
    device_display_name: str
    profile_tag: str
    kind: str
    lang: str
    pushkey: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PusherModel":
        data = data.copy()
        data_field = PusherDataModel.from_dict(data.pop("data"))
        return cls(data=data_field, **data)


@dataclass
class PushersModel(BaseModel):
    """
    Pushers model
    Attributes:
        pushers (list[PusherModel]): An array containing the current pushers for
            the user
        total (int): Total number of pushers

    """

    pushers: List[PusherModel]
    total: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PushersModel":
        pushers = [PusherModel.from_dict(i) for i in data["pushers"]]
        return cls(
            pushers=pushers,
            total=data["total"],
        )
