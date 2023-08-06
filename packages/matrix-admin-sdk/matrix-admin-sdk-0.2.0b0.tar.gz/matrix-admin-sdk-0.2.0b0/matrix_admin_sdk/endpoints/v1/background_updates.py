from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.background_updates import EnabledModel, StatusModel

from .endpoint import Endpoint


class BackgroundUpdates(Endpoint):
    """
    This API allows a server administrator to manage the background
    updates being run against the database.
    """

    async def status(self) -> StatusModel:
        """
        This API gets the current status of the background updates.
        """
        url = self.url("background_updates/status")
        result = await self.request(RequestMethods.GET, url)
        return StatusModel.from_dict(result)

    async def enabled(self, enabled: bool) -> EnabledModel:
        """
        This API allows pausing background updates.

        Background updates should not be paused for significant periods of time,
        as this can affect the performance of Synapse.

        Note: This won't persist over restarts.

        Note: This won't cancel any update query that is currently running.
        This is usually fine since most queries are short lived, except for
        CREATE INDEX background updates which won't be cancelled once started.
        Args:
            enabled: sets whether the background updates are enabled or disabled.

        Returns: The new status of the background updates.
        """
        url = self.url("background_updates/enabled")
        data = {"enabled": enabled}
        result = await self.request(RequestMethods.POST, url, json=data)
        res: EnabledModel = EnabledModel.from_dict(result)
        return res

    async def run(self, job_name: str) -> None:
        """
        This API schedules a specific background update to run.
        The job starts immediately after calling the API.

        Args:
            job_name: A string which job to run. Valid values are:
                - "populate_stats_process_rooms": Recalculate the stats for all rooms.
                - "regenerate_directory":Recalculate the user directory if it is stale or out of sync.

        """
        url = self.url("background_updates/start_job")
        data = {"job_name": job_name}
        await self.request(RequestMethods.POST, url, json=data)
