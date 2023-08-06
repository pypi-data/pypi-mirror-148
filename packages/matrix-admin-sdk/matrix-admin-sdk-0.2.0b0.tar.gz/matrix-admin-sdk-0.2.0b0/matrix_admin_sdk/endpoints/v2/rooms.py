from typing import Dict, Optional

from matrix_admin_sdk.endpoints import RequestMethods

from .endpoint import Endpoint


class Rooms(Endpoint):
    async def delete(
        self,
        room_id: str,
        new_room_user_id: Optional[str] = None,
        room_name: str = "Content Violation Notification",
        message: Optional[str] = None,
        block: bool = False,
        purge: bool = True,
        force_purge: bool = False,
    ) -> Dict[str, str]:
        """
        **Note**: This API is new, experimental and "subject to change".

        This version works asynchronously, meaning you get the response from server
        immediately while the server works on that task in background. You
        can then request the status of the action to check if it has completed.


        Args:
            room_id: room id to delete
            new_room_user_id: If set, a new room will be created with this
                user ID as the creator and admin, and all users in the old room will
                be moved into that room. If not set, no new room will be created and
                the users will just be removed from the old room. The user ID must be
                on the local server, but does not necessarily have to belong to a
                registered user.
            room_name: A string representing the name of the room that new users
                will be invited to. Defaults to Content Violation Notification
            message: A string containing the first message that will be sent as
                new_room_user_id in the new room. Ideally this will clearly convey
                why the original room was shut down. Defaults to Sharing illegal
                content on this server is not permitted and rooms in violation will
                be blocked.
            block: If set to true, this room will be added to a blocking list,
                preventing future attempts to join the room. Rooms can be blocked
                even if they're not yet known to the homeserver (only with Version 1
                of the API). Defaults to false.
            purge: If set to true, it will remove all traces of the room from
                your database. Defaults to true.
            force_purge: Optional, and ignored unless purge is true. If set to
                true, it will force a purge to go ahead even if there are local
                users still in the room. Do not use this unless a regular purge
                operation fails, as it could leave those users' clients in a
                confused state.

        Returns: {"delete_id": "<opaque id>"}

        """
        url = self.url(f"rooms/{room_id}")
        data = {
            "new_room_user_id": new_room_user_id,
            "room_name": room_name,
            "message": message,
            "block": block,
            "purge": purge,
            "force_purge": force_purge,
        }
        result = await self.request(RequestMethods.DELETE, url, json=data)
        return result
