from typing import Any, Dict, Optional

from matrix_admin_sdk.endpoints import RequestMethods

from .endpoint import Endpoint


class ServerNotices(Endpoint):
    """
    The API to send notices
    """

    async def server_notice(
        self,
        user_id: str,
        body: str,
        msg_type: str = "m.text",
        type_: str = "m.room.message",
        state_key: Optional[Any] = None,
    ) -> Dict[str, str]:
        """
        The API to send notices
        Args:
            user_id: user id to send notice
            body: the body of the notice
            msg_type: message type, Default: m.text
            type_: the type of event. Defaults to m.room.message
            state_key:Setting this will result in a state event being sent.

        Returns: {"event_id": "<event_id>"}

        """
        url = self.url("send_server_notice")
        data = {
            "user_id": user_id,
            "content": {"body": body, "msgtype": msg_type},
            "type": type_,
        }
        if state_key is not None:
            data["state_key"] = state_key
        result = await self.request(RequestMethods.POST, url, json=data)
        return result
