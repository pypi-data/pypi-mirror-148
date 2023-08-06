from typing import Dict, List

from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.forward_extremities import ForwardExtremitiesModel

from .endpoint import Endpoint


class ForwardExtremities(Endpoint):
    """
    Enables querying and deleting forward extremities from rooms.
    When a lot of forward extremities accumulate in a room, performance
    can become degraded. For details, see https://github.com/matrix-org/synapse/issues/1760
    """

    async def check_for_forward_extremities(
        self, room_id_or_alias: str
    ) -> List[ForwardExtremitiesModel]:
        """
        To check the status of forward extremities for a room
        Args:
            room_id_or_alias: The room id or alias to check

        Returns: list of ForwardExtremitiesModel

        """
        url = self.url(f"rooms/{room_id_or_alias}/forward_extremities")
        result = await self.request(RequestMethods.GET, url)
        res: List[ForwardExtremitiesModel] = [
            ForwardExtremitiesModel.from_dict(item) for item in result["results"]
        ]
        return res

    async def deleting_forward_extremities(
        self, room_id_or_alias: str
    ) -> Dict[str, int]:
        """
        **WARNING**: Please ensure you know what you're doing and have read the related
        issue #1760. Under no situations should this API be executed as an automated
        maintenance task!
        Args:
            room_id_or_alias: The room id or alias to delete

        Returns: {"deleted": 1}

        """
        url = f"rooms/{room_id_or_alias}/forward_extremities"
        result = await self.request(RequestMethods.DELETE, url)
        return result
