from dataclasses import dataclass
from typing import Any, Dict, List

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class CurrentUpdate(BaseModel):
    """
    CurrentUpdate

    Attributes:
        db_name: the database name (usually Synapse is configured with a single database named 'master')
        name (str):  the name of the update
        total_item_count (int):total number of "items" processed (the meaning of
            'items' depends on the update in question)
        total_duration_ms (float): how long the background process has been running,
            not including time spent sleeping
        average_items_per_ms (float): how many items are processed per millisecond
            based on an exponential average
    """

    db_name: str
    name: str
    total_item_count: int
    total_duration_ms: float
    average_items_per_ms: float


@dataclass
class StatusModel(BaseModel):
    """
    StatusModel
    Attributes:
        enabled: whether the background updates are enabled or disabled
        current_updates: a list of the current updates being processed
    """

    enabled: bool
    current_updates: List[CurrentUpdate]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StatusModel":
        current_updates = []
        for k, v in data["current_updates"].items():
            v["db_name"] = k
            current_updates.append(CurrentUpdate.from_dict(v))
        return cls(enabled=data["enabled"], current_updates=current_updates)


@dataclass
class EnabledModel(BaseModel):
    """
    EnabledModel

    Attributes:
        enabled (bool): whether the background updates are enabled or disabled
    """

    enabled: bool
