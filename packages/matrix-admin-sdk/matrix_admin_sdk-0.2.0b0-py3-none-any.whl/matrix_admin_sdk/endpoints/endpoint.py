import enum

from typing import Any, Awaitable, Callable, Dict, Protocol
from urllib.parse import urljoin

from matrix_admin_sdk import MatrixAdminClient


class MatrixAdminSdkError(Exception):
    def __init__(self, error: str, http_status_code: int):
        message = f"{error} {http_status_code=}"
        super().__init__(message)


class Response(Protocol):
    status_code: int
    text: str

    def json(self) -> Dict[str, Any]:
        ...


class RequestMethods(enum.Enum):
    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    DELETE = enum.auto()


RequestFunc = Callable[..., Awaitable[Response]]


class Endpoint:
    """
    Base class for all endpoints.
    """

    base_url = ""

    def __init__(self, admin_client: MatrixAdminClient):
        """
        Initialize the endpoint.
        Args:
            admin_client: MatrixAdminClient instance.
        """
        self.admin_client = admin_client

    def url(self, endpoint: str) -> str:
        return urljoin(self.base_url, endpoint)

    async def request(
        self, /, method: RequestMethods, url: str, **kwargs
    ) -> Dict[str, Any]:
        methods: Dict[RequestMethods, RequestFunc] = {
            RequestMethods.GET: self.admin_client.get,
            RequestMethods.POST: self.admin_client.post,
            RequestMethods.PUT: self.admin_client.put,
            RequestMethods.DELETE: self.admin_client.delete,
        }
        req = methods[method]
        response = await req(url, **kwargs)
        self.error_check(response)
        return response.json()

    @staticmethod
    def error_check(response: Response) -> None:
        if response.status_code < 300:
            return
        try:
            error = response.json()["error"]
        except (KeyError, TypeError):
            error = "Unknown error"

        raise MatrixAdminSdkError(error, response.status_code)
