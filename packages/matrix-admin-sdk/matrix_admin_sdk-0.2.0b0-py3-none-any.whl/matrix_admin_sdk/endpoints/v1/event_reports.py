from typing import Optional

from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.event_reports import EventDetails
from matrix_admin_sdk.models.v1.event_reports import EventReports as EventReportsModel

from .endpoint import Endpoint


class EventReports(Endpoint):
    """Event Reports endpoint"""

    async def show_reported_events(
        self,
        limit: int = 100,
        from_: int = 0,
        dir_: str = "b",
        user_id: Optional[str] = None,
        room_id: Optional[str] = None,
    ) -> EventReportsModel:
        """
        This API returns information about reported events
        Args:
            limit: used for pagination, denoting the maximum number of items to return in this call
            from_: used for pagination, denoting the offset in the returned results.
                This should be treated as an opaque value and not explicitly set
                to anything other than the return value of
                `next_token` from a previous call
            dir_: Direction of event report order. Whether to fetch the most recent first (b) or the oldest first (f).
            user_id: filters to only return users with user IDs that contain this value. This is the user who
                reported the event and wrote the reason
            room_id:  filters to only return rooms with room IDs that contain this value.

        Returns: list of event reports

        """
        url = self.url("event_reports")
        params = {
            "limit": limit,
            "from": from_,
            "dir": dir_,
            "user_id": user_id,
            "room_id": room_id,
        }
        result = await self.request(RequestMethods.GET, url, params=params)
        return EventReportsModel.from_dict(result)

    async def show_details(self, report_id: str) -> EventDetails:
        """
        This API returns information about a specific event report.
        Args:
            report_id: The ID of the event report

        Returns: event details

        """
        url = self.url(f"event_reports/{report_id}")
        result = await self.request(RequestMethods.GET, url)
        return EventDetails.from_dict(result)
