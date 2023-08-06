from matrix_admin_sdk.endpoints import RequestMethods

from .endpoint import Endpoint


class DeleteGroup(Endpoint):
    """
    Delete a group.
    """

    async def delete(self, group_id) -> None:
        """
        This API lets a server admin delete a local group.
        Doing so will kick all users out of the group so that their
        clients will correctly handle the group being deleted.
        Args:
            group_id: The group ID to delete.
        """
        url = self.url(f"delete_group/{group_id}")
        await self.request(RequestMethods.POST, url, json={})
