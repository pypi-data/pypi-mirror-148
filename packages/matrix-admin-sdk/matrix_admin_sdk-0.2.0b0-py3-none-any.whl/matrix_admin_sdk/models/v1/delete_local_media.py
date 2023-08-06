from dataclasses import dataclass
from typing import List

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class DeleteLocalMediaModel(BaseModel):
    """
    DeleteLocalMedia class
    Attributes:
        deleted_media (list[str]): List of deleted media_id
        total (int): Total number of deleted media_id
    """

    deleted_media: List[str]
    total: int
