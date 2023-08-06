from dataclasses import dataclass
from typing import Any, Dict, List

from matrix_admin_sdk.models.base_model import BaseModel


@dataclass
class UserDeviceModel(BaseModel):
    """
    UserDeviceModel class
    Attributes:
        device_id (str): Identifier of device
        display_name (str):  Display name set by the user for this device.
            Absent if no name has been set.
        last_seen_ip (str): The IP address where this device was last seen.
            (May be a few minutes out of date, for efficiency reasons).
        last_seen_ts (int): The timestamp (in milliseconds since the unix epoch)
            when this devices was last seen. (May be a few minutes out of date,
            for efficiency reasons).
        user_id (str): Owner of device.
    """

    device_id: str
    display_name: str
    last_seen_ip: str
    last_seen_ts: int
    user_id: str


@dataclass
class UserDevicesModel(BaseModel):
    """
    UserDevicesModel
    Attributes:
        devices (list): An array of objects, each containing information about a device
        total (int): Total number of devices
    """

    devices: List[UserDeviceModel]
    total: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        user_devices = [UserDeviceModel.from_dict(i) for i in data.get("devices", [])]
        return cls(devices=user_devices, total=data.get("total", 0))
