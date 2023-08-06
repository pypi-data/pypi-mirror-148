from enum import Enum
from typing import Optional

from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.federation import (
    DestinationModel,
    DestinationRoomsModel,
    DestinationsModel,
)

from .endpoint import Endpoint


class OrderBy(Enum):
    """
    Enum for destinations order by
    Attributes:
        DESTINATION: Destinations are ordered alphabetically by remote server name.
            This is the default.
        RETRY_LAST_TS: Destinations are ordered by time of last retry attempt in ms.
        RETRY_INTERVAL: Destinations are ordered by how long until next retry in ms.
        FAILURE_TS: Destinations are ordered by when the server started failing in ms.
        LAST_SUCCESSFUL_STREAM_ORDERING:Destinations are ordered by the stream
            ordering of the most recent successfully-sent PDU
    """

    DESTINATION = "destination"
    RETRY_LAST_TS = "retry_last_ts"
    RETRY_INTERVAL = "retry_interval"
    FAILURE_TS = "failure_ts"
    LAST_SUCCESSFUL_STREAM_ORDERING = "last_successful_stream_ordering"


class Federation(Endpoint):
    """
    This API allows a server administrator to manage Synapse's federation with
    other homeservers.
    """

    async def get_destinations(
        self,
        from_: int = 0,
        limit: int = 100,
        order_by: Optional[OrderBy] = None,
        dir_: str = "f",
    ) -> DestinationsModel:
        """
        This API gets the current destination retry timing info for all remote servers.

        The list contains all the servers with which the server federates,
        regardless of whether an error occurred or not. If an error occurs,
        it may take up to 20 minutes for the error to be displayed here, as
        a complete retry must have failed.
        Args:
            from_: Offset in the returned list. Defaults to 0
            limit: Maximum amount of destinations to return. Defaults to 100.
            order_by: The method in which to sort the returned list of destinations.
                Default: OrderBy.DESTINATION
            dir_: Direction of room order. Either f for forwards or b for
                backwards. Setting this value to b will reverse the above sort order.
                Defaults to f

        Returns:

        """
        url = self.url("federation/destinations")
        order_by = order_by if order_by is not None else OrderBy.DESTINATION
        params = {
            "from": from_,
            "limit": limit,
            "order_by": order_by.value,
            "dir": dir_,
        }
        result = await self.request(RequestMethods.GET, url, params=params)
        res: DestinationsModel = DestinationsModel.from_dict(result)
        return res

    async def get_destination_details(self, destination: str) -> DestinationModel:
        """
        This API gets the retry timing info for a specific remote server.
        Args:
            destination: Name of the remote server

        Returns: DestinationModel

        """
        url = self.url(f"federation/destinations/{destination}")
        result = await self.request(RequestMethods.GET, url)
        res: DestinationModel = DestinationModel.from_dict(result)
        return res

    async def get_destination_rooms(
        self,
        destination: str,
        from_: int = 0,
        limit: int = 100,
        dir_: str = "f",
    ) -> DestinationRoomsModel:
        """
        This API gets the rooms that federate with a specific remote server.

        Args:
            destination: Name of the remote server
            from_: Offset in the returned list. Defaults to 0
            limit: Maximum amount of destinations to return. Defaults to 100.
            dir_: Direction of room order by room_id. Either f for forwards
                or b for backwards. Defaults to f

        Returns: DestinationRoomsModel

        """
        url = self.url(f"federation/destinations/{destination}/rooms")
        params = {
            "from": from_,
            "limit": limit,
            "dir": dir_,
        }
        result = await self.request(RequestMethods.GET, url, params=params)
        res: DestinationRoomsModel = DestinationRoomsModel.from_dict(result)
        return res

    async def reset_connection_timeout(self, destination: str) -> None:
        """
        Synapse makes federation requests to other homeservers. If a federation
        request fails, Synapse will mark the destination homeserver as offline,
        preventing any future requests to that server for a "cooldown" period.
        This period grows over time if the server continues to fail its
        responses (exponential backoff).

        Admins can cancel the cooldown period with this API.

        This API resets the retry timing for a specific remote server and tries
        to connect to the remote server again. It does not wait for the next
        retry_interval. The connection must have previously run into an error
        and retry_last_ts (Destination Details API) must not be equal to 0.

        The connection attempt is carried out in the background and can take
        a while even if the API already returns the http status 200.
        Args:
            destination: Name of the remote server

        Returns: None

        """
        url = self.url(f"federation/destinations/{destination}/reset_connection")
        await self.request(RequestMethods.POST, url, json={})
