from dataclasses import dataclass
from typing import Optional

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class RegistrationTokensModel(BaseModel):
    """
    Most endpoints make use of JSON objects that contain details about tokens.
    These objects have the following fields

    Attributes:
        token (str): The token which can be used to authenticate registration.
        uses_allowed (int): The number of times the token can be
            used to complete a registration before it becomes invalid.
        pending (int): The number of pending uses the token has. When someone uses
            the token to authenticate themselves, the pending counter is
            incremented so that the token is not used more than the permitted
             number of times. When the person completes registration the pending
             counter is decremented, and the completed counter is incremented.
        completed (int): The number of times the token has been used to successfully
            complete a registration.
        expiry_time (int|None): The latest time the token is valid. Given as the
            number of milliseconds since 1970-01-01 00:00:00 UTC (the start of the
             Unix epoch).
    """

    token: str
    uses_allowed: int
    pending: int
    completed: int
    expiry_time: Optional[int]
