from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class RoomModel(BaseModel):
    """
    Room model
    Attributes:
        room_id (str): The ID of the room.
        name (str): - The name of the room.
        canonical_alias (str): The canonical (main) alias address of the room.
        joined_members (int): How many users are currently in the room.
        joined_local_members (int): How many local users are currently in the room.
        version (str): The version of the room as a string.
        creator (str): The user_id of the room creator.
        encryption (str|None): Algorithm of end-to-end encryption of messages. Is null if encryption is not active.
        federatable (bool): Whether users on other servers can join this room.
        public (bool): Whether the room is visible in room directory.
        join_rules (str): The type of rules used for users wishing to join this room. One of: ["public", "knock", "invite", "private"].
        guest_access (str|None):  Whether guests can join the room. One of: ["can_join", "forbidden"].
        history_visibility (str): Who can see the room history. One of: ["invited", "joined", "shared", "world_readable"].
        state_events (int): Total number of state_events of a room. Complexity of the room.
    """

    room_id: str
    name: str
    canonical_alias: str
    joined_members: int
    joined_local_members: int
    version: str
    creator: str
    encryption: Optional[str]
    federatable: bool
    public: bool
    join_rules: str
    guest_access: Optional[str]
    history_visibility: str
    state_events: int


@dataclass
class RoomsModel(BaseModel):
    """
    Rooms model
    Attributes:
        rooms (list[Room]): An array of objects, each containing information about a room
        offset (int): The offset of the first room in the list.
        total_rooms (int): The total number of rooms.
        next_batch (str|None): The token to get the next batch of rooms.
        prev_batch (str|None): The token to get the previous batch of rooms.
    """

    rooms: List[RoomModel]
    offset: int
    total_rooms: int
    next_batch: Optional[str] = None
    prev_batch: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoomsModel":
        data = data.copy()
        rooms: List[RoomModel] = [RoomModel.from_dict(room) for room in data["rooms"]]
        del data["rooms"]
        return cls(**data, rooms=rooms)


@dataclass
class RoomMembersModel(BaseModel):
    members: List[str]
    total: int


@dataclass
class RoomStateModel(BaseModel):
    """
    Room state model
    Attributes
        type (str):
        state_key (str):
        etc (bool):
    """

    type: str
    state_key: str
    etc: bool


@dataclass
class BlockStatusModel(BaseModel):
    """
    Block status model
    Attributes:
        block (bool): A boolean. True if the room is blocked, otherwise False
        user_id (str): An optional string. If the room is blocked (block is True)
            shows the user who has add the room to blocking list. Otherwise it is
            not displayed.
    """

    block: bool
    user_id: Optional[str] = None


@dataclass
class DeletedRoomModel(BaseModel):
    kicked_users: List[str]
    failed_to_kick_users: List[str]
    local_aliases: List[str]
    new_room_id: str
