from dataclasses import dataclass
from typing import List

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class QueryingMediaModel(BaseModel):
    """
    Querying media model.
    Attributes:
        local (list[str]):
        remote (list[str]):
    """

    local: List[str]
    remote: List[str]
