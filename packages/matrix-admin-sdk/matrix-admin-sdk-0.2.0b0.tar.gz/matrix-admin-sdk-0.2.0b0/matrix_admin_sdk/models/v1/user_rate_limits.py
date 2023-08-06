from dataclasses import dataclass
from typing import Optional

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class RateLimitsStatusModel(BaseModel):
    """
    Class representing the rate limits status model.
    Attributes:
        messages_per_second (int): The number of actions that can be performed in a second.
            0 mean that ratelimiting is disabled for this user
        burst_count (int): How many actions that can be performed before being limited.
    """

    messages_per_second: Optional[int] = None
    burst_count: Optional[int] = None
