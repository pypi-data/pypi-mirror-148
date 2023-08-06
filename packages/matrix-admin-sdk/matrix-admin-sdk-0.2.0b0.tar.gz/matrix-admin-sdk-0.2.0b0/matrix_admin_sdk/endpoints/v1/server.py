from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.server import ServerVersionModel

from .endpoint import Endpoint


class Server(Endpoint):
    async def get_version(self) -> ServerVersionModel:
        """
        This API returns the running Synapse version and the Python version on
        which Synapse is being run. This is useful when a Synapse instance is
        behind a proxy that does not forward the 'Server' header (which also
        contains Synapse version information).

        Returns:

        """
        url = self.url("server_version")
        result = await self.request(RequestMethods.GET, url)
        res: ServerVersionModel = ServerVersionModel.from_dict(result)
        return res
