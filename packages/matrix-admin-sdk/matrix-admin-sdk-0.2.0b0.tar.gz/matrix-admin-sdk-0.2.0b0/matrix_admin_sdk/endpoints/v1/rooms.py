from enum import Enum
from typing import Any, Dict, List, Optional

from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.rooms import (
    BlockStatusModel,
    DeletedRoomModel,
    RoomMembersModel,
    RoomModel,
    RoomsModel,
    RoomStateModel,
)

from .endpoint import Endpoint


class OrderBy(Enum):
    """
    Enum for the order by parameter

    Attributes:
        NAME: Rooms are ordered alphabetically by room name. This is the default.
        CANONICAL_ALIAS: Rooms are ordered alphabetically by main alias address of the room.
        JOINED_LOCAL_MEMBERS: Rooms are ordered by the number of members. Largest to smallest.
        JOINED_LOCAL_MEMBERS: Rooms are ordered by the number of local members. Largest to smallest.
        VERSION: Rooms are ordered by room version. Largest to smallest.
        CREATOR: Rooms are ordered alphabetically by creator of the room.
        ENCRYPTION: Rooms are ordered alphabetically by the end-to-end encryption algorithm.
        FEDERATABLE: Rooms are ordered by whether the room is federatable.
        PUBLIC: Rooms are ordered by visibility in room list.
        JOIN_RULES: Rooms are ordered alphabetically by join rules of the room.
        GUEST_ACCESS: Rooms are ordered alphabetically by guest access option of the room.
        HISTORY_VISIBILITY: Rooms are ordered alphabetically by visibility of history of the room.
        STATE_EVENTS: Rooms are ordered by number of state events. Largest to smallest.
    """

    NAME = "name"
    CANONICAL_ALIAS = "canonical_alias"
    JOINED_MEMBERS = "joined_members"
    JOINED_LOCAL_MEMBERS = "joined_local_members"
    VERSION = "version"
    CREATOR = "creator"
    ENCRYPTION = "encryption"
    FEDERATABLE = "federatable"
    PUBLIC = "public"
    JOIN_RULES = "join_rules"
    GUEST_ACCESS = "guest_access"
    HISTORY_VISIBILITY = "history_visibility"
    STATE_EVENTS = "state_events"


class Rooms(Endpoint):
    """
    Rooms Endpoints API
    """

    async def list_rooms(
        self,
        from_: int = 0,
        limit: int = 100,
        order_by: Optional[OrderBy] = None,
        dir_: str = "f",
        search_term: Optional[str] = None,
    ) -> RoomsModel:
        """
        The List Room admin API allows server admins to get a list of rooms on
        their server. There are various parameters available that allow for
        filtering and sorting the returned list. This API supports pagination.

        Args:
            from_: Offset in the returned list. Defaults to 0
            limit: Maximum amount of rooms to return. Defaults to 100.
            order_by: The method in which to sort the returned list of rooms.
                Defaults to OrderBy.NAME.
            dir_: Direction of room order. Either f for forwards or b for backwards.
                Setting this value to b will reverse the above sort order. Defaults to f
            search_term: Filter rooms by their room name, canonical alias and
                room id. Specifically, rooms are selected if the search term is
                contained in: the room's name, the local part of the room's canonical alias,
                or the complete (local and server part) room's id (case sensitive).
                Defaults to no filtering.

        Returns:

        """
        if order_by is None:
            order_by = OrderBy.NAME
        if dir_ not in ("f", "b"):
            raise ValueError("dir_ must be either f or b")

        url = self.url("rooms")
        params = {
            "from": from_,
            "limit": limit,
            "order_by": order_by.value,
            "dir": dir_,
        }
        if search_term is not None:
            params["search_term"] = search_term

        result = await self.request(RequestMethods.GET, url, params=params)
        return RoomsModel.from_dict(result)

    async def room_details(self, room_id: str) -> RoomModel:
        """
        The Room Details admin API allows server admins to get all details of a room.
        Args:
            room_id: The room id to get details for.

        Returns:

        """
        url = self.url(f"rooms/{room_id}")
        result = await self.request(RequestMethods.GET, url)
        res: RoomModel = RoomModel.from_dict(result)
        return res

    async def room_members(self, room_id: str) -> RoomMembersModel:
        """
        The Room Members admin API allows server admins to get a list of all
        members of a room.
        Args:
            room_id: The room id to get details for.

        Returns: RoomMembersModel

        """
        url = self.url(f"rooms/{room_id}/members")
        result = await self.request(RequestMethods.GET, url)
        res: RoomMembersModel = RoomMembersModel.from_dict(result)
        return res

    async def room_state(self, room_id: str) -> List[RoomStateModel]:
        """
        The Room State admin API allows server admins to get a list of all state
        events in a room.
        Args:
            room_id: room id to get state for

        Returns: list of RoomStateModel

        """
        url = self.url(f"rooms/{room_id}/state")
        result = await self.request(RequestMethods.GET, url)
        res: List[RoomStateModel] = [
            RoomStateModel.from_dict(i) for i in result["state"]
        ]
        return res

    async def block_room(self, room_id: str, block: bool) -> Dict[str, bool]:
        """
        The Block Room admin API allows server admins to block and unblock rooms,
        and query to see if a given room is blocked. This API can be used to
        pre-emptively block a room, even if it's unknown to this homeserver.
        Users will be prevented from joining a blocked room.
        Args:
            room_id: The room id to block.
            block: If True the room will be blocked and if False the room will
                be unblocked.

        Returns: dictionary

        """
        url = self.url(f"rooms/{room_id}/block")
        data = {"block": block}
        result = await self.request(RequestMethods.PUT, url, json=data)
        return result

    async def get_block_status(self, room_id: str) -> BlockStatusModel:
        """
        Is room blocked
        Args:
            room_id: The room id to checking

        Returns: BlockStatusModel

        """
        url = self.url(f"rooms/{room_id}/block")
        result = await self.request(RequestMethods.GET, url)
        res: BlockStatusModel = BlockStatusModel.from_dict(result)
        return res

    async def delete_room(
        self,
        room_id: str,
        new_room_user_id: Optional[str] = None,
        room_name: str = "Content Violation Notification",
        message: str = "Sharing illegal content on this server is not permitted and rooms in violation will be blocked",
        block: bool = False,
        purge: bool = True,
        force_purge: bool = False,
    ) -> DeletedRoomModel:
        """
        The Delete Room admin API allows server admins to remove rooms from the
        server and block these rooms.

        Shuts down a room. Moves all local users and room aliases automatically
        to a new room if new_room_user_id is set. Otherwise local users only
        leave the room without any information.

        The new room will be created with the user specified by the new_room_user_id
        parameter as room administrator and will contain a message explaining
        what happened. Users invited to the new room will have power level -10
        by default, and thus be unable to speak.

        If block is true, users will be prevented from joining the old room.
        This option can in sync version also be used to pre-emptively block a room,
        even if it's unknown to this homeserver. In this case, the room will be
        blocked, and no further action will be taken. If block is false,
        attempting to delete an unknown room is invalid and will be rejected
        as a bad request.

        This API will remove all trace of the old room from your database after
        removing all local users. If purge is true (the default), all traces
        of the old room will be removed from your database after removing all
        local users. If you do not want this to happen, set purge to false.
        Depending on the amount of history being purged, a call to the API may
        take several minutes or longer.

        The local server will only have the power to move local user and room
        aliases to the new room. Users on other servers will be unaffected.

        This version works synchronously. That means you only get the response
        once the server has finished the action, which may take a long time.
        If you request the same action a second time, and the server has not
        finished the first one, the second request will block. This is fixed
        in version 2 of this API. The parameters are the same in both APIs.
        This API will become deprecated in the future.

        Args:
            room_id: The room id to delete
            new_room_user_id: If set, a new room will be created with this user
                ID as the creator and admin, and all users in the old room will be
                moved into that room. If not set, no new room will be created and
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
                even if they're not yet known to the homeserver (only with Version
                1 of the API). Defaults to false.
            purge: If set to true, it will remove all traces of the room from
                your database. Defaults to true.
            force_purge: Optional, and ignored unless purge is true. If set to
                true, it will force a purge to go ahead even if there are local
                users still in the room. Do not use this unless a regular purge
                operation fails, as it could leave those users' clients in a
                confused state.

        Returns:

        """
        url = self.url(f"rooms/{room_id}")
        data = {
            new_room_user_id: new_room_user_id,
            room_name: room_name,
            message: message,
            block: block,
            purge: purge,
            force_purge: force_purge,
        }
        result = await self.request(RequestMethods.DELETE, url, json=data)
        res: DeletedRoomModel = DeletedRoomModel.from_dict(result)
        return res

    async def make_room_admin(self, room_id_or_alias: str, user_id: str) -> None:
        """
        Grants another user the highest power available to a local user who is
        in the room. If the user is not in the room, and it is not publicly
        joinable, then invite the user.

        By default the server admin (the caller) is granted power, but another
        user can optionally be specified
        Args:
            room_id_or_alias: The room id or alias to make new admin
            user_id: The user id to make admin
        Returns:

        """
        url = self.url(f"rooms/{room_id_or_alias}/make_room_admin")
        data = {"user_id": user_id}
        await self.request(RequestMethods.POST, url, json=data)
        return None

    async def event_context(self, room_id: str, event_id: str) -> Dict[str, Any]:
        """
        This API lets a client find the context of an event. This is designed
        primarily to investigate abuse reports.
        Args:
            room_id:
            event_id:

        Returns:

        """
        raise NotImplementedError("This API is not yet implemented")
