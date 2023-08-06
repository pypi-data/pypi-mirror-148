from matrix_admin_sdk.endpoints.endpoint import Endpoint as BaseEndpoint


class Endpoint(BaseEndpoint):
    """
    Base class for all endpoints.
    """

    base_url = "/_synapse/admin/v2/"
