from typing import Any, Dict, Optional, Protocol
from urllib.parse import urljoin


class Response(Protocol):
    text: str
    status_code: int

    def json(self) -> Dict[str, Any]:
        ...


class HttpClient(Protocol):
    async def get(
        self, url: str, headers: Dict[str, Any], params: Optional[Dict[str, Any]] = None
    ) -> Response:
        ...

    async def post(
        self, url: str, data: Dict[str, Any], headers: Dict[str, Any]
    ) -> Response:
        ...

    async def delete(
        self, url: str, data: Dict[str, Any], headers: Dict[str, Any]
    ) -> Response:
        ...

    async def put(
        self, url: str, data: Dict[str, Any], headers: Dict[str, Any]
    ) -> Response:
        ...


class MatrixAdminClient:
    """
    Matrix Admin SDK Client
    """

    def __init__(self, http_client: HttpClient, access_token: str, server_url: str):
        """
        Initialize Matrix Admin SDK Client
        Args:
            http_client: httpx.AsyncClient instance or similar with the same interface
            access_token: admin access token, see https://webapps.stackexchange.com/questions/131056/how-to-get-an-access-token-for-element-riot-matrix
            server_url: matrix server url, e.g. https://matrix.org
        """
        self._http_client = http_client
        self._access_token = access_token
        self._base_url = server_url

    @property
    def access_token(self) -> str:
        return f"Bearer {self._access_token}"

    @access_token.setter
    def access_token(self, access_token: str):
        self._access_token = access_token

    @property
    def request_headers(self) -> Dict[str, str]:
        return {"Authorization": self.access_token}

    async def get(
        self, /, endpoint: str, *, params: Optional[Dict[str, Any]] = None
    ) -> Response:
        url = urljoin(self._base_url, endpoint)
        return await self._http_client.get(
            url, params=params, headers=self.request_headers
        )

    async def post(self, /, endpoint: str, **kwargs) -> Response:
        url = urljoin(self._base_url, endpoint)
        return await self._http_client.post(url, headers=self.request_headers, **kwargs)

    async def delete(self, /, endpoint: str, **kwargs) -> Response:
        url = urljoin(self._base_url, endpoint)
        return await self._http_client.delete(
            url, headers=self.request_headers, **kwargs
        )

    async def put(self, /, endpoint: str, **kwargs) -> Response:
        url = urljoin(self._base_url, endpoint)
        return await self._http_client.put(url, headers=self.request_headers, **kwargs)
