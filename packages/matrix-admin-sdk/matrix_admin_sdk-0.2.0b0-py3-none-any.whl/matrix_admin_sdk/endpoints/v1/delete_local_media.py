from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.delete_local_media import DeleteLocalMediaModel

from .endpoint import Endpoint


class DeleteLocalMedia(Endpoint):
    """
    This API deletes the local media from the disk of your own server.
    This includes any local thumbnails and copies of media downloaded from remote
    homeservers. This API will not affect media that has been uploaded
    to external media repositories
    (e.g https://github.com/turt2live/matrix-media-repo/).
    """

    async def specific_local_media(
        self, server_name: str, media_id: str
    ) -> DeleteLocalMediaModel:
        """
        Delete a specific media_id
        Args:
            server_name: The name of your local server (e.g matrix.org)
            media_id:The ID of the media (e.g abcdefghijklmnopqrstuvwx)

        Returns: DeleteLocalMediaModel

        """
        url = self.url(f"media/{server_name}/{media_id}")
        result = await self.request(RequestMethods.DELETE, url)
        res: DeleteLocalMediaModel = DeleteLocalMediaModel.from_dict(result)
        return res

    async def local_media_by_date_or_size(
        self,
        server_name: str,
        before_ts: int,
        size_gt: int = 0,
        keep_profiles: bool = True,
    ):
        """
        Delete local media by date or size
        Args:
            server_name: The name of your local server (e.g matrix.org).
            before_ts: Unix timestamp in milliseconds. Files that were last used before
                this timestamp will be deleted. It is the timestamp of last access,
                not the timestamp when the file was created.
            size_gt: Size of the media in bytes. Files that are larger will be deleted.
                Defaults to 0.
            keep_profiles: Switch to also delete files that are still used in image
                data (e.g user profile, room avatar). If false these files will be
                deleted. Defaults to true.

        Returns:

        """
        keep_profile_string = "true" if keep_profiles else "false"

        url = self.url(
            f"media/{server_name}/delete?before_ts={before_ts}&size_gt={size_gt}&keep_profiles={keep_profile_string}"
        )

        result = await self.request(RequestMethods.POST, url, json={})
        return DeleteLocalMediaModel.from_dict(result)
