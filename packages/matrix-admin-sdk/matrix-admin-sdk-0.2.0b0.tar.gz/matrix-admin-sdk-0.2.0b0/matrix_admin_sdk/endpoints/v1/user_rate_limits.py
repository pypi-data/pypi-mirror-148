from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.user_rate_limits import RateLimitsStatusModel

from .endpoint import Endpoint


class UserRateLimits(Endpoint):
    """
    This API allows to override or disable ratelimiting for a specific user.
    There are specific APIs to set, get and delete a ratelimit.
    """

    def __int__(self, user_id: str, **kwargs):
        """
        Initialize User endpoint
        Args:
            user_id: fully-qualified user id: for example, @user:server.com
            **kwargs: key

        Returns: None

        """
        self.user_id = user_id
        super().__init__(**kwargs)

    async def get_status(self) -> RateLimitsStatusModel:
        """
        Get the ratelimit status for a user.
        Returns: RateLimitsStatusModel

        """
        url = self.url(f"users/{self.user_id}/override_ratelimit")
        result = await self.request(RequestMethods.GET, url)
        res: RateLimitsStatusModel = RateLimitsStatusModel.from_dict(result)
        return res

    async def set(
        self, messages_per_second: int, burst_count: int
    ) -> RateLimitsStatusModel:
        """
        Set the ratelimit for a user.
        Args:
            messages_per_second: The number of actions that can be performed in a second
            burst_count: How many actions that can be performed before being limited

        Returns: RateLimitsStatusModel

        """
        url = self.url(f"users/{self.user_id}/override_ratelimit")
        data = {"messages_per_second": messages_per_second, "burst_count": burst_count}
        result = await self.request(RequestMethods.POST, url, json=data)
        res: RateLimitsStatusModel = RateLimitsStatusModel.from_dict(result)
        return res

    async def delete(self) -> None:
        """
        Delete the ratelimit for a user.
        Returns: None

        """
        url = self.url(f"users/{self.user_id}/override_ratelimit")
        await self.request(RequestMethods.DELETE, url)
