from typing import List

from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v2.user_devices import UserDeviceModel, UserDevicesModel

from .endpoint import Endpoint


class UserDevices(Endpoint):
    def __int__(self, user_id: str, **kwargs):
        """
        Initialize UserDevices endpoint
        Args:
            user_id: fully-qualified user id: for example, @user:server.com
            **kwargs: keyword arguments to pass to Endpoint

        Returns: None

        """
        self.user_id = user_id
        super().__init__(**kwargs)

    async def get_all(self) -> UserDevicesModel:
        """
        Gets information about all devices for a specific user_id.

        Returns: UserDevicesModel

        """
        url = self.url(f"users/{self.user_id}/devices")
        result = await self.request(RequestMethods.GET, url)
        res: UserDevicesModel = UserDevicesModel.from_dict(result)
        return res

    async def delete_multiple(self, devices: List[str]) -> None:
        """
        Deletes the given devices for a specific user_id, and invalidates any
        access token associated with them.
        Args:
            devices: The list of device IDs to delete.

        Returns: None

        """
        url = self.url(f"users/{self.user_id}/delete_devices")
        data = {"devices": devices}
        await self.request(RequestMethods.POST, url, json=data)

    async def show(self, device_id: str) -> UserDeviceModel:
        """
        Gets information on a single device, by device_id for a specific user_id.
        Args:
            device_id: The device to retrieve.

        Returns:

        """
        url = self.url(f"users/{self.user_id}/devices/{device_id}")
        result = await self.request(RequestMethods.GET, url)
        res: UserDeviceModel = UserDeviceModel.from_dict(result)
        return res

    async def update(self, device_id: str, display_name: str) -> None:
        """
        Updates the metadata on the given device_id for a specific user_id.
        Args:
            device_id: The device to update.
            display_name: The new display name for this device. If not given,
                the display name is unchanged.

        Returns: None

        """
        url = self.url(f"users/{self.user_id}/devices/{device_id}")
        data = {"display_name": display_name}
        await self.request(RequestMethods.PUT, url, json=data)

    async def delete(self, device_id: str) -> None:
        """
        Deletes the given device_id for a specific user_id, and invalidates any
            access token associated with it.
        Args:
            device_id: The device to delete.

        Returns: None

        """
        url = self.url(f"users/{self.user_id}/devices/{device_id}")
        await self.request(RequestMethods.DELETE, url)
