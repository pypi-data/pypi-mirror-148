from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class EventReport(BaseModel):
    """
    Event report model.
    Attributes:
        event_id (str): The ID of the reported event
        id (int): ID of event report
        reason (str|None): Comment made by the user_id in this report
        score (int|None): Content is reported based upon a negative score, where -100 is "most offensive" and 0 is "inoffensive"
        received_ts (int): The timestamp (in milliseconds since the unix epoch) when this report was sent
        canonical_alias (str): The canonical alias of the room. null if the room does not have a canonical alias set.
        room_id (str): The ID of the room in which the event being reported is located
        name (str): The name of the room
        sender (str): This is the ID of the user who sent the original message/event that was reported.
        user_id (str): This is the user who reported the event and wrote the reason
    """

    event_id: str
    id: int
    reason: Optional[str]
    score: Optional[int]
    received_ts: int
    canonical_alias: str
    room_id: str
    name: str
    sender: str
    user_id: str


@dataclass
class EventReports(BaseModel):
    """
    List of Event Reports
    Attributes:
        event_reports (List[EventReport]): List of Event Reports
        next_token (int): Indication for pagination
        total (int): Total number of event reports related to the query
    """

    event_reports: List[EventReport]
    next_token: int
    total: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventReports":
        return cls(
            next_token=data["next_token"],
            total=data["total"],
            event_reports=[EventReport.from_dict(i) for i in data["event_reports"]],
        )


@dataclass
class EventContent(BaseModel):
    body: str
    format: str
    formatted_body: str
    msgtype: str


Signatures = Dict[str, Dict[str, str]]


@dataclass
class EventJson(BaseModel):
    auth_events: List[str]
    content: EventContent
    depth: int
    hashes: Dict[str, str]
    origin: str
    origin_server_ts: int
    prev_events: List[str]
    prev_state: List[str]
    room_id: str
    sender: str
    signatures: Signatures
    type: str
    unsigned: Dict[str, int]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventJson":
        data = data.copy()
        content = EventContent.from_dict(data["content"])
        del data["content"]
        return cls(**data, content=content)


@dataclass
class EventDetails:
    """
    Event details model.
    Attributes:
       id (int): ID of event report.
       received_ts (int): The timestamp (in milliseconds since the unix epoch) when this report was sent.
       room_id (str): The ID of the room in which the event being reported is located.
       name (str): The name of the room.
       event_id (str): The ID of the reported event.
       user_id (str): This is the user who reported the event and wrote the reason.
       reason (str): Comment made by the user_id in this report. May be blank.
       score (int): Content is reported based upon a negative score, where -100 is "most offensive" and 0 is "inoffensive".
       sender (str): This is the ID of the user who sent the original message/event that was reported.
       canonical_alias (str): The canonical alias of the room. null if the room does not have a canonical alias set.
       event_json (EventJson): Details of the original event that was reported.
    """

    event_json: EventJson
    id: int
    received_ts: int
    room_id: str
    name: str
    event_id: str
    user_id: str
    reason: str
    score: int
    sender: str
    canonical_alias: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventDetails":
        event_json = EventJson.from_dict(data["event_json"])
        del data["event_json"]
        return cls(**data, event_json=event_json)
