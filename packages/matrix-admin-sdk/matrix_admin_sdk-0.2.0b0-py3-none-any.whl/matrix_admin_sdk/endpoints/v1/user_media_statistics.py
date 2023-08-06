from enum import Enum
from typing import Optional

from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.user_media_statistics import UsersMediaStatisticsModel

from .endpoint import Endpoint


class OrderBy(Enum):
    """
    Enum for order by for user media statistics
    Attributes:
        USER_ID (str): Users are ordered alphabetically
        DISPLAY_NAME (str): Users are ordered alphabetically by displayname
        MEDIA_LENGTH (str): Users are ordered by the total size of uploaded media
            in bytes. Smallest to largest.
        MEDIA_COUNT (str): Users are ordered by number of uploaded media.
            Smallest to largest

    """

    USER_ID = "user_id"
    DISPLAY_NAME = "displayname"
    MEDIA_LENGTH = "media_length"
    MEDIA_COUNT = "media_count"


class UserMediaStatistics(Endpoint):
    """
    User Media Statistics Endpoint
    """

    async def user_media_statistics(
        self,
        limit: int = 100,
        from_: int = 0,
        order_by: Optional[OrderBy] = None,
        from_ts: Optional[int] = None,
        until_ts: Optional[int] = None,
        search_term: Optional[str] = None,
        dir_: str = "f",
    ) -> UsersMediaStatisticsModel:
        """
        Returns information about all local media usage of users. Gives the
        possibility to filter them by time and user
        Args:
            limit:  is used for pagination, denoting the maximum number of items
                to return in this call. Defaults to 100
            from_: used for pagination, denoting the offset in the returned results.
                This should be treated as an opaque value and not explicitly set to
                anything other than the return value of next_token from a previous call.
                Defaults to 0
            order_by: The method in which to sort the returned list of users.
                Defaults to OrderBy.USER_ID
            from_ts:  Considers only files created at this timestamp or later.
                Unix timestamp in ms.
            until_ts: Considers only files created at this timestamp or earlier.
                Unix timestamp in ms.
            search_term: Filter users by their user ID localpart or displayname.
                The search term can be found in any part of the string.
                Defaults to no filtering.
            dir_: Either f for forwards or b for backwards. Setting this value
                to b will reverse the above sort order. Defaults to f.

        Returns:

        """
        if order_by is None:
            order_by = OrderBy.USER_ID

        url = self.url("statistics/users/media")
        params = {
            "limit": limit,
            "from": from_,
            "order_by": order_by.value,
            "from_ts": from_ts,
            "until_ts": until_ts,
            "dir": dir_,
        }
        if search_term is not None:
            params["search_term"] = search_term

        result = await self.request(RequestMethods.GET, url, params=params)
        res: UsersMediaStatisticsModel = UsersMediaStatisticsModel.from_dict(result)
        return res
