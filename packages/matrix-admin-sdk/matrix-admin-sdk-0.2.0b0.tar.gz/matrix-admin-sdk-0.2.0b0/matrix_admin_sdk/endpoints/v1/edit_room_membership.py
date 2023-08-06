from typing import Dict

from matrix_admin_sdk.endpoints import RequestMethods

from .endpoint import Endpoint


class EditRoomMembership(Endpoint):
    """
    Endpoint to edit a room membership.
    """

    async def join_user_to_room(
        self, room_id_or_alias: str, user_id: str
    ) -> Dict[str, str]:
        """
        This API allows an administrator to join an user account with a given user_id
        to a room with a given room_id_or_alias. You can only modify the membership
        of local users. The server administrator must be in the room and have
        permission to invite users.
        Args:
            room_id_or_alias: The room identifier or alias to join:
                for example, !636q39766251:server.com
            user_id: Fully qualified user: for example, @user:server.com

        Returns: {"room_id": "!636q39766251:server.com"}

        """
        url = self.url(f"join/{room_id_or_alias}")
        data = {"user_id": user_id}
        result = await self.request(RequestMethods.POST, url, json=data)
        return result
