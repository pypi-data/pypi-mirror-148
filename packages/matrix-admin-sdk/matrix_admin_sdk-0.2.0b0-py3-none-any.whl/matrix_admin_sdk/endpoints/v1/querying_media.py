from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.querying_media import QueryingMediaModel

from .endpoint import Endpoint


class QueryingMedia(Endpoint):
    """
    These APIs allow extracting media information from the homeserver.

    Details about the format of the media_id and storage of the media
    in the file system are documented under
    https://matrix-org.github.io/synapse/latest/media_repository.html
    """

    async def all_media_in_room(self, room_id: str) -> QueryingMediaModel:
        """
        This API gets a list of known media in a room. However,
        it only shows media from unencrypted events or rooms.
        Args:
            room_id: room id

        Returns: QueryingMediaModel

        """
        url = self.url(f"room/{room_id}/media")
        result = await self.request(RequestMethods.GET, url)
        res: QueryingMediaModel = QueryingMediaModel.from_dict(result)
        return res
