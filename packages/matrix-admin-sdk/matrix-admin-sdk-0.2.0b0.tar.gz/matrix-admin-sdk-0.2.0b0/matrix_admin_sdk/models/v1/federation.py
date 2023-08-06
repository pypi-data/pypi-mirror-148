from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class DestinationModel(BaseModel):
    """
    Class representing a destination model.
    Attributes:
        destination (str): Name of the remote server to federate
        retry_last_ts (int): The last time Synapse tried and failed to reach the
            remote server, in ms. This is 0 if the last attempt to communicate
            with the remote server was successful
        retry_interval (int): How long since the last time Synapse tried to reach
            the remote server before trying again, in ms. This is 0
            if no further retrying occuring
        failure_ts: (int|None): The first time Synapse tried and failed to reach
            the remote server, in ms. This is null if communication with the
            remote server has never failed.
        last_successful_stream_ordering: (int|None): The stream ordering of the
            most recent successfully-sent PDU to this destination, or null if this
            information has not been tracked yet.
    """

    destination: str
    retry_last_ts: int
    retry_interval: int
    failure_ts: Optional[int] = None
    last_successful_stream_ordering: Optional[int] = None


@dataclass
class DestinationsModel(BaseModel):
    """
    A list of destinations.
    Attributes:
        destinations (list[DestinationModel]): An array of objects, each containing
            information about a destination
        total (int): Total number of destinations
        next_token (int|None): Indication for pagination
    """

    destinations: List[DestinationModel]
    total: int
    next_token: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DestinationsModel":
        destinations = [DestinationModel.from_dict(d) for d in data["destinations"]]
        return cls(
            destinations=destinations,
            total=data["total"],
            next_token=data.get("next_token"),
        )


@dataclass
class DestinationRoomModel(BaseModel):
    """
    Class representing a destination room model.
    Attributes:
        room_id (str): The ID of the room
        stream_ordering (int): The stream ordering of the most recent
            successfully-sent PDU to this destination in this room
    """

    room_id: str
    stream_ordering: int


@dataclass
class DestinationRoomsModel(BaseModel):
    """
    A list of rooms in a destination.
    Attributes:
        rooms (list[DestinationRoomModel]): An array of objects, each containing
            information about a room
        total (int): Total number of destinations
        next_token (int|None): Indication for pagination
    """

    rooms: List[DestinationRoomModel]
    total: int
    next_token: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DestinationRoomsModel":
        rooms = [DestinationRoomModel.from_dict(d) for d in data["rooms"]]
        return cls(
            rooms=rooms,
            total=data["total"],
            next_token=data.get("next_token"),
        )
